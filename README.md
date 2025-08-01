# amiet-self-noise
ciao
## Airfoil trailing edge noise computation code. GMC729 final project

This code implements the Amiet model for airfoil trailing edge noise prediction, based on measured or simulated turbulent boundary layer statistics. The user should provide all input statistics in a `.h5` file, containing a `f` field for the acquisition frequencies, `phi_pp` for the pressure spectrum $\Phi_{pp}$, `coherence` for the span-wise coherence length $\ell_y$, and `u_c` for the convection velocity $U_c$. All these fields mush be one dimensional arrays. HDF5 (`.h5`) files are preferable to other types of files, like `.txt` files, for numerous reasons. First, they are binary files, so they are more compact, especially when the data size gets large. Secondly, they allow to store meta-data along with the actual data, which can be extremely important if the original files will be reused in the future. Finally, they make you look like a pro, without being more difficult to read or write from any programming language (like python).

## Get the software
Go into the project folder in your pc and type:
```
git pull origin main
```
If ever your pc doesn't know what origin is, just type:
```
git remote add origin https://github.com/enricofoglia/amiet-self-noise.git
```

## Building the documentation
You can build an html version of the documentation by typing in a terminal:
```
cd docs
make html
```
and the opening ``docs/build/html/index.html`` in any browser.

## Possible features
1. We can implement a data processing module if the user has only time measurements at different microphones.
2. We can implement a data visualization module.

## ✅ Git Branch & Pull Request Checklist

### 🏗️ Before Starting a Branch
- [ ] Pull the latest `main` branch  
  `git checkout main && git pull origin main`
- [ ] Create a new branch with a descriptive name  
  `git checkout -b feature/your-task-name`

---

### 🧑‍💻 While Working on the Branch
- [ ] Keep changes focused on **one feature or fix**
- [ ] Avoid unrelated "quick fixes" — make a note and do them later
- [ ] Commit frequently with meaningful messages:
  - `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, etc.
  - Example: `feat(auth): add GitHub OAuth login`
- [ ] Run and test your code locally before pushing

---

### 🔄 Before Pushing or Opening a PR
- [ ] Merge latest `main` into your branch  
  `git fetch origin && git merge origin/main`
- [ ] Resolve any conflicts cleanly
- [ ] Push your branch  
  `git push origin feature/your-task-name`

---

### 🚀 Creating a Pull Request
- [ ] PR title is clear and describes the purpose (avoid vague titles)
- [ ] Description explains what was changed and why
- [ ] Screenshots or GIFs included if UI is affected
- [ ] Linked to relevant issues or tasks (e.g., `Closes #42`)
- [ ] Add reviewers or labels (if in a team)

---

### 🧹 After PR is Merged
- [ ] Delete the feature branch (on GitHub or via `git push origin --delete`)
- [ ] Pull the updated `main` to your local  
  `git checkout main && git pull origin main`

---

### ✨ Pro Tips (Optional)
- Use `draft` PRs if work is still in progress
- Use `squash & merge` to keep commit history clean
- Tag releases with version numbers for important milestones

