""" Data preparation pipeline """
from kedro.pipeline import Pipeline, node
from .nodes import preprocess

def create_pipeline(**kwargs):
    """
    Creates data preparation pipeline
    Returns:
        A pipeline object containing all of the nodes that make it up
    """
    return Pipeline(
        [
            node(
                preprocess,
                inputs=["params:raw_data_dir"],
                outputs="P_clouds",
                name="preprocess",
            )
        ]
    )
