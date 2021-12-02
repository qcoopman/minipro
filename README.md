# minipro

## Overview

## Structure of the code
The structure of the code in this repo is based on the [cookiecutter](https://drivendata.github.io/cookiecutter-data-science/) model.
```
├── README.md          <- Top-level README for developers using this project
├── data/              <- Can be used to store local project data (not commited to version control)
├── docs/              <- Project documentation
├── conf/              <- Project configuration files
│   ├── base/          <- Bottom-level configuration environment to be shared by all developers
│   ├── local/         <- Configuration environment that should never be committed to version control:
|                             its purpose is to contain values that are specific to a local development machine
├── logs/              <- Project output logs (not commited to version control)    
├── notebooks/         <- Project related Jupyter notebooks (can be used for experimental code before moving the code to `src`). 
|                            Naming convention is a number (for ordering), the initials of the creator, and a short `-` delimeted description
│                            Examle: `1.0-qc-initial-data-exploration`.
├── requirements.txt   <- Requirements file for the project
├── src/               <- Project source code
|   ├── tests/         <- Tests
├── setup.cfg          <- Configuration options for `kedro test` and `kedro lint`
├── .coveragerc        <- Configuration file for the coverage reporting when doing `kedro test`
├── .ipython           <- IPython startup scripts
├── .gitignore         <- Prevent staging of unnecessary files to `git`
├── pyproject.toml     <- Identifies the project root and contains [configuration information](https://kedro.readthedocs.io/en/latest/11_faq/02_architecture_overview.html#kedro-yml)
```

## Usage

You can run your Kedro project with:
```
kedro run
```

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. 
You can run your tests as follows:
```
kedro test
```
