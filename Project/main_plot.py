import importlib
from attrition_api import fetch_data

# Import all functions from attrition_plots
attrition_plots = importlib.import_module("attrition_plots")
all_functions = [
    func for func in dir(attrition_plots)
    if callable(getattr(attrition_plots, func))
    and not func.startswith("__")
]


def generate_visualizations(data):
    for func_name in all_functions:
        func = getattr(attrition_plots, func_name)
        func(data)


if __name__ == '__main__':
    attrition_df = fetch_data()
    generate_visualizations(attrition_df)
