"""
Set of functions to retrieve data from geoportail website
"""

import os
from PIL import Image
import requests
from io import BytesIO

from .geotools import latlong_to_tile_coords

base_url = "https://wxs.ign.fr/an7nvfzojv5wa96dsga5nk8w/geoportail/wmts"  # TODO token?


def retrieve_tile(params):
    """Request a specific tile from geoportail website.

    Args:
        params (dict): set of parameters

    Returns:
        (Image): returns None if request fails
    """
    res = requests.get(base_url, params=params)
    if res.status_code != 200:
        return None

    buff = BytesIO(res.content)
    img = Image.open(buff)
    return img


def get_tile(tile_zoom, tile_col, tile_row):
    """Get a tile from geoportail.

    Notes: images contains two layers:
            - orthophotos
            - cadastre parcels

    Args:
        tile_zoom (int): zoom level
        tile_col (int):
        tile_row (int):

    Returns:
        (Image): Returns None if request fails
    """
    params_background = {
        'layer': "ORTHOIMAGERY.ORTHOPHOTOS",
        'style': "normal",
        'tilematrixset': "PM",
        'Service': "WMTS",
        'Request': "GetTile",
        'Version': "1.0.0",
        'Format': "image/jpeg",
        'TileMatrix': tile_zoom,
        'TileCol': tile_col,
        'TileRow': tile_row
    }

    params_parcels = {
        'layer': "CADASTRALPARCELS.PARCELS",
        'style': "bdparcellaire",
        'tilematrixset': "PM",
        'Service': "WMTS",
        'Request': "GetTile",
        'Version': "1.0.0",
        'Format': "image/png",
        'TileMatrix': tile_zoom,
        'TileCol': tile_col,
        'TileRow': tile_row
    }
    img_background = retrieve_tile(params_background)
    if img_background is None:
        return None

    img_parcels = retrieve_tile(params_parcels)
    if img_parcels is None:
        return None

    img_parcels = img_parcels.convert("RGBA")
    img_background.paste(img_parcels, (0, 0), img_parcels)

    return img_background


def buffer_tile(root_dir, tile_zoom, tile_col, tile_row):
    """Retrieve tile if needed and store it in geoportail dir

    Args:
        root_dir (str): Root directory where to store tile images
        tile_zoom (int): zoom level
        tile_col (int):
        tile_row (int):

    Returns:
        (bool): whether storage was successful or not
    """
    dir_pth = "{}/{}/{}".format(root_dir, tile_zoom, tile_col)
    img_pth = "{}/{}.png.tile".format(dir_pth, tile_row)
    if os.path.exists(img_pth):
        return True

    tile_img = get_tile(tile_zoom, tile_col, tile_row)
    if tile_img is None:
        return False

    # register in _new to know what's been updated
    dir_pth = "{}_new/{}/{}".format(root_dir, tile_zoom, tile_col)
    img_pth = "{}/{}.png.tile".format(dir_pth, tile_row)
    if not os.path.exists(dir_pth):
        os.makedirs(dir_pth)
    tile_img.save(img_pth, "PNG")

    return True


def buffer_bbox(root_dir, zoom_level, north_west_corner, south_east_corner):
    """Buffer all tiles at this zoom level inside the given bounding box.

    Args:
        root_dir (str): Root directory where to store tile images
        zoom_level (int): zoom level
        north_west_corner (float, float): lat, long of north west corner
        south_east_corner (float, float): lat, long of south east corner

    Returns:
        (list of (int, int, int)): list of failed tiles (zoom, col, row)
    """
    icol_min, irow_min = latlong_to_tile_coords(zoom_level,
                                                north_west_corner[0],
                                                north_west_corner[1])
    icol_max, irow_max = latlong_to_tile_coords(zoom_level,
                                                south_east_corner[0],
                                                south_east_corner[1])
    errs = []
    tiles = [(icol, irow) for irow in range(irow_min, irow_max + 1) for icol in range(icol_min, icol_max + 1)]
    nb_tiles = len(tiles)
    for i, (icol, irow) in enumerate(tiles):
        print(icol, irow, int(i * 100. / nb_tiles))
        if not buffer_tile(root_dir, zoom_level, icol, irow):
            errs.append((zoom_level, icol, irow))

    return errs
