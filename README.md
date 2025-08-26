# Dynamic nanoscale architecture of synaptic vesicle fusion in mouse hippocampal neurons

This repository holds the codes used for analyzing the mesoscopic simulations the synaptic vesicle docking.

The following Jupyter notebooks are provided:

 - ```docking_kinetics.ipynb``` for the analysis of docking kinetics, as shown in Supplementary Fig. 8 of the paper.
 - ```docking_morphology.ipynb``` for visualizing different membrane morphologies during the docking procedure, as shown in Fig. 3 of the paper.
 - ```synaptic_vesicle_MSM.ipynb``` for building Markov State models, based on the number of observations in the cryo-EM images.

The notebooks also contains the code to automatically download simulation trajectories from the online repository.

In addition to the Python Standard Library, the notebook depends on local installations of packages listed in the ```requirements.txt``` file.

You can install all the required dependencies by simply running 

```pip install -r requirements.txt```

from your local python environment.

We recommend making a conda environment for installing all the necessary components and running the notebook. See <a href="https://docs.conda.io/en/latest/miniconda.html">https://docs.conda.io/en/latest/miniconda.html</a> for instructions.

## Reference
[1] J. Kroll, U. Kravčenko, M. Sadeghi, C. A. Diebolder, L. Ivanov, M. Lubas,  T. Sprink,  M. Schacherl,  M. Kudryashev,  C. Rosenmund “<a href = "https://doi.org/10.1101/2025.02.11.635788">Dynamic nanoscale architecture of synaptic vesicle fusion in mouse hippocampal neurons</a>”, _bioRxiv_ (2025) 635788.
		

