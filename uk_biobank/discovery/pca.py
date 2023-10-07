from sklearn.decomposition import PCA
from utils.datahandler import UKBiobankData
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import NamedTuple
from pathlib import Path


class PCAGraphs(NamedTuple):
    # plot to hold gender PCA
    gender: plt.figure
    age: plt.figure


class PCAResults:
    def __init__(self, graphs: PCAGraphs, version: str):
        self.graphs = graphs
        self.version = version

    def save(self, dir: Path):
        dir.mkdir(parents=True, exist_ok=True)
        for var, value in self.graphs._asdict().items():
            _path = dir / f"{var}_pca_plot_v{self.version}.png"
            value.savefig(_path)


class PCAPlotter:
    def __init__(self, ukbb_data: UKBiobankData, version: str):
        self.ukbb_data = ukbb_data
        self.version = version

    def plot(self):
        pca_data, model_basic = self.__fit_transform(
            self.ukbb_data.base_data, self.ukbb_data.base_data
        )

        # technically the eid should be in the same order, this is just to be safe
        plot_data = pd.merge(
            pca_data, self.ukbb_data.metadata, left_index=True, right_index=True
        )

        gender = self.__plot(
            plot_data,
            model_basic,
            "PCA_1",
            "PCA_2",
            hue="gender",
        )
        age = self.__plot(
            plot_data,
            model_basic,
            "PCA_1",
            "PCA_2",
            hue="age",
        )

        return PCAResults(PCAGraphs(gender, age), version=self.version)

    @staticmethod
    def __plot(data: pd.DataFrame, model: PCA, x: str, y: str, **kwargs):

        fig, ax = plt.subplots(figsize=(6, 6))
        sns.scatterplot(x=x, y=y, data=data, ax=ax, **kwargs)

        x_var = model.explained_variance_ratio_[data.columns.tolist().index(x)]
        ax.set_xlabel(f"{x}, {100*x_var:.1f}%")

        y_var = model.explained_variance_ratio_[data.columns.tolist().index(y)]
        ax.set_ylabel(f"{y}, {100*y_var:.1f}%")

        return fig

    @staticmethod
    def __fit_transform(x: pd.DataFrame, y: pd.DataFrame, **kwargs):
        model = PCA(**kwargs)
        model.fit(x.copy())
        results_np = model.transform(y.copy())
        return (
            pd.DataFrame(
                results_np,
                index=x.index.to_list(),
                columns=[f"PCA_{i+1}" for i in range(results_np.shape[-1])],
            ),
            model,
        )
