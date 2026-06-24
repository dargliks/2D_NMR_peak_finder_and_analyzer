# 2D_NMR_peak_finder_and_analyzer

In protein NMR spectroscopy, spectra contain peaks corresponding to individual amino acids. Even after the initial assignment of each peak to its corresponding amino acid in the protein's sequence, small changes in the experimental conditions (such as tiny fluctuations in temperature, pH, salt concentration, magnetic field stability and others) can affect the positions of peaks in the spectrum in each individual experiment. While large changes to the peaks' positions ("chemical shift perturbations") or to their intensity are scientifically used to learn about the protein's structural dynamics and its interactions with small molecules or other proteins, small changes can occur as part of normal experiment error. 

Before spectra can be compared quantitatively, assigned peak lists must therefore be realigned to the observed peak positions in each spectrum. This process is often performed manually and can take hours for a single dataset.

This project automates that alignment process for 2D NMR spectra by refining peak positions within a configurable search radius, reporting alignment status, and identifying potential peak assignment collisions. The program also identifies cases where multiple assignments converge to the same spectral region, flagging potentially ambiguous assignments for manual review.

## 1. What does this project do?

This project takes an existing assigned peak list for a given protein and compares it to an experimental 2D NMR spectrum of the same protein. Using a limited search window and an iterative refinement algorithm, it aligns each peak to the highest-intensity point within a local region of the spectrum.

It returns an updated list of aligned peaks together with a status report that flags cases requiring user review, including peaks below an intensity threshold and peaks where the alignment failed to converge within the maximum number of iterations.

The program also checks for collisions, where multiple assigned peaks converge to the same spectral region, and flags these cases for manual inspection.

## 2. Input and output data

### Inputs

This project currently accepts two input files:

1. a 2D protein NMR spectrum - in UCSF format

2. a SPARKY-generated text file containing a peak list

Further optional inputs allow the user to adjust the default spectrum and alignment configurations, including applying a global PPM shift, adjust the permitted search radius/window and number of iterations for the alignment algorithm, and determine the accepted peak intensity threshold. 

### outputs

The project returns two outputs:

1. a SPARKY-compatible peak list file, containing the aligned positions of the peaks (peaks that failed to converge retain their original position, for user review).

2. a CSV report file, containing for each peak: 

    * its original and aligned positions,

    * a status indicating whether the peak:
        * converged successfully (CONVERGED)
        * converged but is below intensity threshold (LOW_SIGNAL)
        * failed to converge within the maximum number of iterations (FAILED_TO_CONVERGE)
    
    * a list of peaks occupying the same spectral region as it (collisions), where applicable

## 3. Project installation and usage

### Project installation

To install the project, clone this repository: https://github.com/dargliks/2D_NMR_peak_finder_and_analyzer.git

### Project dependencies

This project requires Python 3.10+, as well as the following packages:

* nmrglue
* numpy
* matplotlib (optional, used in dev_tools only)

You can install the required dependencies using:

    pip install -r requirements.txt


### run tests

The project includes a total of 30 automated tests for core logic. run them with:

    pytest tests\

### run the project

run this project using:

    python main.py

## 4. Future improvements

1. Multiple file format support - including bruker and NMRPipe spectrum files, and potentially additional peak list formats.

2. Improved alignment algorithm - allowing for candidate selection and scoring to identify larger shift in peak positions, rather than local refinement only.

3. Improved configuration settings:
    * Adjustment of default settings to further experiment types.
    * SNR-based, spectrum-specific intensity threshold determination.

4. Post-alignment analysis tools: 
    * peak volume integration. 
    * list comparison analyses, including chemical shift perturbations and intensity changes

5. Interactive GUI. 

## 5. AI usage disclosure

Parts of the software design, implementation, testing, debugging, and documentation were developed with assistance from OpenAI ChatGPT. All final code, design decisions, and  scientific validation were performed or reviewed by the project author.

## 6. course information

This project was written as part of the [WIS python programming course](https://github.com/Code-Maven/wis-python-course-2026-03/)


