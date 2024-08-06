import psfmodels as psfm
from tifffile import imwrite

# generate centered psf with a point source at `pz` microns from coverslip
# shape will be (127, 127, 127)
psf = psfm.make_psf(61, 32, dxy=0.227, dz=0.5, pz=0, ti0=610, wvl=0.465, NA=0.8)
imwrite('./psf.tiff', psf)
