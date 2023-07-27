import cv2 as cv2
import numpy as np
from PIL import Image as pilimage
import scipy.ndimage as scimg

def get_affine_parameters(theta, pixelsize, mag, fps, v, F_indexmismatch, polarity, dim_height, dim_flow):
    scale_z = (F_indexmismatch * np.cos(theta)) #first dimension
    scale_y = (v / fps / (pixelsize / mag)) #third dimension\

    M_yzscale = np.array([[scale_y, 0, 0],
                [0, scale_z, 0],
                [0, 0, 1]], dtype=np.float32)
    M_yzshear =  np.array([[1, np.tan(theta), 0],
                [0, 1, 0],
                [0, 0, 1]], dtype=np.float32)
    T = np.matmul(M_yzshear, M_yzscale)
    dim_height_recon = int(np.ceil(dim_height*scale_z))
    dim_flow_recon = int(np.ceil(dim_flow*scale_y + dim_height*scale_z*np.tan(np.abs(theta))))
    return T, dim_height_recon, dim_flow_recon

def get_increased_y_scale(theta, F_indexmismatch):
    scale_z = (F_indexmismatch * np.cos(theta)) #first dimension
    increased_y_scale = scale_z*np.tan(np.abs(theta))
    return increased_y_scale

def calc_bg_ex_profiles(path_bg, path_ex, path_ex_bg, kernel_movmean):
    img_bg = np.float32(np.array(pilimage.open(path_bg)))
    img_ex = np.float32(np.array(pilimage.open(path_ex)))-np.float32(np.array(pilimage.open(path_ex_bg)))
    img_ex = scimg.uniform_filter(img_ex, size=kernel_movmean, mode='constant')
    img_ex = img_ex / img_ex.mean()
    return img_bg, img_ex

def read_img_sequence(img_stack, img_bg, img_ex, dim_flow, path, color, printcurrentloop):
    data = pilimage.open(path)
    for i in np.arange(dim_flow):
        data.seek(i)
        img_stack[:,:,i] = (np.float32(np.array(data)) - img_bg) / img_ex
        if printcurrentloop:
            print('reading' + color + ':' + str(i) + '/' + str(dim_flow))
   
def affine_transform_3D(img_out, img_stack, T, dim_width, dim_flow_recon, dim_height_recon, color, printcurrentloop):
    for i in np.arange(dim_width):
        img_out[:,i,:] = cv2.warpAffine(img_stack[:,i,:], T, (dim_flow_recon, dim_height_recon), flags=cv2.INTER_CUBIC)
        if printcurrentloop:
            print('reconstructing' + color + ':' + str(i) + '/' + str(dim_width))

def bg_ex_calib(img_stack, img_bg, img_ex, dim_flow, color, printcurrentloop):
    for i in np.arange(dim_flow):
        img_stack[:,:,i] = np.clip((img_stack[:,:,i] - img_bg) / img_ex, 0, None)
        if printcurrentloop:
            print('reading' + color + ':' + str(i) + '/' + str(dim_flow))