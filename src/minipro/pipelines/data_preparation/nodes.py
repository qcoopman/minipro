""" Nodes for the data_preparation pipeline """
import pandas as pd
from pathlib import Path


def preprocess(data_dir: str) -> pd.DataFrame:
    """
    Reads all data files found in an input DATA_DIR and filters out malformed
    data points. Each file represents all satellite measurements of clouds in
    a given day over the Southern Ocean from 2005 to 2017. Each data or line
    represents one cloud object (a set of connected cloudy pixels from CLAAS-2
    dataset, https://doi.org/10.5676/EUM_SAF_CM/CLAAS/V002). Each data point
    has 28 columns
    Args:
        data_dir: Folder that contains all data files
    Returns:
        A dataframe that contains all well-formed data points
    """
    # Columns of each data file
    COL_NAMES = [
        "date",
        # Area of the cloud
        "area",
        # Cloud optical depth
        "tau",
        # Standard deviation tau
        "std_tau",
        # Hydrometeor effective radius
        "re",
        # Std re
        "std_re",
        # Cloud top temperature
        "ctt",
        # Standad deviation ctt
        "std_ctt",
        # Cloud top height
        "cth_mp",
        # Std CTH
        "std_cth",
        # Cloud perimeter
        "perim",
        # Number of ice pixels
        "nb_ice",
        # Number of liquid pixels
        "nb_liq",
        # Mean effective radius of liquid cloud droplets
        "re_liq",
        # Mean effective radius of ice crytals
        "re_ice",
        "off",
        # Number of ice pockets (cluster of ice pixels) within the cloud
        "nb_pocket_ice",
        # Mean size of ice pockets
        "size_pocket_ice",
        # Standard deviation of ice pocket size
        "size_pocket_std_ice",
        # Number of liquid pockets (cluster of liquid pockets) within the cloud
        "nb_pocket_liq",
        # Mean size of liquid pockets
        "size_pocket_liq",
        # Standard deviation of liquid pocket size
        "size_pocket_std_liq",
        # Mean optical thickness of liquid pixels
        "tau_liq",
        # Mean optical thickness of ice pixels
        "tau_ice",
        # Mean longitude of cloud object
        "lon",
        # Mean latitude of cloud object
        "lat",
        # Minimum of cloud top temperature
        "min_ctt",
        # Maximum of cloud top temperature
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
            & (df["nb_ice"] > 3.0)
            & (df["nb_liq"] > 3.0)
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
