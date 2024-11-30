# Gnina Docking Project

## Introduction and Background
The goal of this project was to identify small-molecules capable of binding to a hydrophobic region on the tau
fillament involved in progressive supranuclear palsy (PSP) identified through molecular dynamics simulations.

Below is an image of our target fillament, the red region on the top is the targeted hydrophobic region. 
<img width="496" alt="Screenshot 2024-11-30 at 1 56 57 PM" src="https://github.com/user-attachments/assets/7d30a5ad-f5f5-43c3-b1fe-12c7046b7cd0">

## Softwares

* Autodock Tools 4.0 - used to get coordinates of binding site on receptor
* Autodock Vina - used to split PDBQT files from ZINC and dock them onto the receptor
* Docker - necessary to run a containerized version of Gnina
* Gnina - used to score docked ligands from autodock vina
  * Gnina could be used for the entire process, eliminating the need for Autodock Vina. With the resources we had available, we decided to
    use Autodock Vina because it runs on CPUs. This shortened the time needed for the overall process. 

## Python Packages
* Numpy
* Pandas
* OpenBabel
  * Necessary for condensing docked PDBQT files from Autodock Vina into mol2 files for each tranche
  * Make sure openbabel is installed both on the machine as well as the corresponding python package
    
## Main Scripts and Workflow

**Note:**  *All main and supporting scripts are found in the `workingCode` directory. The `oldCode` directory is simply an archival directory with scripts no longer serve a purpose for the workflow.*

1. `vinaSplit1000.py`
     * First it will split all tranche.xaa files contained in the directory specified by the `trancheXAAOrigin` variable into individual ligand.pdbqt files
       contained within directories for their respective tranches. These directories will all be contained within the path specified by `trancheOutput`.
       If a tranche has more than 1000 ligands, this script will automatically create sub-directories of 1000 or less compounds. This feature was implemented
       due to constraints that will be explained in the second step. 
     * After splitting, the script will move all the tranche.xaa files into the directory defined under `trancheXAAOut`
     * Finally, the script will write a file called `ligandData.csv`. This csv file contains information about each ligand, like its tranche, file name, and
       most importantly, a pathway to what the docked ligand file for that compound will be. This is used in step 2. Every docked ligand from this step will be
       saved in a directory with the original sub-directory name plus _OutFiles. 
       
2. `submitJobs.py` 
     * The goal of this script is to write a shell script for each sub-directory of each tranche that will run an array of jobs. The exact number of jobs that
       the script for a sub-directory runs is determined by the number of ligands within the sub-directory. Each job is an Autodock Vina call on one ligand within
       the sub-directory. Since we had a limit of 1000 jobs in an array, our directories could be not exceed 1000 compounds. 
     * The shell script written is called `submissionScript.sh`. As mentioned above, this script is updated and submitted for each sub-tranche.
     * The data for the specific ligand pathway and out pathway used during any given run of an array job is found in `ligandData.csv`. 
    
3. `condenseFiles.py`
     * This script was written to go through each subtranche, delete the undocked tranche files, then merge all files within a subtranche into a single .mol2 file
       that can be transfered to the system that will be running the Gnina software. Ideally, the docked and undocked files will be in separate directories, however
       in the event that they aren't, this script has been written to stop deleting a sub-directory.
     * Each function in this script has several checkpoints defined by boolean values that need to the correct value. This is done to ensure that there are no files
       lost or mistakes that can be propogated further without the knowledge of the user. Errors in this step of the process can result in uncertainty about what
       compounds or tranches were complete, leading to time being wasted on manually checking files.
     * The final function in this script, `zipPDBQTS` is important both as a checkpiont and part of the final data collection process. This function puts all the
       docked pdbqt files into a zip file, which will both save them should anything go awry later on as well as minimize the amount of space they take up. In the
       last step of this process, these files will need to be referenced to obtain the smiles representation for each compound.

4. `gninaPrep.py`
     * This writes a CSV with the path to each mol2 file in it. The file is called `mol2Data.csv`. This step is necessary so that a script can iterate through the
       paths and call Gnina on each.
      
5. `gninaScript.py`
     * This will call Gnina on every mol2 file listed in `mol2Data.csv`.

6. `scoreCSVGenerator.py`
     * This script contains a series of functions which isolate scores for each ligand being screened from the output of running Gnina. It will also use the zipped            ligand pdbqt files to find the SMILES representation for each ligand. It will compile all of this information into a single CSV file that can be used for               further analysis. 

## Supporting Scripts

 * In practice, `vinaSplit1000.py` was run using the `splitScript.sh` shell script.
 * `submitJobs.py` is run using the script `submit.sh`
 * `listDirectory.py` was written to help keep track of tranches that had been completed and those that still needed to be screeened.
 * `zipMol2.py` was written to zip all mol2 files and aid in transfer between clusters
 * `moveZips.py` is used to transfer zips to a new directory
   
## Acknowledgments

### People
* Sam Lobo
* Andrew Longhini
  
### Labs
* [Kosik Lab](https://ken-kosik.mcdb.ucsb.edu)
* [Shea Group](https://labs.chem.ucsb.edu/shea/joan-emma/)
* [Shell Lab](https://theshelllab.org)
  
### Resources and Publications
* [ZINC](https://zinc.docking.org) - Small molecule database
* [UCSB CNSI](https://www.cnsi.ucsb.edu) - Computing Resources
