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
mv rules_model ..

# Change directory to the root dir and run the Studio from there
cd ..
python bin/studio.py
```

In the Studio:
* in the Run tab, click `Run Simulation`. Note: in previous releases, we tried to follow the nanoHUB workflow whereby output was forced to be written to `tmpdir` (and that's where the executable was run from). Now we follow a workflow that focuses on running from your own computer and therefore allow for any output `folder `.
* in the Plot tab, click `Play`.
* edit params if you want then repeat: Run, Play.
