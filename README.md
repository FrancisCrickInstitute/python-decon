```
usage: PyDecon [-h] [--dxy XY Size] [--dz DZ] [--wd WD] [--wl WL] [--na NA] [--method {cpu,gpu,skimage}] [--iter ITER] [--output OUTPUT] input
                                                                                                                                              
Image deconvolution with Python. Uses psfmodels from Talley Lambert and RedLionfish from the Rosalind Franklin Institute.                     
                                                                                                                                              
positional arguments:                                                                                                                         
  input                 Input file                                                                                                            
                                                                                                                                              
options:                                                                                                                                      
  -h, --help            show this help message and exit                                                                                       
  --dxy XY Size         Voxel size (microns) in x and y                                                                                       
  --dz DZ               Voxel size (microns) in z                                                                                             
  --wd WD               Working distance (microns)                                                                                            
  --wl WL               Emission wavelength (microns)                                                                                         
  --na NA               Numerical aperture                                                                                                    
  --method {cpu,gpu,skimage}                                                                                                                  
                        Use GPU- or CPU-based deconvolution                                                                                   
  --iter ITER           Number of iterations                                                                                                  
  --output OUTPUT       Output directory. Existing directories will be overwritten.                                                           
                                                                                                                                              
https://github.com/FrancisCrickInstitute/python-decon
```
