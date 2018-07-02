import numpy as np
from astropy import units as u
from astropy.nddata import CCDData
import ccdproc
import astropy
from astropy.io import fits
import glob
import os
# we organise the dark image first by bias substracting the dark file

dark_raw = astropy.nddata.CCDData.read('dark_stacked.fit', unit="electron")
print ("dark import success")
bias = CCDData(np.full((512, 512), np.min(dark_raw)), unit="electron")
print ("bias found")
dark = ccdproc.subtract_bias(dark_raw,bias)
flat_image = astropy.nddata.CCDData.read('dome_stacked_h.fit', unit="electron")
dark_flat = ccdproc.subtract_dark(flat_image, dark,
                                  dark_exposure=20*u.second,
                                  data_exposure=20*u.second,
                                  scale=True)
print ("bias subtracted from dark")
file_list = glob.glob("../../../../../Volumes/TD/SN2018cow/H/*.fits")

print (file_list)

output_folder = "./reduced_images/"

failed_images = []

for input_file in file_list:
	# try:
    image = astropy.nddata.CCDData.read(input_file, unit="electron")
    dark_bias_sub = ccdproc.subtract_dark(image, dark,
                                  dark_exposure=20*u.second, #exposure of dark/bias image
                                  data_exposure=200*u.second, #exposure of science image
                                  scale=True)
    flat_final_subdata = ccdproc.flat_correct(dark_bias_sub, dark_flat)

    flat_final_subdata.write(os.path.basename(input_file).replace(".fits",".reduced.fits"))
	# except (KeyboardInterrupt, SystemExit):
	# 	raise
	# except:
	# 	print "Failed to reduce images"
	# 	failed_images.append(input_file)
