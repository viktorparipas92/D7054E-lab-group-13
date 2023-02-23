import pandas as pd

if __name__ == '__main__':
    melbourne_data = pd.read_csv('datasets/melbourne_data.csv')
    correlation = melbourne_data['Price'].corr(melbourne_data['Distance'])
    print(
        f"Correlation between the price and distance columns "
        f"is {correlation:.3f}."
    )