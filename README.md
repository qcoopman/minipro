# minipro

## Overview
The thermodynamic phase transition of clouds is still not well understood, therefore, the partitioning of ice and liquid in mixed phase clouds is often misrepresented in numerical models. 
Clouds processes represent the highest incertitude in current models to predict the future climate so the effects of cloud thermodynamic phase are important to determine the amplitude of global warming.
We use 12 years of cloud observations from the geostationary Spinning Enhanced Visible and InfraRed Imager (SEVIRI), CLAAS-2 dataset (https://doi.org/10.5676/EUM_SAF_CM/CLAAS/V002), over the Southern Ocean to detect clouds which contain both liquid and ice pixels at their tops and we retrieve microphysical and radiative properties in each cloud object. We collocate cloud properties with meteorological parameters from reanalysis from ERA-5. 
The project analyse the distribution of pockets of liquid and ice within mixed-phase clouds via a gradient boosting regression tree method. The study aims to understand which parameters potentially impact the formation and multiplication of ice pockets when clouds transition from liquid to ice.

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
