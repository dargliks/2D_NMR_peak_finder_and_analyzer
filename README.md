# 2D_NMR_peak_finder_and_analyzer

In protein NMR spectroscopy, our measurement data is usually a two-dimentional spectrum of frequencies, where the "peaks" in the spectrum correlate to the individual amino acids of the protein. Even after the initail assignment of each peak to its corresponding amino acid in the protein's sequence, even minute changes to the chemical environment (such as tiny fluctuations in temperature, pH level, salt concentration and other factors) or to the magnetic field of the experiment can affect the location of the peaks on the spectrum in each individual experiment. While large changes to the peaks' location ("chemical shift perturbations") or to their intensity (usually the integrated volume of the peak) are scientifically used to learn about the protein's structural dynamics in and its interactions with small molecules or other proteins, small changes can occur as part of normal experiment error. 

Therefore, every analysis of protein NMR data currently begins with adjusting the assigned peak list to align with the centers of the peaks in each individual experiment's spectrum and integrating the volume under them, prior to being able to compare the spectra and analyze the differences caused by our intended experimental variables. This is currently done manually, mostly peak-by-peak, and can take several hours for each spectrum. This tool is meant to automate as much of this process as possible, while flagging larger changes or discrepancies that require a human discretion. 

## 1. what does this project do?

This project takes a 2D protein NMR spectrum and finds all the maximum points that are higher than a defined threshold (peaks). It then compares this list of peaks to the assigned peak list for the given protein, and will generate a new peak list in which the name of each peak from the assigned list is given to the spectrum peak that has the smallest distance from it. The system will flag for human discretion any peaks that are moved more than a determined threshold in this process, as well as possible cases where two assignments are moved to the same peak in the spectrum. 

After aligning the assigned peaks to the spectrum, the project will integrate the volume under each peak and add the volume, as well as the peak height, to the peak list data. It can then run calculations comparing two such lists either in the locations of the peaks ("chemical shift perturbations") or in their relative intensity (calculated from peaks volume and/or height). 

## 2. input and output data

### expected inputs

This project will require two main inputs:

1. a 2D protein NMR spectrum - in the format of either Bruker, NMRPipe or Sparky.

2. a text file containing a peak list - most likely in Sparky's list format, though other formats may be accepted as well. 

The project may also require some manual input of parameters such as the acceptable thresholds for peak selection and for acceptable shift distance. 

### expected outputs

The primary output expected is a text file containing the new adjusted and integrated peak list - most likely in Sparky's list format. 

Further outputs may include CSV files containing the results of calculated comparisons between spectra, and PNG files plotting these calculations to the protein sequence. 

## 3. how to run this project?

### install this project

To install the project, clone this repository: https://github.com/dargliks/2D_NMR_peak_finder_and_analyzer.git

### install dependencies 

You can install the required dependencies using:

    pip install -r requirements.txt

This project requires the following packages to run:

* nmrglue
* numpy
* scipy
* matplotlib
* PANDAS

### run tests

The project will include automated tests for core logic. run them with
    pytest tests\

### run the project

run this project using
    python PeakFinder_main.py

## 4. course information

This project was written as part of the [WIS python programming course](https://github.com/Code-Maven/wis-python-course-2026-03/)
