""" Data science pipeline """
from kedro.pipeline import Pipeline, node
from .nodes import train_model, predict_and_evaluate


def create_pipeline(**kwargs):
    """
    Creates data science pipeline
    Returns:
        A pipeline object containing all of the nodes that make it up
    """
    return Pipeline(
        [
            node(
                train_model,
                inputs=["P_clouds_trn_x", "P_clouds_trn_y", "params:model"],
                outputs={"model": "model"},
                name="train",
            ),
            node(
                predict_and_evaluate,
                inputs=["P_clouds_tst_x", "P_clouds_tst_y", "model"],
                outputs={
                    "chart_feat_importance": "chart_feat_importance",
                    "chart_var_correlation": "chart_var_correlation",
                },
                name="predict_and_evaluate",
            ),
        ]
    )
