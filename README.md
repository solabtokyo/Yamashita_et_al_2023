# Custom-made codes of Yamashita et al., 2023, Small

## Description
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
To run the codes correctly, make a new directory called "result" and put "data" and "result" at the same layer as the directory of the codes as below.
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
Run "Simulate-velocity_make-figure2c.ipynb".  
A simulation to calculate a flow velocity distribution inside a microfluidic channel is performed and Fgure 2c is created.  

#### Veocity distribution for Figure 2f and Figure 2g
First, run "calculate-velocity-position".  
Velocities and positions of flowing objects are calculated.  
Then, run "make-figure2fg.ipynb".  
Figure 2f and Figure 2g are created.  

#### Movies for supplemental movies
Run "make-suppl-movies".  
Supplemental movies 3 to 6 are created.  

### 3D analysis
#### Effect of acoustic focusing for Figure 2e
Run "make-figure2e.ipynb".  
Images and a line plot for Figure 2e are created.  

#### 3D images acquired in one second for calculation of throughput and Figure 3
_Figure 3a_  
Run "make-figure3a.ipynb".  
Time-series images for Figure 2a are created.  

_Throughput, Figure 3b and Figure 3c_  
First, run "reconstruct_limited-frames_throughput-figure3bc.ipynb".  
3D images are reconstructed from a time series of optically sectioned 2D images acquired in one second.  
- Throughput  
To calculate the throughputs (cells and spheroids per second) using these images, run "analyze_throughput".  
- Figure 3b and Figure 3c  
Run "make-figure3bc.ipynb".  
Figure 3b and 3D images for Figure 3c are created.  
Figure 3c is created from these 3D images using Fiji.  

#### Analysis of 3D morphological properties for Figure 4b
First, run "reconstruct.ipynb".  
3D images of spheroids and suspended cells are reconstructed from a time series of optically sectioned 2D images.  
Then, run "analyze-nucleus-spheroid.ipynb" and "analyze-nucleus-suspended.ipynb".  
Morphological properties of nuclei are calculated and Figure 4b is created.  

#### Supplemental Figures S1 and S3
Make sure to reconstrunct 3D images for Figure 4b beforehand.  
Run "make-suppl1.ipynb" for Figure S1 and "make-suppl3.ipynb" for Figure S3.  
Figure S1 and Figure S3 are created.  

## Author
Minato Yamashira  
The University of Tokyo  
© 2023 Minatoya Yamashita
