# pc4rules

Prototyping "rules" modeling for PhysiCell.

The rules consist of a constrained grammar:
```
signal{Y} promotes/inhibits/is neutral to {behavior} in cell type{X}

{X}, {behavior}, {Y}, ...
```
or, e.g.,

"tumor cell: oxygen increases cycle entry from 1.7e-05 towards 0.0007 with a Hill response, with half-max 21.5 and Hill power 4"


Compile, move the executable, run the Studio:
```
cd pc4rules/src
make

# move the executable into the root folder
mv rules ..

# Change directory to the root dir and run the Studio from there
cd ..
python bin/studio.py
```

In the Studio:
* in the Run tab, click `Run Simulation`. Note: both locally and on nanoHUB, the simulation is run *from* the `tmpdir` directory and that's where all output files will be written. The `tmpdir` is also where the [edited] config file is copied and renamed `config.xml`. Therefore the original config file needs to specify the save output folder is "."
* in the Plot tab, click `Play`.
* edit params if you want then repeat: Run, Play.
