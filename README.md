![CI](https://github.com/KatyBrown/CIAlign/actions/workflows/main.yml/badge.svg)
# CIAlign
CIAlign documentation is now available via [ReadTheDocs](https://cialign.readthedocs.io/en/latest/)

## Installation

**Requirements**

* python >= 3.6
* matplotlib >= 2.1.1
* numpy >= 1.16.3
* scipy >= 1.3.0

The easiest way to install CIAlign is using conda or pip3.

**Conda**

`conda install -c bioconda cialign`

[link](https://anaconda.org/bioconda/cialign)

**pip3**
`pip3 install cialign`

[link](https://pypi.org/project/cialign/)

**Download**
The current release of CIAlign can also be downloaded directly using [this link](https://github.com/KatyBrown/CIAlign/releases/latest),

If you download the package directly, you will also need to add the CIAlign directory to your PATH environment variable as described [here](https://gist.github.com/nex3/c395b2f8fd4b02068be37c961301caa7)

## Summary
CIAlign allows the user to:


**Clean**

* Remove sources of noise from an MSA 
  * Remove sequences above a threshold level percentage of divergence from the majority.
  * Remove insertions which are not present in the majority of sequences.
  * Crop poorly aligned  sequence ends.
  * Remove short sequences below a threshold number of bases or amino acids.
  * Remove columns containing only gaps.
  * Remove either end of an alignment where columns don't meet a minimum identity threshold and coverage level.

**Visualise**

* Visualise alignments.
  * Generate image files summarising the alignment.
  * Label these images to show how CIAlign has affected the alignment.
  * Draw sequence logos
  * Plot alignment statistics - visualise coverage and conservation at each position in the alignment.


**Interpret**

* Generate consensus sequences.
* Generate position frequency, position probability and position weight matrices
* Format these matrices to be used as input for the BLAMM and MEME motif analysis tools.
* Generate a similarity matrix showing the percentage identity between each sequence pair.
  
**Edit**

* Extract a section of the alignment.
* Unalign the alignment.
* Replace U with T, or T with U in a nucleotide alignment.

CIAlign is designed to be highly customisable, allowing users to specify exactly which functions to run and which settings to use.

It is also transparent, generating a clear log file and alignment markup showing exactly how the alignment has changed and what has been removed by which function.

## Citation
If you found CIAlign useful, please cite: 

Tumescheit C, Firth AE, Brown K. 2022. CIAlign: A highly customisable command line tool to clean, interpret and visualise multiple sequence alignments. PeerJ 10:e12983 https://doi.org/10.7717/peerj.12983

## Mailing List
Sign up here for updates when a new feature is added to CIAlign 

