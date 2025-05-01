#---------------CONFIGURATION--------------------------------------------------<--
#in-code process parameters 0-skip / 1-enter
#first position - upscaling or resizing
#second position - deconvolution
#third position - sharpening
input_parameters = [1, 0, 1]

#var second_option decides between upscale or resize option
#if False - upscale
#it True - upsize
second_option = True
#parameters thet decides if you need to use antialiasing on your image (remove blur)
use_antialiasing = False
#scale factor decide how much on each axis you want to upscale an image
scale_factor_x = 3
scale_factor_y = 3
#---------------CONFIGURATION END--------------------------------------------------