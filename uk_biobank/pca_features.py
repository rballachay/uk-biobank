from utils.datahandler import load_ukbb_data
from discovery.pca import PCAPlotter
from pathlib import Path

VERSION_NUMBER = "1.0"


def main(
    base_data_path: Path,
    description_path: Path,
    cat_map_path: Path,
    metadata_path: Path,
    results: Path = Path("results"),
):

    ukbb_data = load_ukbb_data(
        base_data_path, description_path, cat_map_path, metadata_path
    )

    pca_results = PCAPlotter(ukbb_data=ukbb_data, version=VERSION_NUMBER).plot()

    pca_results.save(results)


if __name__ == "__main__":
    base_data_path = Path("../data/ukbb_miller_mh_v1_phes_filled.csv")
    description_path = Path("../data/ukbb_miller_mh_v1_description.txt")
    cat_map_path = Path("../data/ukbb_miller_mh_v1_cat_map.csv")
    metadata_path = Path("../data/ukb40500_selected_cols.csv")
    main(base_data_path, description_path, cat_map_path, metadata_path)
