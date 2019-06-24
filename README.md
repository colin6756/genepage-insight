# genepage-insight

## Overview
The instructions below provide users with a copy of this program which can be directly used or adapted for their own project. The program require 2 plain text files, one containing a list of geneIDs and the other with a list of keywords describing the phenotypes the user suspects the genes have influence over. The script can work for either rice, wheat or arabidopsis.

The tabular output would provide the users with the chromosome and start position for every gene, a knetscore which assesses the relevance of each gene to the specified phenotype or phenotypes and a Knetminer genepage url per gene.
The url leads the user into Knetminer's network view which accelerates research by outlining orthology of the gene as well as traits and publications related to it.

#### Prerequisites
* The script can run on any computer with access to Python2.7 and above or any versions of Python3. 

* The program does not require heavy computational resources. However, as the user may prefer high performance computing the instructions on how to set up and run the program on a node managed by the Easybuild framework has been included below. The User should read set up instructions specific to any other HPC frameworks.

* Python virtual environments, e.g. virtualenv for python2 or pyvenv for python3. If the user does not have root permission on Easybuild a virtual environment is required for installation of numpy and pandas through pip. See **3. Installing requests** in **Instructions** on how to do this.

## Tutorial and usage instructions
This is a quick tutorial to get the user started by reproducing the outputs of map_snp_to_gene_vEN.py for 2 different GWAS output spreadsheets, GAPIT.MLM.DTF.GWAS.Results.csv and GAPIT.MLM.blupWidth.GWAS.Results.csv as seen in the 2 directories of the same names. The tutorial generally assume the user is using linux managed by Easybuild.

#### 1.Downloading the repository
Clone this repository with the GitHub URL using either Git or a Git GUI. The user should obtain a directory named gwas-gene-discovery containing identical contents to the GitHub repository.

#### 2. Accessing compute node on Easybuild
The user can check available compute nodes by the command:
```
sinfo 
```
If available, login to a standard compute node on Rothhpc4 using:
```
srun --pty bash -i
```

#### 3.Setting up a virtual environment on Easybuild
A virtual environment is required for pip installation of numpy, pandas and requests.
Check all the available versions of python currently on cluster:
```
module avail Python
```
Afer a Python2.7 and above or Python3 version has been selected either edit the sbatch script in this repository, virtualenv_setup.sbatch or execute the commands below.

```
module load <Python version>
virtualenv <name of Python virtual environment>
source </path to env>/bin/activate/
```
The user can return to the virtual environment in a new session after logging out by:
```
module load <Python version>
source </path to env>/bin/activate/
```
  
#### 4.Installing python request library
Requests is needed for the steps that send HTTP request protocols found in the script while Numpy and Pandas are required for obtaining information from Kentminer API. Use pip to install the following library:
```
pip install requests
pip install pandas
pip install numpy
```

#### 5.Execution of script
The command:
```
python genepage_insight.py -h
```
Returns the usage of the script as the following:
```
usage: genepage-insight.py [-h] file list species
```
The **mandatory arguments** are:
* File. A spreadsheet containing the results of GWAS analysis. The fields of spreadsheet should be arranged in the order below as the script was originally designed for GAPIT software outputs (examples being 2 csv files in repository).:

SNP [integer], Chromosome [integer], Position [integer], P.value [float]

* List. A plain text file containing one or more short description of the phenotype or phenotypes genes of interest are suspected to influence. The keywords should be vertically listed line by line. An example list, mock_keyword_list.txt can be found in the repository.

* Species. The species of organism subjected to gwas which the script will return gene IDs specific to. The options are currently 3 species represented by an integer value as shown below:


     * 1 represents rice
     * 2 represents wheat
     * 3 represents arabidopsis

If the User has either a standard or Easybuild terminal set up with requests installed, they can run the following command. This will reproduce the directories: ./example_list which contains a tabular txt file summarising the Knetminer findings on genes provided.

```
python map_snp_to_gene_vEn.py GAPIT.MLM.DTF.GWAS.Results.csv mock_keyword_list.txt 1
```
```
python map_snp_to_gene_vEn.py GAPIT.MLM.DTF.GWAS.Results.csv mock_keyword_list.txt 1
```

#### 6. Output information



## External tools included


Knetminer



## Authors
Keywan-Hassani Pak


Colin Li



## Acknowledgement

Knetminer


Rothamsted Resarch
