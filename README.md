# amiet-self-noise 🔊:
## Airfoil trailing edge noise computation code. GMC729 final project

This code implements the Amiet model for airfoil trailing edge noise prediction, based on measured or simulated turbulent boundary layer statistics. The user should provide all input statistics in a `.h5` file, containing a `f` field for the acquisition frequencies, `phi_pp` for the pressure spectrum $\Phi_{pp}$, `coherence` for the span-wise coherence length $\ell_y$, and `u_c` for the convection velocity $U_c$. All these fields mush be one dimensional arrays. HDF5 (`.h5`) files are preferable to other types of files, like `.txt` files, for numerous reasons. First, they are binary files, so they are more compact, especially when the data size gets large. Secondly, they allow to store meta-data along with the actual data, which can be extremely important if the original files will be reused in the future. Finally, they make you look like a pro, without being more difficult to read or write from any programming language (like python).

## Get the software
Go into the project folder in your pc and type:
```
git pull origin main
```
If prompted to write a commit message, modify the default text (if you want) and then type:
```
<Esc>
:wq
```
to save and quit the editor (the editor is called ``vim``).

If ever your pc doesn't know what origin is, just type:
```
git remote add origin https://github.com/enricofoglia/amiet-self-noise.git
```

## Building the documentation 📑:
You can build an html version of the documentation by typing in a terminal:
```
cd docs
make html
```
and the opening ``docs/build/html/index.html`` in any browser.

## Contribute to the project 🚧:
To contribute to the project, you need to follow these five steps:

✳️: Synchronize your fork (your github version of this repo) with my, original repo (to be done in github).

✳️: Copy the content of your repo to your computer, by running:
   ```bash
   git pull origin main
   ```
   in the GIT app.
 
✳️: Work on your local files. Please try to work on new files, or tell me if you need to modify any existing file.

&nbsp;&nbsp;&nbsp;✴️: You can "save" your progress by running:
    
  ```bash
  git add .
  git commit -m "A nice commit message"
  ```
&nbsp;&nbsp;&nbsp;it the GIT terminal. This preserves the history of all modifications on your *local* machine.
  
&nbsp;&nbsp;&nbsp;✴️: It is good practice to only work on specific branches, instead of the main branch. This is a way to keep your modifications separate from the "definitive" code until you know everything works fine. To create a new brach, use:
  ```bash
  git checkout -b [new-branch-name]
  ```
&nbsp;&nbsp;&nbsp;you will be now working on a new branch called ``new-branch-name``. To see a list of all the branches you have, use ``git branch`` and use ``git checkout [branch-name]`` to switch to the branch called ``branch-name``.
  
✳️: Put your local modification on your github repo by running.
   ```bash
   git push origin [branch-name]
   ```
   This will synchronize your local and remote repositories, but I cannot see the progress you made yet.
   
✳️: In github, open a pull request by using the contribute button. Follow the instructions and leave a descriptive comment telling me what you have modified and why.

Now I will see that you want me to integrate some modifications to the code, I can review them and merge them into the main code. 

♻️: repeat these steps every time you work on the project. Remember to get my modifications before starting to work on yours, or you might modify something that I have already changed on my side!

## Bash 101
Useful commands are:
```bash
# Move to the location 'path/to/something'
cd path/to/something
# See where you are
pwd
# See what's up where you are
ls [path]
```

## Possible features
1. We can implement a data processing module if the user has only time measurements at different microphones.
2. We can implement a data visualization module.



