""" Project pipelines """
from typing import Dict
from kedro.pipeline import Pipeline
from minipro.pipelines import data_preparation as dp
from minipro.pipelines import data_engineering as de
from minipro.pipelines import data_science as ds


def register_pipelines() -> Dict[str, Pipeline]:
    """
    Registers the project's pipelines
    Returns:
        A mapping from a pipeline name to a pipeline object.
    """
    data_preparation_pipeline = dp.create_pipeline()
    data_engineering_pipeline = de.create_pipeline()
    data_science_pipeline = ds.create_pipeline()
    return {
        "dp": data_preparation_pipeline,
        "de": data_engineering_pipeline,
        "ds": data_science_pipeline,
        "__default__": data_science_pipeline,
    }
