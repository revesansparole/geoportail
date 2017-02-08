from geoportail.crawler import get_tile
from geoportail.geotools import latlong_to_tile_coords


pos = (43.64269, 3.908987)  # (lat, long)
zoom = 1

tile_col, tile_row = latlong_to_tile_coords(zoom, pos[0], pos[1])

tile = get_tile(zoom, tile_col, tile_row)
tile.save("mytile.png")
