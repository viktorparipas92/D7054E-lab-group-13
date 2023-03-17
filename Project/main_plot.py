import importlib
from attrition_api import fetch_data


def generate_visualizations(functions, data):
    for func_name in functions:
        func = getattr(attrition_plots, func_name)
        func(data)


if __name__ == '__main__':
    attrition_plots = importlib.import_module('attrition_plots')
    all_functions = [
        func for func in dir(attrition_plots)
        if callable(getattr(attrition_plots, func))
        and not func.startswith('__')
    ]

    attrition_df = fetch_data()

    generate_visualizations(all_functions, attrition_df)
