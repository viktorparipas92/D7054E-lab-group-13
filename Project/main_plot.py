import importlib
import os
from typing import List

import pandas as pd
from matplotlib import pyplot as plt

from attrition_api import fetch_data


def generate_visualizations(functions: List[str], data: pd.DataFrame):
    for function_name in functions:
        function = getattr(attrition_plots, function_name)
        function(data)
        filename = function_name.lstrip('create_').replace('_', '-')
        if os.path.isfile(filename):
            os.remove(filename)

        plt.savefig(f'images/{filename}')


if __name__ == '__main__':
    attrition_plots = importlib.import_module('attrition_plots')
    all_functions = [
        func for func in dir(attrition_plots)
        if callable(getattr(attrition_plots, func))
        and not func.startswith('__')
    ]

    attrition_df = fetch_data()

    generate_visualizations(all_functions, attrition_df)
