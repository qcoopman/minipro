""" Project pipelines """
from typing import Dict
from kedro.pipeline import Pipeline
from minipro.pipelines import data_preparation as dp

def register_pipelines() -> Dict[str, Pipeline]:
    """
    Registers the project's pipelines
    Returns:
        A mapping from a pipeline name to a pipeline object.
    """
    data_preparation_pipeline = dp.create_pipeline()
    return {
        "dp": data_preparation_pipeline,
        "__default__": data_preparation_pipeline,
    }
