# 2D_NMR_peak_finder_and_analyzer

In protein NMR spectroscopy, our measurement data is usually a two-dimentional spectrum of frequencies, where the "peaks" in the spectrum correlate to the individual amino acids of the protein. Even after the initail assignment of each peak to its corresponding amino acid in the protein's sequence, even minute changes to the chemical environment (such as tiny fluctuations in temperature, pH level, salt concentration and other factors) or to the magnetic field of the experiment can affect the location of the peaks on the spectrum in each individual experiment. While large changes to the peaks' location ("chemical shift perturbations") or to their intensity (usually the integrated volume of the peak) are scientifically used to learn about the protein's structural dynamics in and its interactions with small molecules or other proteins, small changes can occur as part of normal experiment error. 

Therefore, every analysis of protein NMR data currently begins with adjusting the assigned peak list to align with the centers of the peaks in each individual experiment's spectrum and integrating the volume under them, prior to being able to compare the spectra and analyze the differences caused by our intended experimental variables. This is currently done manually, mostly peak-by-peak, and can take several hours for each spectrum. This tool is meant to automate as much of this process as possible, while flagging larger changes or discrepancies that require a human discretion. 

## 1. what does this project do?

This project is meant to 




## 2. input and output data

### expected inputs

### expected outputs

## 3. how to run this project?

### install this project

To install the project, clone this repository: https://github.com/dargliks/2D_NMR_peak_finder_and_analyzer.git

### install dependencies 

You will need the following dependencies to run this project:

* nmrglue
* numpy
* scipy
* matplotlib
* PANDAS

### run tests

### run the project

## 4. course information

This project was written as part of the [WIS python programming course](https://github.com/Code-Maven/wis-python-course-2026-03/)
