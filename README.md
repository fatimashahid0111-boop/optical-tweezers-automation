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


<img width="900" height="500" alt="Figure_forcecalibration001" src="https://github.com/user-attachments/assets/deebf9b5-1222-413e-9fe7-f9971d6e63ca" />

<img width="900" height="500" alt="znogammafact01" src="https://github.com/user-attachments/assets/483ce829-fbc1-4ba3-823a-60300f3b2295" /> 
<img width="900" height="500" alt="gamma001pic" src="https://github.com/user-attachments/assets/abcdfc7a-b5f8-4610-994d-c6a74b151312" />


## Usage
Ensure the Thorlabs stage is connected, then execute the movement script:
```bash
python movestage.py

### Calibration Results

<table>
  <tr>
    <td width="50%">
      <img src="[link-to-your-image-here.png](https://github.com/user-attachments/assets/deebf9b5-1222-413e-9fe7-f9971d6e63ca)" alt="Calibration Plots">
    </td>
    <td width="50%">
      <b>Force Calibration S-Curve (Top)</b><br>
      This graph demonstrates the raw positional response of the trapped particle as the piezo stage scans it across the laser's focal point. The steep central region crossing the zero-voltage difference mark represents the center of the optical trap.<br><br>
      <b>Gamma Factor Extractions (Middle & Bottom)</b><br>
      These plots isolate the central linear regime of the S-curve to compute the detector's spatial calibration factor, or gamma. The middle plot displays this extraction specifically for a ZnO nanoparticle with a sensitivity of 0.241 V/µm, whereas the bottom plot demonstrates a distinct extraction with a much steeper slope, yielding a sensitivity of 5.188 V/µm.
    </td>
  </tr>
</table>




