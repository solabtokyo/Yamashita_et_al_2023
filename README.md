![figure_3c@300x](https://github.com/solabtokyo/Yamashita_et_al_2023/assets/36177990/a97757c7-e0d8-433f-8aab-176a496aceb1)
![Static Badge](https://img.shields.io/badge/Python-3-blue)  
![Static Badge](https://img.shields.io/badge/3D_cell_culture-blue)
![Static Badge](https://img.shields.io/badge/Adherent_cell-blue)
![Static Badge](https://img.shields.io/badge/3D_imaging_flow_cytometry-blue)
![Static Badge](https://img.shields.io/badge/Acoustofluidics-blue)
![Static Badge](https://img.shields.io/badge/Light--sheet%20microscopy-blue)
![Static Badge](https://img.shields.io/badge/Hydrogel_bead-blue)

# High-throughput 3D imaging flow cytometry of adherent 3D cell cultures
Minato Yamashita<sup>1</sup>†, Miu Tamamitsu<sup>1</sup>†, Hiromi Kirisako<sup>1</sup>, Yuki Goda<sup>1</sup>, Xiaoyao Chen<sup>1</sup>, Kazuki Hattori<sup>1</sup>\*, Sadao Ota<sup>1</sup>\*\*　　  
**Affiliations:**　<sup>1</sup>Research Center for Advanced Science and Technology, The University of Tokyo, 4-6-1 Komaba, Meguro-ku, Tokyo, 153-8904, Japan

\*Corresponding author. Email: kzkhattori@g.ecc.u-tokyo.ac.jp  
\*\*Corresponding author. Email: sadaota@solab.rcast.u-tokyo.ac.jp  
†These authors contributed equally to this work.  

**Abstract:**  
Three-dimensional (3D) cell cultures are indispensable in recapitulating in vivo environments. Among many 3D culture methods, the strategy to culture adherent cells on hydrogel beads to form spheroid-like structures is powerful for maintaining high cell viability and functions through an efficient supply of nutrients and oxygen. However, high-throughput, scalable technologies for 3D imaging of individual cells cultured on the hydrogel scaffolds are lacking. This study reports the development of a high-throughput, scalable 3D imaging flow cytometry (3D-iFCM) platform for analyzing spheroid models on hydrogel beads. This platform is realized by integrating a single objective lens-based fluorescence light-sheet microscopy with a microfluidic device employing a combination of hydrodynamic and acoustofluidic focusing techniques. This integration enabled an unprecedentedly high-throughput, robust optofluidic 3D imaging, processing 1,310 spheroids and 28,117 cells min<sup>-1</sup>. The large dataset obtained allows us to quantify and compare the nuclear morphology of adhering and suspended cells, revealing adhering cells have smaller nuclei with non-round surfaces. This platform's high throughput, robustness, and precision for analyzing the morphology of subcellular compartments in 3D culture models holds promising potential for various biomedical analyses, including image-based phenotypic screening of drugs with spheroids or organoids.

**Paper:** https://www.biorxiv.org/content/10.1101/2023.07.10.548361v2

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
│          ├── velocity_analysis
│          └── 3D_analysis  
├── data
│     ├── 2D
│     └── 3D
│          ├── raw
│          └── calib    
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
All the analysis codes for the paper are provided as jupyter notebooks (.ipynb).  
All the necessary modules for the analyses are provided as python files (.py).  

All the figures of the paper are created in the notebooks for the analyses or in the ones named "make-XXX.ipynb".

### Velocity analysis
#### Flow velocity simulation for Figure 2c
- simulate-velocity_make-figure2c.ipynb

A simulation assuming the Hagen–Poiseuille flow is performed.  
A flow velocity distribution inside a microfluidic channel is calculated.  

#### Veocity distribution for Figure 2f and Figure 2g
- calculate-velocity-position.ipynb

Velocities and positions of flowing spheroids are calculated under the conditions where acoustic and hydrodynamic focusing on or off.  

#### Movies for supplemental movies 3 to 6
- make-suppl-movies.ipynb

Movies (.mp4) of flowing spheroids under each condition are created.

### 3D analysis
#### Effect of acoustic focusing for Figure 2e
- make-figure2e.ipynb

Fluorescence intensity is summed to show the effect of acoustic focusing.  

#### 3D images acquired in one second for calculation of throughput and Figure 3
_Tiem-series figures for Figure 3a_  
- make-figure3a.ipynb

Time-series, optically sectioned 2D images are serially shown.  

_Reconstruction of 3D images for throughput calculation, Figure 3b and Figure 3c_  
- reconstruct_limited-frames_throughput-figure3bc.ipynb

3D images are reconstructed from a time series of optically sectioned 2D images acquired in one second.  
- analyze_throughput.ipynb

Throughputs (cells and spheroids per second) using these 3D images are calculated.


Figure 3c is created from these 3D images using Fiji.  

#### Analysis of 3D morphological properties for Figure 4b
- reconstruct.ipynb

3D images of spheroids and suspended cells are reconstructed from a time series of optically sectioned 2D images.  
- analyze-nucleus-spheroid.ipynb
- analyze-nucleus-suspended.ipynb

Morphological properties of nuclei of spheroids and suspended cells are calculated.  

#### Supplemental Figures S1 and S3
Make sure to reconstrunct 3D images for Figure 4b before running "make-XXX.ipynb".  

## Author
Minato Yamashira  
The University of Tokyo  
## License
© 2023 The University of Tokyo, Sadao Ota Lab
