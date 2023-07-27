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
### Velocity analysis
The velosity simulation was conducted on MacBook Air.  
- OS: macOS Big Sur 11.7.8
- CPU: Intel(R) Core(TM) i5-1030NG7 CPU @ 1.10GHz  
- RAM: 16GB

All the other analyses were conducted on the same envinronemt as 3D analysis below.
  
### 3D analysis
All the anlyses were conducted on Supermicro workstation (Super Micro Computer, Inc.).  
- OS: Ubuntu 16.04.7 LTS  
- CPU: Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz  
- GPU: GeForce GTX TITAN X (NVIDIA)  
- RAM: 125GB
The 3D analyses require GPU for segmentation.

The analyses have not been tested in other environments.  
If you have any problem, feel free contanct us.

## Prerequisites
All the analyses wew conducted using Python 3.8.  
The following libraries are necessary to run the codes.  
- numpy >1.23.3
- pandas 2.0.3
- matplotlib 3.7.2
- seaborn 0.12.2
- scikit-image 0.21.0
- pyclesperanto-prototype 0.24.1
- tifffile 2023.7.10
- astropy 5.2.2
- opencv-python 4.8.0
- Pillow 10.0.0
- trackpy 0.5.0
- sympy 1.11.1
