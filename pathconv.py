import argparse


parser = argparse.ArgumentParser(description="Path convolution")
parser.add_argument('--vector', type=str, help='input path vector', required=True)
parser.add_argument('--raster', type=str, help='input raster', required=True)
parser.add_argument('--kernel', type=int, default=3, help='kernel size for convolution', choices = [3, 5, 7])

args = parser.parse_args()

if __name__ == '__main__':
    print(args.vector, args.kernel)