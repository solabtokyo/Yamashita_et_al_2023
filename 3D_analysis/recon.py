import numpy as np
import myfunctions as myfunc
from astropy.io import fits
import cv2
import gc
from skimage.transform import rescale


def reconstruction(data, suffix, wavelength, fps, mean_aspect_ratio, raw, calib, result, polarity=0, rescaling_factor=0.25, print_loop=False, start_end_frames=(None, None)):
    
                       
    '''
    Reconstruct 3D image

    data: data name of the input data
    suffix: suffix of the data
    wavelength: wavelength of excitation (405, 488)
    fps: frame per second
    mean_aspect_ratio: mean aspect ratio of bead or cell
    raw: path of raw data
    calib: path of calibration data
    result: path of result
    rescaling_factor: factor to rescale image
    polarity: scanning direction, forward (0) or reverse (1) 
    rescaling factor: scale factor of rescaling
    print_loop: whether to print loop counter
    start_end_frames: start and end frames to reconstruct
    '''

    # file names for calibrartion
    file_405_bg = 'bg_300Hz_100average_405.tif'
    file_488_bg = 'bg_300Hz_100average_488.tif'
    file_405_ex = 'ex_405.tif'
    file_488_ex = 'ex_488.tif'
    ex_bg_488 = 'bg_1Hz_100average_488.tif'

                       
    # acquisition parameters
    theta = np.arcsin(0.62/1.33) # angle of light sheet in water
    pixelsize = 6.5 # pixel size of the image sensor in um
    mag = 200/9 # magnification rate of imaging
    fps = fps # frame per second in Hz
    v = mean_aspect_ratio*fps*(pixelsize/mag) # scanning velocity in the flow direction in um/s
    F_indexmismatch = 1.412 # axial elongation factor due to refractive-index mismatch of remote focusing
    polarity = polarity # forward or reverse scanning direction
    coeff_405 = 0.994

    # calibration parameters
    kernel_movmean=10
    shift1_405 = (-10, 0, 0)
    p22 = [-4.2206e-7,  8.9098e-4, 2.2979]
    p27 = [-6.4205e-7,  0.0014, 1.6154]
    
    for s in suffix:
        print(s)
        file = raw+data+wavelength+s+'.fits'
        img = np.float32(fits.getdata(file))
        if start_end_frames!=(None, None):
            img = img[start_end_frames[0]:start_end_frames[1], ...]
        (dim_flow, dim_height, dim_width) = img.shape

        # prepare an array to store the reconstructed image
        if wavelength=='405':
            F_indexmismatch = F_indexmismatch/coeff_405
        
        T, dim_height_recon, dim_flow_recon = myfunc.get_affine_parameters(theta,pixelsize,mag, fps, v, F_indexmismatch, polarity, dim_height, dim_flow)
        img_stack = np.transpose(img, [1,2,0])
        img_out = np.zeros((dim_height_recon, dim_width, dim_flow_recon), dtype='float32')
        print('initialized')

        # calculate background and excitation profile
        if wavelength=='405':
            bg = file_405_bg
            ex = file_405_ex
        if wavelength=='488':
            bg = file_488_bg
            ex = file_488_ex
             
        img_bg, img_ex =  myfunc.calc_bg_ex_profiles(calib+bg, calib+ex, calib+ex_bg_488, kernel_movmean)
        
        if polarity==1:
            img_stack = np.flip(img_stack, 2)

        # calibrate the input image
        myfunc.bg_ex_calib(img_stack, img_bg, img_ex, dim_flow, wavelength, print_loop)

        if wavelength=='405':
            # shift the image
            img_stack = np.roll(img_stack, shift1_405, axis=(0,1,2))
        
        # reconstruct
        myfunc.affine_transform_3D(img_out, img_stack[:,:,0:dim_flow-1], T[:2], dim_width, dim_flow_recon, dim_height_recon, wavelength, print_loop)

        # delete unnecessary object
        del img_stack
        gc.collect()

        # flip image along the z-axis
        img_out = np.flip(img_out, axis=0)

        # calibrate spatially
        if wavelength=='405':
            X, Y, Z = img_out.shape
            x, y = np.meshgrid(np.arange(Z), np.arange(X))
            for k in np.arange(Y):
               offset405_Z = p27[2] + p27[1] * k + p27[0] * k**2
               offset405_X = p22[2] + p22[1] * k + p22[0] * k**2
               xq405, yq405 = np.float32(np.meshgrid(np.arange(Z) + offset405_Z, np.arange(X) + offset405_X))
               img_out[:,k,:] = cv2.remap(img_out[:,k,:], xq405, yq405, cv2.INTER_LINEAR)
            
        # rescale the image
        if rescaling_factor!=1:
            img_out = rescale(img_out, rescaling_factor, anti_aliasing=True)


        if start_end_frames!=(None, None):
            np.save(f'{result}{data}{wavelength}{s}_{start_end_frames[0]}-{start_end_frames[1]}.npy', img_out)    
        else:
            np.save(f'{result}{data}{wavelength}{s}.npy', img_out)