import arcpy
import json
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import cv2
from PIL import Image
import funcs.geoTransformation
import funcs.interpolationTool


# initialize the data to uint8
def __initial_visual__(img):
    img[img > 8848] = 0
    with np.errstate(all='ignore'):
        img = (255 * (img - img.min()).astype(np.float) / (img.max() - img.min()).astype(np.float)).astype(
            img.dtype)
    img = img.reshape(img.shape[0], img.shape[1])
    return img


class PathConv(object):
    def __init__(self):
        self.img = None  # numpy array from raster
        self.output_img = None  # output image format data
        self.output_tif = None  # output tiff format data (with geo-info)
        self.path_set = None  # input path
        self.raster = None  # input raster
        self.path_geo_info = None  # input path geo json
        self.extent = None  # input raster extent

    # load path
    def load_path(self, path_file):
        self.path_set = arcpy.FeatureSet(path_file)
        self.path_geo_info = json.loads(self.path_set.JSON)
        if self.path_geo_info["geometryType"] != 'esriGeometryPolyline':
            return False
        # print("Spatial Reference wkid: ", self.path_geo_info["spatialReference"]["wkid"])
        # self.sourceGeoRefCode = self.path_geo_info["spatialReference"]["wkid"]
        # print("Spatial Reference wkid: ", self.path_geo_info)
        self.__point_loading__()
        return True

    # load resampled points
    def __point_loading__(self):
        self.routes = []
        for route in self.path_geo_info["features"]:
            org_points = route['geometry']['paths'][0]
            tmp_route = []
            for point in org_points:
                tmp_route.append([point[0], point[1]])
            tmp_route = funcs.geoTransformation.PointTOLocal(tmp_route, self.extent.XMin, self.extent.YMax,
                                                             self.raster.meanCellWidth, self.raster.meanCellHeight)
            self.routes.append(tmp_route)
        self.routes = list(map(lambda p: funcs.interpolationTool.interpolationPoints(p, self.img.shape), self.routes))

    # load raster
    def load_raster(self, raster_file):
        self.raster = arcpy.sa.Raster(raster_file)
        self.extent = self.raster.extent
        # self.standardGeoRefCode = self.raster.spatialReference.GCS.factoryCode
        # print("standard code: ", self.standardGeoRefCode)
        self.img = self.raster.read()
        self.img[self.img > 8848] = 0

    # make raster visualization
    def visualize_raster(self, label_size):
        img = self.img.copy()
        img = __initial_visual__(img)
        img = img.astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        imgScr = self.__cvToQImage__(img)
        pixel_src = QPixmap.fromImage(imgScr).scaled(label_size[0], label_size[1])
        return pixel_src

    # make raster visualized after the convolution operation
    def visualize_afterPath(self, label_size):
        img = self.img.copy()
        img = __initial_visual__(img)
        for route in self.routes:
            for point in route:
                img[point[1], point[0]] = 255
        img = img.astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        imgScr = self.__cvToQImage__(img)
        pixel_src = QPixmap.fromImage(imgScr).scaled(label_size[0], label_size[1])
        return pixel_src

    # make the output visualized
    def visualize_output(self, label_size):
        img = self.output_img.copy()
        img = __initial_visual__(img)
        img = img.astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        imgScr = self.__cvToQImage__(img)
        pixel_src = QPixmap.fromImage(imgScr).scaled(label_size[0], label_size[1])
        return pixel_src

    # OpenCV format to QImage format
    def __cvToQImage__(self, data):
        # 8-bits unsigned, NO. OF CHANNELS=1
        channels = None
        if data.dtype == np.uint8:
            channels = 1 if len(data.shape) == 2 else data.shape[2]
        if channels == 3:  # CV_8UC3
            img = QImage(data, data.shape[1], data.shape[0], data.strides[0], QImage.Format_RGB888)
            return img.rgbSwapped()
        elif channels == 1:  # CV8UC1
            img = QImage(data, data.shape[1], data.shape[0], data.strides[0], QImage.Format_Indexed8)
            return img
        else:
            print("ERROR: numpy.ndarray could not be converted to QImage. Channels = %d" % data.shape[2])
            return QImage() # return NULL

    # convolution operation
    def path_convolution(self, img, kernel, method="mean"):
        assert method in ["mean", "max", "min"]
        assert kernel % 2 == 1
        # loop each router
        for route in self.routes:
            route_length = len(route)
            assert route_length > kernel
            half_kernel = int(kernel / 2)
            values = list(map(lambda x: self.img[x[1], x[0]][0], route)) # got the value of each router
            for i in range(half_kernel, route_length - half_kernel): # calculate and assign
                if method == "mean":
                    img[route[i][1], route[i][0]] = np.mean(values[i - half_kernel:i + half_kernel + 1])
                elif method == "max":
                    img[route[i][1], route[i][0]] = np.max(values[i - half_kernel:i + half_kernel + 1])
                elif method == "min":
                    img[route[i][1], route[i][0]] = np.min(values[i - half_kernel:i + half_kernel + 1])
        # create output image
        self.output_img = np.uint8(__initial_visual__(img))
        # create output tiff
        X_cell_size = self.raster.meanCellWidth
        Y_cell_size = self.raster.meanCellHeight
        lower_left_corner = self.raster.extent.lowerLeft
        self.output_tif = arcpy.NumPyArrayToRaster(img.reshape((img.shape[0], img.shape[1])), x_cell_size=X_cell_size,
                                                   y_cell_size=Y_cell_size, lower_left_corner=lower_left_corner)
        arcpy.management.DefineProjection(self.output_tif, self.raster.spatialReference)
        return img

    # image export
    def export_img(self, path):
        output = Image.fromarray(self.output_img)
        output.save(path)

    # tiff export
    def export_tiff(self, path):
        self.output_tif.save(path)
