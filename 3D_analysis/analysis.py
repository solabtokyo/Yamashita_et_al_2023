import numpy as np
import pandas as pd

from skimage.transform import rescale
from skimage.measure import regionprops_table, marching_cubes, mesh_surface_area
from skimage.morphology import remove_small_objects
from skimage.segmentation import clear_border
from skimage.filters import unsharp_mask

import pyclesperanto_prototype as cle



def segment(data, suffix, description, sigma_spot_detection, sigma_outline, rescaling_factor=1):
    '''
    Segment samples

    data: name of the input data
    suffix: suffix of the input data
    description: description of the input data
    sigma_spot_detectio: sigma of Gaussian filter to detect of the peak spot of the samples
    sigma_outline: sigmae of Gaussian fileter to detect the edge of the samples
    rescaling factor: scale factor of rescaling
    '''
    cle.select_device('GTX')
    
    res = []
    for s in suffix:
        print(s)
        img = np.load(f'{data}{s}{description}.npy')
        if rescaling_factor!=1:
            img = rescale(img, rescaling_factor, anti_aliasing=True)
        img_gpu = cle.push(img)
        segmented = cle.voronoi_otsu_labeling(img_gpu, spot_sigma=sigma_spot_detection, outline_sigma=sigma_outline)
        res.append(cle.pull(segmented))

    return res


def filter_spheroid(segmented, props, volume_thresh=30000, solidity_thresh=0.7):
    '''
    Filter out spheroids without beads

    segmented: label images after segmentation
    props: calculated properties
    suffix: suffix of the input data  
    volume_thresh: threshold value of volume
    splidity_thresh: threshold value of solidity
    '''
    res_filtered = []
    for i, segment in enumerate(segmented):
        props_filtered = props[i][(props[i]['Volume']>volume_thresh)&(props[i]['Solidity']>solidity_thresh)]
        retained_label = props_filtered['Label'].values
        label_img = np.where(np.isin(segment, retained_label), segment, 0)
        res_filtered.append(label_img)
    
    return res_filtered
    

def filter_nucleus(nucleus, spheroid, suffix):
    '''
    Filter out nuclei in spheroids without beads

    nucleus: segmented labels of nuclei after segmentation
    spheroid: segmented labels of spheroid after segmentation
    suffix: suffix of the data of spheroid
    '''
    res_filtered = []
    for i, s in enumerate(suffix):
        spheroid[i] = spheroid[i]>0 # select area of spheroids
        nucleus_i = nucleus[i][:spheroid[i].shape[0], :, :spheroid[i].shape[2]] # adjust the size
        retained_labels = np.unique(nucleus_i[spheroid[i]]) # find labels of nucleus inside spheroids
        res_filtered.append(np.where(np.isin(nucleus[i], retained_labels), nucleus[i], 0)) 

    return  res_filtered


def calculate_props(segmented, suffix, target=('spheroid', 'nucleus'), scale=(None, None, None)):
    '''
    Calculate morphological properties of target objects

    segmented: segmented labels
    suffix: suffix of the input data    
    target: spheroid or nucleus
    scale: pixel resolution in μm scale
    '''
    res = []

    if target=='nucleus':
        surface = []
    
    for i, s_data in enumerate(segmented):
        print(suffix[i])

        # calculate properties
        s_data = remove_small_objects(s_data, min_size=100) # remove small objects
        if target=='spheroid':
            props = pd.DataFrame(regionprops_table(label_image=s_data,
                                                   properties=('label', 'area', 'solidity', 'bbox'), 
                                                   spacing=scale))
            props = props.rename(columns={'label':'Label', 'area': 'Volume', 'solidity': 'Solidity'})
            res.append(props)

        if target=='nucleus':
            s_data = clear_border(s_data) # remove objects on the edge
            props = pd.DataFrame(regionprops_table(label_image=s_data, 
                                                   properties=('label', 'area', 'axis_major_length', 'axis_minor_length', 
                                                               'solidity', 'bbox'),
                                                   spacing=scale))
            props = props.rename(columns={'area': 'Volume', 'axis_major_length': 'Major axis length', 
                                          'axis_minor_length': 'Minor axis length', 'solidity': 'Solidity'})
            props['Aspect ratio'] = props['Major axis length']/props['Minor axis length']
            res.append(props)
        
            for i, row in props.iterrows():
                label = row['label']
                bbox = np.array((row['bbox-0'], row['bbox-3'], row['bbox-1'], row['bbox-4'], row['bbox-2'], row['bbox-5']), dtype='uint64')
                labelled_object = s_data[bbox[0]:bbox[1], bbox[2]:bbox[3], bbox[4]:bbox[5]]
                labelled_object = np.where(labelled_object==label, True, False)
                verts, faces, _, _ = marching_cubes(labelled_object, spacing=scale)
                surface.append(mesh_surface_area(verts, faces))
           
    if target=='nucleus':
        res = pd.concat(res)
        res = res.reset_index(drop=True)
        res['label'] = np.arange(1, len(res)+1)
        
        res['Surface area'] = surface
        res['Surface-area-to-Volume'] = surface/res['Volume']
 
    return res