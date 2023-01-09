# pc4rules

Prototyping "rules" modeling for PhysiCell.

The rules consist of a constrained grammar:
```
signal{Y} promotes/inhibits/is neutral to {behavior} in cell type{X}

{X}, {behavior}, {Y}, ...
```
or,


e.g.,

tumor cell: oxygen increases cycle entry from 1.7e-05 towards 0.0007 with a Hill response, with half-max 21.5 and Hill power 4.

Compile (all provided sample models), copy the executable(s) you want to run to the root directory, run the Studio:
```
cd pc4rules/src
make

# move the executables into the root folder
mv biorobots ..
mv celltypes ..
mv pred_prey ..
mv interactions ..

# Change directory to the root dir and run the GUI from there
cd ..
python bin/pmb.py --studio --rules -c data/rules_model1.xml

(previously/future simplify: python bin/studio.py)
```

In the Studio:
* select the model to test from the `Model` menu
* in the Run tab, click `Run Simulation`. Note: on nanoHUB, the simulation is run *from* the `tmpdir` directory and that's where all output files will be written.
* in the Plot tab, click `Play`.
* edit params if you want then repeat: Run, Play.
