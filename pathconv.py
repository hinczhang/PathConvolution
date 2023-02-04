import argparse
from funcs.pathConv import PathConv

parser = argparse.ArgumentParser(description="Path convolution")
parser.add_argument('--vector', type=str, help='input path vector', required=True)
parser.add_argument('--raster', type=str, help='input raster', required=True)
parser.add_argument('--kernel', type=int, default=3, help='kernel size for convolution', choices=[3, 5, 7])
parser.add_argument('--method', type=str, default='mean', help='methods for convolution',
                    choices=['mean', 'max', 'min'])
parser.add_argument('--format', type=str, default='image', help='export format', choices=['image', 'tif'])
parser.add_argument('--path', type=str, help='export path', required=True)
args = parser.parse_args()

def report_error(e):
    print('The error type is: ', e.__class__.__name__)
    print('The error detail is: ', e)

def main():
    print(args.vector, args.kernel)
    solver = PathConv()

    try:
        solver.load_raster(args.raster)
        solver.load_path(args.vector)
    except Exception as e:
        report_error(e)
        return

    try:
        solver.path_convolution(img=solver.img, kernel=int(args.kernel), method=args.method)
    except Exception as e:
        report_error(e)
        return
    # TODO: finish the export part, require to change the interface in the PathConv Class



if __name__ == '__main__':
    main()
