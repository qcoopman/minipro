""" Nodes for the data preparation pipeline """
import pandas as pd
from pathlib import Path


def preprocess(data_dir_mps: str, data_dir_era: str) -> pd.DataFrame:
    """
    Reads all data files and filters out malformed data points.
    Each file represents all satellite measurements of clouds in a given day
    over the Southern Ocean from 2005 to 2017. Each line represents one cloud
    object (a set of connected cloudy pixels from CLAAS-2 dataset,
    https://doi.org/10.5676/EUM_SAF_CM/CLAAS/V002)
    Args:
        data_dir_mps: Folder that contains one part of the data files
        Each MPS data file contains 28 columns
        data_dir_era: Folder that contains complementary data
        Each ERA data file contains 5 columns
    Returns:
        A dataframe that contains all well-formed data points
    """
    # Columns of each MPS data file
    COL_NAMES_MPS = [
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
        "off1",
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
    # Columns of each ERA data file
    COL_NAMES_ERA = [
        "off2",
        # Convective available potential energy
        "cape",
        # Vertical velocity at 500 hPa
        "omega",
        # Sea surface temperature
        "sst",
        "off3",
    ]

    # Retrieve a list of the paths of all MPS and ERA data files
    # There should be a matching ERA data file for each MPS data file that
    # should have the same name as the MPS file but with the suffix "CAPE"
    I_FILES = list(Path(data_dir_mps).glob("*.txt"))

    # Create a dataframe from each data file
    list_df = []
    for MPS_FILE in I_FILES:
        ERA_FILE = Path(str(MPS_FILE.with_suffix("")) + "_CAPE.txt")
        ERA_FILE = Path(str(ERA_FILE).replace(data_dir_mps, data_dir_era))

        if ERA_FILE.exists():
            # Parse each data file into dataframes
            df_mps = pd.read_csv(MPS_FILE, delimiter=" ", names=COL_NAMES_MPS)
            df_era = pd.read_csv(ERA_FILE, delimiter=" ", names=COL_NAMES_ERA)

            if len(df_mps) == len(df_era):
                # Adjust the value of two columns
                df_mps["re_liq"] = df_mps["re_liq"] * 10 ** 6
                df_mps["re_ice"] = df_mps["re_ice"] * 10 ** 6
                # Format date column
                df_mps["date"] = pd.to_datetime(
                    df_mps["date"].astype("int64").astype(str), format="%Y%m%d%H%M"
                )
                # Add a month column
                try:
                    parse_function = lambda x: pd.Series([x["date"].month])
                    df_mps[["month"]] = df_mps.apply(parse_function, axis=1)
                except ValueError:
                    continue

                # Concatenate MPS and ERA dataframes
                df = pd.concat([df_mps, df_era], axis=1)
                # Add new column that we will try and predict
                df["nb_pocket_ice_over_area"] = df.apply(
                    lambda row: row.nb_pocket_ice / row.area, axis=1
                )
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

                # Drop columns that won't be used for training
                df = df.drop(
                    columns=[
                        "date",
                        "area",
                        "std_tau",
                        "re",
                        "std_re",
                        "std_ctt",
                        "cth_mp",
                        "std_cth",
                        "off1",
                        "nb_ice",
                        "nb_liq",
                        "nb_pocket_ice",
                        "size_pocket_ice",
                        "off2",
                        "size_pocket_std_ice",
                        "nb_pocket_liq",
                        "size_pocket_liq",
                        "size_pocket_std_liq",
                        "min_ctt",
                        "max_ctt",
                        "off3",
                    ]
                )

                list_df.append(df)

    # Concatenate all dataframes
    df = pd.concat(list_df, axis=0).reset_index(drop=True)
    print("Number of data points in our resulting data frame: %d" % (len(df)))
    return df
