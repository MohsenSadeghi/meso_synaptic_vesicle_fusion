# Dynamic nanoscale architecture of synaptic vesicle fusion in mouse hippocampal neurons

This repository holds the codes used for analyzing the mesoscopic simulations the synaptic vesicle docking.

The following Jupyter notebooks are provided:

 - ```data_preprocessor.ipynb``` this notebooks contains code to automatically download simulation trajectories from the online repository and preprocess the data for further analysis. It should be run first. 
 - ```docking_kinetics.ipynb``` for the analysis of docking kinetics, as shown in Supplementary Fig. 8 of the paper.
 - ```docking_morphology.ipynb``` for visualizing different membrane morphologies during the docking procedure, as shown in Fig. 3 of the paper.
 - ```synaptic_vesicle_MSM.ipynb``` for building Markov State models, based on the number of observations in the cryo-EM images.

The notebooks are developed independent of the operating system, and you can run them with Jupyter server running under Linux, Windows, or macOS.

You can either download the contents of this repository (use the ```<> Code``` menu) or clone it using the command line:

```git clone https://github.com/MohsenSadeghi/meso_synaptic_vesicle_fusion.git```

In addition to the Python Standard Library, the notebooks depend on local installations of the following packages.
We have successfully tested them with the version numbers mentioned.
All the dependencies are listed in the ```requirements.txt``` file.

 | package    | version |
 |------------|---------|
 | numpy      | 2.3.2   |
 | scipy      | 1.16.1  |
 | matplotlib | 3.10.5  |
 | h5py       | 3.14.0  |
 | pandas     | 2.3.2   |
 | jupyter    | 1.1.1   |
 | tqdm       | 4.67.1  |
 | seaborn    | 0.13.2  | 
 | networkx   | 3.5     |

We recommend making a conda environment for installing all the necessary components and running the notebook.
See <a href="https://docs.conda.io/en/latest/miniconda.html">https://docs.conda.io/en/latest/miniconda.html</a> for instructions.
Whe you have conda installed, make new environment for running the notebooks:

```
conda create -n <your_conda_environment_name> python 
conda activate <your_conda_environment_name>
```
Then you can simply install all the required dependencies by running: 

```
pip install -r requirements.txt
```
All these installation steps, including cloning the repository, downloading and installing miniconda, and installing the required packages should take less than 15 min on a normal desktop computer.

After setting up your Python environment and having installed the requirements, you should start Jupyter from the folder containing the cloned repo and the notebooks:

```
cd <where_you_cloned_the_github_repo>
conda activate <your_conda_environment_name>
jupyter notebook
```
The notebooks themselves contain remarks and instructions about the code and the expected output.

You should start by running the ```data_processor``` notebook, otherwise other notebooks will throw an exception mentioning lack of data.
Running the ```data_processor``` notebook comprises downloading all the required data from the ```ftp``` server, and depending on the internet speed, can take several minutes.
Alternatively, you can manually download the files from ```https://ftp.mi.fu-berlin.de/pub/msadeghi/synaptic_vesicle``` and put a copy inside the ```trajectory``` folder. But you still need to run the ```data_processor``` notebook for processing data from the downloaded files.

Due to the large size of the trajectory data being loaded and processed, we recommend running the notebooks, as they are, on a machine with at least 20GB of free storage space and 16GB of RAM available. 

## Reference
[1] J. Kroll, U. Kravčenko, M. Sadeghi, C. A. Diebolder, L. Ivanov, M. Lubas,  T. Sprink,  M. Schacherl,  M. Kudryashev,  C. Rosenmund “<a href = "https://doi.org/10.1101/2025.02.11.635788">Dynamic nanoscale architecture of synaptic vesicle fusion in mouse hippocampal neurons</a>”, _bioRxiv_ (2025) 635788.

