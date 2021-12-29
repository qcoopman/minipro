""" Nodes for the data engineering pipeline """
import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split


def split_data(
    p_clouds: pd.DataFrame, tst_data_pct: float
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits the cloud data into train and test set
    Args:
        p_clouds: Dataframe that contains all the data points
        tst_data_pct: Proportion of the dataset to include in the test split
    Returns:
        A tuple made up of four datasets: X_train, Y_train, X_test, Y_test
    """
    y = p_clouds.pop("nb_pocket_ice_over_area")
    x = p_clouds
    x_trn, x_tst, y_trn, y_tst = train_test_split(x, y, test_size=tst_data_pct)
    return {
        "x_trn": x_trn,
        "x_tst": x_tst,
        "y_trn": y_trn.to_frame(),
        "y_tst": y_tst.to_frame(),
    }
