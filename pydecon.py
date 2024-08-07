import argparse
import logging
import shutil
from pathlib import Path

import RedLionfishDeconv as rl
import psfmodels as psfm
import skimage.restoration
import tifffile as tf

# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

METHODS = ['cpu', 'gpu', 'skimage']


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='PyDecon',
        description='Image deconvolution with Python. Uses psfmodels from Talley Lambert and RedLionfish from the Rosalind'
                    ' Franklin Institute.',
        epilog='https://github.com/FrancisCrickInstitute/python-decon'
    )
    parser.add_argument("--dxy", metavar='XY Size', type=float, help="Voxel size (microns) in x and y", default=1.0)
    parser.add_argument("--dz", type=float, help="Voxel size (microns) in z", default=1.0)
    parser.add_argument("--wd", type=float, help="Working distance (microns)", default=1000.0)
    parser.add_argument("--wl", type=float, help="Emission wavelength (microns)", default=0.5)
    parser.add_argument("--na", type=float, help="Numerical aperture", default=1.0)
    parser.add_argument("--method", type=str, help="Use GPU- or CPU-based deconvolution", default='gpu',
                        choices=METHODS)
    parser.add_argument("--iter", type=int, help="Number of iterations", default=20)
    parser.add_argument("--output", type=str, help="Output directory. Existing directories will be overwritten.",
                        required=False)
    parser.add_argument("input", type=str, help="Input file")
    return parser.parse_args()


def create_output_directory(output_path: Path):
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)


def generate_psf(args):
    psf = psfm.make_psf(61, 32, dxy=args.dxy, dz=args.dz, pz=0, ti0=args.wd, wvl=args.wl, NA=args.na)
    psf_path = args.output / 'psf.tiff'
    tf.imwrite(psf_path, psf)
    return psf, psf_path


def load_data(input_path: Path):
    return tf.imread(input_path)


def deconvolve(data, psf, args):
    if args.method == 'cpu':
        logger.info("CPU decon...")
        result = rl.doRLDeconvolutionFromNpArrays(data, psf, niter=args.iter, method='cpu')
    elif args.method == 'gpu':
        logger.info("GPU decon...")
        result = rl.doRLDeconvolutionFromNpArrays(data, psf, niter=args.iter)
    elif args.method == 'skimage':
        logger.info("SKImage decon...")
        result = skimage.restoration.richardson_lucy(data, psf, num_iter=args.iter, clip=False)
    else:
        raise ValueError(f"Unknown deconvolution method: {args.method}")
    return result


def save_result(result, result_path: Path, args):
    tf.imwrite(result_path, result, ome=True, resolution=(args.dxy, args.dxy),
               metadata={'spacing': args.dz, 'unit': 'um', 'axes': 'ZYX'}, compression='zlib')
    logger.info(f"{args.method.upper()} decon done.")
    return result_path


def main():
    args = parse_arguments()

    args.output = Path(args.output) if args.output else Path(args.input).parent / 'deconvolved_images'
    create_output_directory(args.output)

    psf, psf_path = generate_psf(args)
    logger.info(f"PSF saved to {psf_path}")

    data = load_data(args.input)
    logger.info(f"Image shape: {data.shape}")
    logger.info(f"PSF shape: {psf.shape}")

    try:
        result = deconvolve(data, psf, args)
        result_path = save_result(result, args.output / f'{Path(args.input).stem}_{args.method}_decon.tiff',
                                  args)
        logger.info(f"Result saved to {result_path}")
    except Exception as e:
        logger.error(f"Error during deconvolution: {e}")


if __name__ == "__main__":
    main()
