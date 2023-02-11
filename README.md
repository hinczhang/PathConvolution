# PathConvolution
A QT application for path convolution. Contains the GUI end and the terminal end.  
## Required packages 
### open-source
- numpy
- pyqt5
- pyproj
- opencv-python
### commercial
- arcpy

Please use your ArcGIS Pro Package Manager to create a new virtual environment.
Then, install all the open-source packages there. 
## Terminal
For the terminal part, the parameter could be: `--raster ./test_data/clip_raster.tif --vector ./test_data/test_road.shp --path ./a.tif`  
These are compulsory parameters. For more, please view the `terminal.py`:  
```python
import argparse

parser = argparse.ArgumentParser(description="Path convolution")
parser.add_argument('--vector', type=str, help='input path vector', required=True)
parser.add_argument('--raster', type=str, help='input raster', required=True)
parser.add_argument('--kernel', type=int, default=3, help='kernel size for convolution', choices=[3, 5, 7])
parser.add_argument('--method', type=str, default='mean', help='methods for convolution',
                    choices=['mean', 'max', 'min'])
parser.add_argument('--format', type=str, default='image', help='export format', choices=['image', 'tif'])
parser.add_argument('--path', type=str, help='export path', required=True)
```
