from pyproj import CRS
from pyproj import Transformer

def PointTransformation(x, y, sourceCode, destinationCode):
    sourceRef = CRS.from_epsg(sourceCode)
    dstRef = CRS.from_epsg(destinationCode)
    transformer = Transformer.from_crs(sourceRef, dstRef)
    n_x, n_y = transformer.transform(x, y)
    return [n_x, n_y]

def PointTOLocal(points, extent_left, extent_up, width, height):
    n_points = []
    for point in points:
        n_points.append([int((point[0] - extent_left)/width), int((extent_up - point[1])/height)])
    return n_points

