import numpy as np
import psfmodels as psfm
from pycudadecon import decon
from skimage import io
from PIL import Image

nx = 11
nz = 11

# generate centered psf with a point source at `pz` microns from coverslip
# shape will be (127, 127, 127)
#psf = psfm.make_psf(np.linspace(-5, 5, 51), 127, dxy=0.05, dz=0.05, pz=0, ni=1.4, ns=1.443, NA=1.25, wvl=0.42)

#io.imsave('./psf.tiff', psf)

im = Image.open('./DAPI.tif')

image = np.array(im)

psf = io.imread('./psf.tiff')

result = decon(image, psf)

io.imsave('./DAPI_decon.tiff', result)
