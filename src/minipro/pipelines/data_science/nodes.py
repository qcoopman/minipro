""" Nodes for the data science pipeline """
import pandas as pd
from typing import Dict, Tuple
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.figure
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
    print(xgbr)
    xgbr.fit(p_clouds_trn_x, p_clouds_trn_y)
    score = xgbr.score(p_clouds_trn_x, p_clouds_trn_y)
    print("Training score: ", score)
    return {"model": xgbr}


def predict_and_evaluate(
    p_clouds_tst_x: pd.DataFrame,
    p_clouds_tst_y: pd.DataFrame,
    model: xgb.sklearn.XGBRegressor,
) -> Tuple[matplotlib.figure.Figure, matplotlib.figure.Figure]:
    """
    Use a trained XGBoost regression model to make predictions in a test set
    and compute the mean squared error (MSE)
    Args:
        p_clouds_tst_x: Input variables of our test set
        p_clouds_tst_y: Variable to predict in our test set
    Returns:
        A trained XGBoost regression model
    """
    # Make predictions
    preds = model.predict(p_clouds_tst_x)
    # Compute MSE
    mse = mean_squared_error(p_clouds_tst_y, preds)
    print("MSE: %.8f" % mse)

    # Feature importace plot
    plot_feat_importance = plt.figure(1)
    sorted_idx = model.feature_importances_.argsort()
    plt.barh(p_clouds_tst_x.columns[sorted_idx], 
        model.feature_importances_[sorted_idx])
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

    return {
        "chart_feat_importance": plot_feat_importance,
        "chart_var_correlation": plot_var_correlation,
    }
