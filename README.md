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

## Directory Structure
* `/src` - Python wrappers and automation scripts for the Thorlabs stages.
* `/analysis` - Calibration scripts for analyzing BFPI voltage signals and extracting trap stiffness.
* `/data_samples` - A small dataset of sample silica bead position data to test the calibration algorithms.

## Usage 
To run the automated calibration routine, execute the main script from the terminal:
```bash
python src/main_calibration.py

<img width="900" height="500" alt="Figure_forcecalibration001" src="https://github.com/user-attachments/assets/c5649334-9e14-4aa8-b5e7-f019a128f141" />

