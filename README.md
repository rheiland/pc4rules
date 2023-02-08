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
python bin/studio.py -e rules_model
```

In the Studio:
* in the Run tab, click `Run Simulation`. Note: in previous releases, we tried to follow the nanoHUB workflow whereby output was forced to be written to `tmpdir` (and that's where the executable was run from). Now we follow a workflow that focuses on running from your own computer and therefore allow for any output `folder `.
* in the Plot tab, click `Play`.
* edit params if you want then repeat: Run, Play.

## Python Dependencies

The studio requires an installation of python. There are a few python dependencies for the studio to work, listed in `requirements.txt`. 

You can set up a virual environment to resolve these dependencies.  The following commands (assuming python is already installed) will install the [`virtualenv`](https://virtualenv.pypa.io/en/latest/) python module and activate it.

First install the `virtualenv` module.
```
$ python -m pip install virtualenv
```

Then make sure you are in the `pc4rules` root directory and enter the following commands to set up and activate your virtual environment.
```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ 
```

* **Note**: `venv` is just the name of the virtual environment in this example, you can name it whatever you want.

To actually install the dependencies in your virtual environment, next use the following command:
```
pip install -r requirements.txt
```

After doing this, you should be able to launch the studio.  You can exit the virtual environment by saying `deactivate`.