import importlib
import os
from typing import List, Callable

import pandas as pd
from matplotlib import pyplot as plt

from attrition_api import fetch_data
from attrition_plots import (
    create_hist_age_distribution,
    create_violin_plot,
    create_bar_overtime,
    create_pie_chart_yes,
    create_pie_chart_no,
    create_bar_education_level,
    create_plot_business_travel,
)


PLOT_FUNCTIONS = [
    create_hist_age_distribution,
    create_violin_plot,
    create_bar_overtime,
    create_pie_chart_yes,
    create_pie_chart_no,
    create_bar_education_level,
    create_plot_business_travel,
]


def generate_visualizations(functions: List[Callable], data: pd.DataFrame):
    for function in functions:
        function(data)
        filename = function.__name__.lstrip('create_').replace('_', '-')
        path = f'images/{filename}'
        if os.path.isfile(path):
            os.remove(path)

        plt.savefig(path)
        plt.show()


if __name__ == '__main__':
    attrition_df = fetch_data()

    generate_visualizations(PLOT_FUNCTIONS, attrition_df)
