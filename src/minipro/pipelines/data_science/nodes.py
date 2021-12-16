""" Nodes for the data science pipeline """
import time
import mlflow
import pandas as pd
from typing import Dict
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


def train_model(
    p_clouds_trn_x: pd.DataFrame,
    p_clouds_trn_y: pd.DataFrame,
    params: Dict[plt.figure, plt.figure],
) -> xgb.sklearn.XGBRegressor:
    """
    Train a XGBoost regression model
    Args:
        p_clouds_trn_x: Input variables of our train set
        p_clouds_trn_y: Variable to predict in our train set
        params: XGBoost regression model hyperparameters
    Returns:
        A trained XGBoost regression model
    """
    xgbr = xgb.XGBRegressor(
        n_estimators=params["n_estimators"],
        max_depth=params["max_depth"],
        learning_rate=params["learning_rate"],
        subsample=params["subsample"],
        colsample_bytree=params["colsample_bytree"],
    )
    xgbr.fit(p_clouds_trn_x, p_clouds_trn_y)
    score = xgbr.score(p_clouds_trn_x, p_clouds_trn_y)
    print("Training score:", score)
    return {"model": xgbr}


def predict_and_evaluate(
    p_clouds_tst_x: pd.DataFrame,
    p_clouds_tst_y: pd.DataFrame,
    model: xgb.sklearn.XGBRegressor,
    mlflow_experiment: str,
) -> None:
    """
    Use a trained XGBoost regression model to make predictions in a test set
    and compute the mean squared error (MSE). It logs the hyperparameters of
    the model, its MSE score on the test set, and two plots to MLFlow:
        A feature importance plot for the trained XGBoost regression model 
        A variable correlation plot for the trained XGBoost regression model 
    XGBoost regression model)
    Args:
        p_clouds_tst_x: Input variables of our test set
        p_clouds_tst_y: Variable to predict in our test set
        model: A trained XGBoost regression model
        mlflow_experiment: Name to give our MLFLow experiment
    """
    # Make predictions
    preds = model.predict(p_clouds_tst_x)
    # Compute MSE
    mse = mean_squared_error(p_clouds_tst_y, preds)
    print("MSE: %.8f" % mse)

    mlflow.set_experiment(mlflow_experiment)
    run_name = mlflow_experiment + time.strftime("_%y%m%d_%H%M%S")
    with mlflow.start_run(run_name=run_name):
        # Log params and metrics
        params = model.get_xgb_params()
        mlflow.log_param("max_depth", params["max_depth"])
        mlflow.log_param("learning_rate", params["learning_rate"])
        mlflow.log_param("subsample", params["subsample"])
        mlflow.log_param("colsample_bytree", params["colsample_bytree"])
        mlflow.log_metric("training_score", mse)

        # Feature importace plot
        plot_feat_importance = plt.figure(1)
        sorted_idx = model.feature_importances_.argsort()
        plt.barh(
            p_clouds_tst_x.columns[sorted_idx], model.feature_importances_[sorted_idx]
        )
        plt.xlabel("XGBoost Feature Importance")
        plt.title("Feature importance")

        # Var correlation plot
        df_plot = p_clouds_tst_x.sample(25, random_state=42)
        preds = model.predict(df_plot)
        plot_var_correlation = plt.figure(2)
        plt.plot(df_plot["re_liq"], model.predict(df_plot), color="blue")
        plt.xlabel("re_liq")
        plt.ylabel("nb_pocket_ice_over_area")
        plt.title("Correlation")

        # Log figures
        mlflow.log_figure(
            plot_feat_importance, artifact_file="figure/feat_importance.png"
        )
        mlflow.log_figure(
            plot_var_correlation, artifact_file="figure/var_correlation.png"
        )

    return None
