""" Data engineering pipeline """
from kedro.pipeline import Pipeline, node
from .nodes import split_data


def create_pipeline(**kwargs):
    """
    Creates data engineering pipeline
    Returns:
        A pipeline object containing all of the nodes that make it up
    """
    return Pipeline(
        [
            node(
                split_data,
                inputs=["P_clouds", "params:tst_data_pct"],
                outputs={
                    "x_trn": "P_clouds_trn_x",
                    "x_tst": "P_clouds_tst_x",
                    "y_trn": "P_clouds_trn_y",
                    "y_tst": "P_clouds_tst_y",
                },
                name="split_data",
            )
        ]
    )
