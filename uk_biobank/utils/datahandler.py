from pathlib import Path
import pandas as pd
from typing import NamedTuple
from utils.caching import cachewrapper

USE_CACHE = True


class UKBiobankData(NamedTuple):
    # this is the base dataframe,
    # with the phenotype and brain
    # variables
    base_data: pd.DataFrame

    # this is the map between
    # codified column titles
    # and true descriptions
    description: pd.DataFrame

    # map between the variables and
    # general categories
    cat_map: pd.DataFrame

    # metadata for important columns
    # that aren't in base_data
    metadata: pd.DataFrame


# have this cache wrapper because its faster to load
# a single pickle than multiple csv files
@cachewrapper("../data/ukbb_data_cache.pkl", USE_CACHE)
def load_ukbb_data(
    base_data_path: Path,
    description_path: Path,
    cat_map_path: Path,
    metadata_path: Path,
):
    """
    Load in behavioural phenotypes and auxillary files
    y_group is a relic of my naming conventions
    Output is:
    ukbb_y: Behavioural phenotype, 40681 ppl x 978 columns
            There are 977 behaviours and 1 'eid' column (called userID)
    y_desc_dict: Maps column names in ukbb_y to a descriptive
                 explanation of what they represent
                 Note that in the case of categorical values,
                 it may be necessary to go into the data showcase to determine
                 what is being encoded by the column (check 'type' of output)
    y_cat_dict: Maps column to the broad category it belongs to
    """

    metadata = pd.read_csv(metadata_path.resolve())
    metadata.columns = ["eid", "age", "gender"]

    # https://biobank.ndph.ox.ac.uk/showcase/field.cgi?id=31
    metadata["gender"] = metadata["gender"].map({0: "female", 1: "male"})
    metadata = metadata.set_index("eid")
    # metadata.index = metadata.index.astype(float)

    base_data = pd.read_csv(base_data_path.resolve(), low_memory=False, index_col=0)
    base_data = base_data.set_index("userID")

    description = pd.read_csv(
        description_path.resolve(), sep="\t", header=None, index_col=0
    ).to_dict()[1]
    cat_map = pd.read_csv(cat_map_path, index_col=0)

    # return instance of UKBiobankData -> namedtuple for simplification
    return UKBiobankData(base_data, description, cat_map, metadata)
