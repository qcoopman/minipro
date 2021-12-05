""" Nodes for the data_preparation pipeline """
import pandas as pd
from pathlib import Path
import datetime


def preprocess(data_dir: str) -> pd.DataFrame:
    """
    Reads all data files found in an input DATA_DIR and filters out malformed
    data points. Each file represents all satellite measurements of clouds in
    a given day over the Southern Ocean from 2005 to 2017. Each data point has
    28 columns
    Args:
        data_dir: Folder that contains all data files
    Returns:
        A dataframe that contains all well-formed data points
    """
    # Columns of each data file
    COL_NAMES = [
        "date",
        "area",
        "tau",
        "std_tau",
        "re",
        "std_re",
        "ctt",
        "std_ctt",
        "cth_mp",
        "std_cth",
        "perim",
        "nb_ice",
        "nb_liq",
        "re_liq",
        "re_ice",
        "off",
        "nb_pocket_ice",
        "size_pocket_ice",
        "size_pocket_std_ice",
        "nb_pocket_liq",
        "size_pocket_liq",
        "size_pocket_std_liq",
        "tau_liq",
        "tau_ice",
        "lon",
        "lat",
        "min_ctt",
        "max_ctt",
    ]

    # Retrieve a list of the paths of all data files
    I_FILES = list(Path(data_dir).glob("*.txt"))

    # Create a dataframe from each data file
    list_df = []
    for I_FILE in I_FILES:
        # Parse each data file into a dataframe
        df = pd.read_csv(I_FILE, delimiter=" ", names=COL_NAMES)
        # Filter out malformed data points
        df = df[
            ~df["re_liq"].isna()
            & ~df["re_ice"].isna()
            & (df["nb_ice"] != 0.0)
            & (df["nb_liq"] != 0.0)
            & (df["area"] > 50)
            & (df["tau"] > 1.0)
            & (df["size_pocket_ice"] != df["area"])
            & (df["size_pocket_liq"] != df["area"])
        ]
        # Adjust the value of two columns
        df["re_liq"] = df["re_liq"] * 10 ** 6
        df["re_ice"] = df["re_ice"] * 10 ** 6
        # Format date column
        df["date"] = pd.to_datetime(
            df["date"].astype("int64").astype(str), format="%Y%m%d%H%M"
        )
        # Add new columns that correspond to all parts of the date
        parse_function = lambda x: pd.Series(
            [
                x["date"].year,
                x["date"].month,
                x["date"].day,
                x["date"].hour,
                x["date"].minute,
            ]
        )
        df[["year", "month", "day", "hour", "minute"]] = df.apply(
            parse_function, axis=1
        )
        list_df.append(df)

    # Concatenate all dataframes
    return pd.concat(list_df, axis=0).reset_index(drop=True)
