import math


def latlong_to_tile_coords(zoom, latitude, longitude):
    """Find tile coordinates of a given position.

    Notes:
        https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

    Args:
        zoom (int): zoom level
        latitude (float): latitude in degrees
        longitude (float): longitude in degrees

    Returns:
        (int, int): tile column, tile row
    """
    lat_rad = math.radians(latitude)
    n = 2.0 ** zoom
    tile_col = int((longitude + 180.0) / 360.0 * n)
    tile_row = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return tile_col, tile_row


def tile_resolution(zoom, latitude):
    """Compute resolution for a given position

    Notes:
        https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

    Args:
        zoom (int): zoom level
        latitude (float): latitude in degrees

    Returns:
        (float): [m.pix-1] number of meters per pixel in the tile
    """
    return 156543.034 * math.cos(math.radians(latitude)) / (2 ** zoom)


def tile_coords_to_latlong(zoom, tile_col, tile_row):
    """Find lat long of upper left corner of a tile.

    Notes:
        https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

    Args:
        zoom (int): zoom level
        tile_col (int): see :func:`latlong_to_tile_coords`
        tile_row (int): see :func:`latlong_to_tile_coords`

    Returns:
        (float, float, float, float): lat_nw, long_nw, lat_se, long_se
    """
    n = 2 ** zoom
    longitude = tile_col / n * 360.0 - 180.0
    latitude = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * tile_row / n))))

    return latitude, longitude
