# minipro

## Overview
Numerical models struggle to predict our future climate because clouds glaciate too efficiently in such a way that the partitioning of cloud thermodynamic phase is misrepresented in global climate models. The isotherms rise in a warming climate leading to a replacement of ice clouds by liquid clouds. This effect increases the reflectivity of clouds to sunlight since cloud droplets are smaller and more numerous than ice crystals for a fixed water content. This project aims for developing a method to improve our understanding on cloud thermodynamic phase partitioning within mixed phase clouds.

Twelve years of cloud observations from the geostationary space-based instrument Spinning Enhanced Visible and InfraRed Imager are collocated with reanalysis from ERA-5 over the Southern Ocean. The project focusses on mixed phase clouds so we only keep clouds consisting of both liquid and ice pixels. The dataset contains radiative and microphysical cloud properties associated with meteorological parameter.

The distributions of liquid and ice pockets within mixed phase clouds are analyzed through a gradient boosting regression tree method. The relative impact of each parameter on the thermodynamic phase distribution is highlighted considering non-linear relations. This work would potentially improve climate models by providing new parametrizations to represent the thermodynamic phase of cloud.   

## Structure of the code
The structure of the code in this repo is based on the [cookiecutter](https://drivendata.github.io/cookiecutter-data-science/) model.
```
├── README.md          <- Top-level README for developers using this project
├── data/              <- Can be used to store local project data (not commited to version control)
├── docs/              <- Project documentation
├── conf/              <- Project configuration files
│   ├── base/          <- Bottom-level configuration environment to be shared by all developers
│   ├── local/         <- Configuration environment that should never be committed to version control:
|                         its purpose is to contain values that are specific to a local development machine
├── logs/              <- Project output logs (not commited to version control)    
├── notebooks/         <- Project related Jupyter notebooks (can be used for experimental code before moving the code to `src`). 
|                         Naming convention is a number (for ordering), the initials of the creator, and a short `-` delimeted description
│                         Examle: `1.0-qc-initial-data-exploration`.
├── requirements.txt   <- Requirements file for the project
├── src/               <- Project source code
|   ├── tests/         <- Tests
├── setup.cfg          <- Configuration options for `kedro test` and `kedro lint`
├── .coveragerc        <- Configuration file for the coverage reporting when doing `kedro test`
├── .ipython           <- IPython startup scripts
├── .gitignore         <- Prevent staging of unnecessary files to `git`
├── pyproject.toml     <- Identifies the project root and contains configuration information
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
