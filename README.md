# minipro

## Overview
Scientists use numerical models to predict how the climate might change in the future, especially as human actions, like adding greenhouse gases to the atmosphere, change the basic conditions of our planet. Clouds have long been the biggest uncertainty in climate calculations. They can both shade the Earth and trap heat. Which effect dominates depends on their properties.

This project aims at developing a method to improve our understanding of the thermodynamic phase of mixed-phase clouds, cloud layers containing both liquid and ice water at sub-freezing temperatures. Twelve years of cloud observations from the geostationary space-based instrument Spinning Enhanced Visible and InfraRed Imager (SEVIRI) are collocated with information from the ERA-5 dataset that was compiled over the Southern Ocean. The resulting dataset contains radiative and microphysical cloud properties associated with meteorological parameters.

The distribution of liquid and ice pockets within mixed-phase clouds is analyzed through a gradient boosting regression tree (GBRT) method. Unlike linear models, decision trees have the ability to capture the non-linear interactions between training features and the target variable. As such, the relative impact of each parameter on the thermodynamic phase is highlighted. This work could potentially be used to improve climate models by providing new parametrizations to represent the thermodynamic phase of clouds.

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

## Pipelines

### Data preparation
This pipeline reads all data files from two data sources:  
1. Twelve years of cloud observations from the geostationary space-based instrument 
Spinning Enhanced Visible and InfraRed Imager (SEVIRI) collected over the Southern Ocean
2. Complimentary meteorological parameters from the ERA-5 dataset published by the
European Centre for Medium-Range Weather Forecasts (ECMWF)
The resulting dataset is then 
It also filters out malformed data points from the resulting dataset.

### Data engineering
This pipeline splits our resulting dataset into a train and a test set.

### Data science
This pipeline trains a XGBoost regression model with a train set, evaluates the trained
model and then uses it to make predictions in a test set. The hyperparameters used to 
train the model and the mean squared error computed during its evaluation are logged to
MLFlow, as well as two plots:
1. A feature importance plot for the trained XGBoost regression model
2. A variable correlation plot for the trained XGBoost regression model

## Usage

Run the Kedro project with:
```
kedro run
```

Run a specific pipeline with:
```
kedro run --pipeline name-of-the-pipeline
```
