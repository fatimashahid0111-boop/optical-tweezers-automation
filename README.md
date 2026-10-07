# Thorlabs Optical Tweezers Automation & Calibration

This repository contains Python scripts for automating the mechanical assembly and stage control of a Thorlabs optical tweezers system, alongside analytical tools for force calibration. 

## Overview
The project is divided into two primary components:
1. **Stage Automation:** Interfacing with Thorlabs Kinesis DLLs via Python to control stage positioning.
2. **Force Calibration:** Utilizing Back Focal Plane Interferometry (BFPI) to calculate trap stiffness using silica beads.

## Hardware & Dependencies
* Thorlabs Optical Tweezers Kit 
* Python 3.12
* Required libraries: `numpy`, `scipy`, `matplotlib`
* *Note: Thorlabs Kinesis DLLs must be installed locally and are not included in this repository.*

## Files
*  `/movestage.py` - The code I used to move the 3-axis piezo stage.
*  `/force_calibration.py` - The code I used to scan the sample through the laser's focal point and get piezo voltages to eventually find gamma factor.


### Calibration Results

<img width="900" height="500" alt="Figure_forcecalibration001" src="https://github.com/user-attachments/assets/deebf9b5-1222-413e-9fe7-f9971d6e63ca" />

**Force Calibration S-Curve**
This graph demonstrates the raw positional response of the trapped particle as the piezo stage scans it across the laser's focal point. The characteristic "S-curve" plots the Quadrant Photodiode (QPD) difference signal against the piezo output voltage. The steep central region crossing the zero-voltage difference mark represents the center of the optical trap, confirming the specific spatial region where the trapping force behaves linearly, akin to a harmonic oscillator (Hooke's Law).

<img width="900" height="500" alt="gamma001pic" src="https://github.com/user-attachments/assets/abcdfc7a-b5f8-4610-994d-c6a74b151312" />

**Silica Beads Gamma Factor Extraction**
This plot isolates the central linear regime of the S-curve (highlighted by the blue data points) to compute the detector's spatial calibration factor, or gamma. By applying a linear line of best fit (the red line), the slope determines the sensitivity of the QPD voltage to the physical displacement of the trapped particle. This extraction specifically for a Silica Microbead shows a sensitivity of 0.241 V/µm.


<img width="900" height="500" alt="znogammafact01" src="https://github.com/user-attachments/assets/483ce829-fbc1-4ba3-823a-60300f3b2295" />


**Steeper Gamma Factor Extraction**
Similar to the silica microbeads, this plot demonstrates a distinct extraction with a much steeper slope, yielding a higher sensitivity of 5.188 V/µm.

## Academic Context

This toolkit was developed as part of a final year undergraduate thesis project for the BS Physics program at the Pakistan Institute of Engineering and Applied Sciences (PIEAS). The research focused on the mechanical assembly and computational automation of the optical tweezers system, conducted under the supervision of Dr. Afshan Irshad.




