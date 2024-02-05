# Meeting Notes

## Meeting 1/30

* Where should the grid be centered?
* Look into what the difference between adding all hydrogens vs only polar
* Check if vina takes .gpf

* Inertial Tensor
    Its a 3x3 matrix. Read up later.

# Terminal Basics

## Basic Commands 

There are several key commands to know in order to effectively navigate the machine.

`ls`: show all files in current directory  
 `ls -a`: show all files + hidden files
    
`cd` : change directory (standard is to home)

`pwd` : get current working directory pathway

`pwd|pbcopy` : copy working directory to clipboard

`cp` :copy
`cp -r`: recursive copy

## VI

Vi is a text editing software for unix. We can use this to easily view files and make changes within terminal. 

shift + " + * + y

### Key Commands

`vi [Filename]` -- Write or edit a file in terminal

i (key): enable insert mode, allows changes to be made to file
* 0 (key): start of line
* $ (key): end of line
    
`:w` -- Write (save) changes

`:q` -- Quit file

`:wq` -- Write and Quit

## SSH

Secure Shell (SSH) is a cryptographic method we use in order to do remote logins to servers and command-line work. 

### Basics of SSH

To SSH into something: `ssh [Username]@[Link]`

To leave an SSH Connection: `exit`

** My username is maunger **


### Setting up SSH Shortcut

Typing in the previous command can be really tedious and frustrating, so what we can do is create a shortcut such that we only have to type ssh xyz in order to enter the machine

1. Go to home directory and do `cd ~/.ssh`. This will take you into your ssh directory

2. `vi config` -- This will enable you to edit the configuration for your ssh

3. Do the following in the document
    ```
    Host scotch
        Hostname [url to server]
        User [username]
    ```
4. Generate an rsa key `ssh-keygen -t rsa`
5. Copy and put it into id_rsa.pub

# PyMol

# Autodock Tools

## Preparing the Receptor 

There are two things that need to be done in order for the receptor to be ready for docking:

1. We need the file format to be .pdbqt
    * PDBQT File is a modified version of a PDB file that contains columns with the partial charge (Q) of each atom as well as the AutoDock type for each atom (T). This is literally seen in the name, it is a PDB file with QT.
    
    * Autodock Atom Types (T): These are pre-defined atom types within autodock. The type that a particular atom is assigned will help the program decide what the chemical interactions with the environemnt will be
    
    * PDBQT files are necessary in order to be able to do molecualr docking. If you don't have a PDBQT file, the software can't properly assess charge interactions and find the best fit.  

2. We need a grid box to where we want the docking to be done
    * Assuming we aren't doing blind docking and we have a region that we want to target on the molecule, we need to determine the coordinates of the region to where the program will be. 


## Generating a PDBQT File in AutoDock Tools

Assuming you have imported your protein:

1. Remove Waters (edit > delete water)
2. Add Hydrogens (edit > hydrogens > add > polar hydrogens, noBondOrder, yes)
    * What is the effect of adding all hydrogens, not just polar ones?
     
3. Assign Autodock Element Field (edit > atoms > assign AD4 type)
4. Compute Gasteiger Charges (edit > charges > compute Gasteiger)
5. Save file (file > save > write PDBQT)
    * Be sure you add .pdbqt to the end 

## Establishing the Grid


## .gpf file format

* Explain this/put picture here

# Git

## Initializing a Repository (Command-Line Approach):

1. Create file on your machine that you want to use as the repo
    * Make sure you are cd'd into it
    * Put a file in (either vi or create some kind of file)
2. Create repository on github, obtain link
3. Return to terminal, do the following
    * `git init`
    * `git remote add origin [URL]`
    * `git add .`
    * `git commit -m "[some message]"`
    * `git push -u origin main`

## How to get around using a git token repeatedly

For this project, token: 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

Once you have initialized your repo and done your initial commit using a personal token, run the following command and it will bypass you having to re-enter credentials:

```
git config --global credential.helper manager
```

## Removing a File From Git

1. Ensure you are in your git repository
2. `git rm [filename]`
3. `git commit -m "[message]"`
4. `git push origin main`

# Pod

`echo`: print 

If you just type in command like vina ..., you will run on the head node

Always write a 

`sbatch [filename]`: this is the command to submit a job in pod
Head Node: This is where you put files, make text edits -- it is realy only to delegate tasks and organize

`squeue -u maunger`: this is how you monitor your progress

    R: Running
    PD: Pending
    CG: ?

* You never want to run a job too long on the head node

Pod uses linux, so use that installer for vina

scp [filename] pod:~

Create bashrc for pod with important aliases
Do some scripting

Do some reading,
script out using vina_split into mulitple jobs
optimal number of processors per job
Reading about how to get multiple computers to do jobs

See how much slower flexible side chains are

Autodock command (so I don't have to retype)

vina_split --receptor tauSLS.pdbqt --ligand JJEBML.xaa.pdbqt --center_x 179.991 --center_y 178.728 --center_z 172.492 --size_x 19.1166666667 --size_y 20.3416666667 --size_z 31.35

Access:

username: munger
password: accessCluster@93117