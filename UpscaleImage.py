import PIL.Image
import numpy as np
import sys
import os
from skimage.transform import rescale, resize
from skimage.filters import unsharp_mask
from skimage import color, restoration
from scipy.signal import convolve2d as conv2
from scipy.signal import convolve as conv3
import matplotlib.pyplot as plt

from GetNameNPath import get_file_name
from Config import *

sys.stdout.reconfigure(encoding='utf-8')



#ДОИСПРАВИТЬ И ДОПИЛИТЬ, ПРИВЕСТИ КОД В ПОРЯДОК
def UpscaleImage(source_file_path):
    try:
        #convenient way for file renaming after processing
        #var for convenient naming after processing
        output_file_name, output_file_path  = get_file_name(source_file_path)

        #creating directory for saves
        if not os.path.exists(output_file_path):
            os.mkdir(output_file_path)
        else:
            print("Folder %s already exists" % output_file_path)

        print(f'Image received: {output_file_name}\nand will be saved in the following path:{output_file_path}')

        source_image = PIL.Image.open(source_file_path)
        #source_image.show()
        source_img_asarr = np.asarray(source_image)

        #print(source_img_asarr.ndim)
        #print(source_img_asarr.shape)
        result_image = source_img_asarr

        if input_parameters[0] == 1:
            #upscaling/resizing part
            #they are pretty much the same (even docs say that) but resize is more flexible with parameters
            if second_option == False:
                result_image = rescale(source_img_asarr, (scale_factor_x, scale_factor_y, 1), anti_aliasing=use_antialiasing)
                output_file_name += "_upscaled"
            else:
                result_image = resize(
                    source_img_asarr, (source_img_asarr.shape[0] * scale_factor_x, source_img_asarr.shape[1] * scale_factor_y),
                    anti_aliasing=use_antialiasing, mode='reflect', #symetric, wrap, edge, constant
                    anti_aliasing_sigma=0.5 #the downsampling factor, where s > 1. For the up-size case, s < 1,
                                            #no anti-aliasing is performed prior to rescaling. 
                )
                output_file_name += "_upsized"
        
            if use_antialiasing == True:
                output_file_name += "_AA"
            elif use_antialiasing == False:
                output_file_name += "_no_AA"
                
            print("Succesfully resized")

        if input_parameters[1] == 1:
        #deconvolution_part
        # The hardest to configure as it takes a lot of tries to 
        #figure the psf
        #Also works better with blurry images
        # for better setup see https://scikit-image.org/docs/stable/auto_examples/filters/plot_deconvolution.html
            rng = np.random.default_rng()
            #source_image_gray = color.rgb2gray(result_image)

            #psf is a Point Spread Function (tells how much to and where to shift the points of original image)
            #np.ones is a kernel that goes around the image, the less the more precise (but no less than 3 by 3)
            psf = np.ones((5, 5)) / 5 #/25
            conv = conv3(result_image, psf, 'same')
            # Add Noise to Image
            conv_noisy = conv.copy()
            conv_noisy += (rng.poisson(lam=25, size=conv.shape) - 10) / 255.0 #lam=25

            # Restore Image using Richardson-Lucy algorithm
            result_image = restoration.richardson_lucy(conv_noisy, psf, num_iter=10)
            #print(f"Arr of axis: {result_image.ndim}")
            result_image = color.gray2rgb(result_image)
            output_file_name += "_deconvoluted"
            print("Succesfully deconvoluted")

        if input_parameters[2] == 1:
        #sharpening_part
        #When applying this filter to several color layers independently, 
        #color bleeding may occur. More visually pleasing result can be achieved 
        #by processing only the brightness/lightness/intensity channel in a 
        #suitable color space such as HSV, HSL, YUV, or YCbCr.
            print(f"params: {result_image.shape}")
            result_image = unsharp_mask(result_image, radius=(5.5,5.5), amount=1.7, channel_axis=2)
            output_file_name += "_sharpened"
            print("Succesfully sharpened")

        if input_parameters[0] == 0 and input_parameters[1] == 0 and input_parameters[2] == 0:
            print("No parameters were chosen !")
            return
            #output_file_name += "_unchanged"
            
        #converting numpy arr back to image
        print(f'Result image parameters: dim={result_image.ndim}, size = {result_image.shape}')

        #For debug purposes
        """
        fig, axes = plt.subplots(ncols=2)
        ax = axes.ravel()
        ax[0].imshow(source_img_asarr)
        ax[0].set_title('Original image')
        ax[1].imshow(result_image)
        ax[1].set_title('Processed image')
        plt.tight_layout
        plt.show()
        """

        #----Saving image to machine------
        plt.imsave(output_file_path+output_file_name+'.png', result_image)
        #result_image.show()
        print("Processing completed !")

    except Exception as e:
        print(e)




