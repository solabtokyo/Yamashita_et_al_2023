# Custom-made codes of Yamashita et al., 2023, Small
This is a repository for custom-made codes of Yamashita et al., 2023, Small (doi: XXX).  
Using these codes, velocity distributions and 3D morphological properties of nuclei are analyzed.  
Also, figures and movies attached to the manuscript are created.  

## Data
First of all, data to analyze have to be downloaded to the local environment.  
The original data are found on BioStudies (XXX).  
The data are separated into two directories:
- 2D images to analyze velocity dstributions
- 3D images (raw files and calibration-related files) to analyze the effect of acoustic focusing and morphological properties of nuclei

Make sure to put them in two separate directories called "2D" and "3D", respectively, and put the directories in one directory called "data".

## Directory structure
To run the codes correctly, make a new directory called "result" and put "data" and "result" at the same layer as the directory of the codes.
```
.
├── This repository (codes)
│          ├── Velocity_analysis
│          └── 3D_analysis  
├── data
│     ├── 2D
│     └── 3D    
└── result
```

## Machine environment
All the anlyses were conducted on Supermicro workstation (Super Micro Computer, Inc.).  
- OS: Ubuntu 16.04.7 LTS  
- CPU: Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz  
- GPU: GeForce GTX TITAN X (NVIDIA)  
- RAM: 125GB

The 3D analyses require GPU for segmentation.

The analyses have not been tested in other environments.  
If you have any problem, feel free to contanct us.

## Prerequisites
All the analyses were conducted using Python 3.8.  
The following libraries are necessary to run the codes.  
- astropy 5.2.2
- matplotlib 3.7.2
- numpy 1.24.4
- opencv-python 4.8.0
- pandas 2.0.3
- Pillow 10.0.0
- pyclesperanto-prototype 0.24.1
- scikit-image 0.21.0
- seaborn 0.12.2
- sympy 1.12
- tifffile 2023.7.10
- trackpy 0.6.1 


## Usage
### Velocity analysis
#### Flow velocity simulation for Figure 2c
