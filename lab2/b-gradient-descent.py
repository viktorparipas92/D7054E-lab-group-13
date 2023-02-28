import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from plot import create_plot


def gradient_step(
    vec: np.array, gradient: np.array, step_size: float
) -> np.array:
    assert len(vec) == len(gradient)
    return vec + step_size * gradient


def linear_gradient(x: float, y: float, theta: np.array) -> np.array:
    slope, intercept = theta
    predicted = slope * x + intercept
    error = predicted - y
    loss = error**2
    grad = [2 * error * x, 2 * error]
    return grad, loss


def plot_scatter_between_size_and_price(caulfield_north):
    plt.scatter(caulfield_north['Bedroom2'], caulfield_north['Price'])
    plt.xlabel('Number of Bedrooms')
    plt.ylabel('Price')
    plt.title('Price vs Number of Bedrooms in Caulfield North')


def plot_scatter_between_size_and_price_with_regression_line(
    caulfield_north, slope, intercept
):
    plot_scatter_between_size_and_price(caulfield_north)
    min_num_of_bedrooms = caulfield_north['Bedroom2'].min()
    max_num_of_bedrooms = caulfield_north['Bedroom2'].max()
    x = np.linspace(min_num_of_bedrooms, max_num_of_bedrooms, 100)
    y = slope * x + intercept
    plt.plot(x, y, '-r', label='Linear regression')
    plt.legend()
    plt.grid()


def _plot_learning_rate_and_parameters(data):
    plt.scatter(data['learning_rates'], data['slopes'], label='Slopes')
    plt.scatter(data['learning_rates'], data['intercepts'], label='Intercepts')
    plt.xlabel('Learning rates')
    plt.title('Optimal parameters obtained with different learning rates')
    plt.xscale('log')
    plt.legend()


def plot_sns_regression(caulfield_north):
    sns.regplot(x=caulfield_north['Bedroom2'], y=caulfield_north['Price'])
    plt.grid()
    plt.title('Price vs Number of Bedrooms in Caulfield North')


def gradient_descent(
        x, y, num_of_epochs=5000, learning_rate=0.01, extended_output=False
):
    if extended_output:
        losses = []
        thetas = []

    theta = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
    for epoch in range(num_of_epochs):
        gradients, epoch_losses = zip(*[
            linear_gradient(x, y, theta) for x, y in zip(x, y)
        ])
        gradients = np.array(gradients)
        gradient = gradients.mean(axis=0)
        theta = gradient_step(theta, gradient, -learning_rate)
        if extended_output:
            losses.append(np.mean(epoch_losses))
            thetas.append(theta)

    if extended_output:
        return theta, losses, thetas
    else:
        return theta


def experiment_with_learning_rates(x, y, *, learning_rates):
    thetas = [
        gradient_descent(x, y, learning_rate=lr) for lr in learning_rates
    ]
    data = pd.DataFrame({
        'learning_rates': learning_rates,
        'slopes': [theta[0] for theta in thetas],
        'intercepts': [theta[1] for theta in thetas],
    })

    create_plot(
        _plot_learning_rate_and_parameters, data,
        save=True, filename='melbourne-lr-plot.png'
    )


def plot_loss_function(x, y):
    _, losses, thetas = (
        gradient_descent(x, y, learning_rate=0.01, extended_output=True)
    )
    slopes, intercepts = zip(*thetas)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(slopes, intercepts, losses)


if __name__ == '__main__':
    melbourne_data = pd.read_csv('datasets/melbourne_data.csv')
    caulfield_north = (
        melbourne_data[melbourne_data['Suburb'] == 'Caulfield North']
    )
    create_plot(
        plot_scatter_between_size_and_price, caulfield_north,
    )

    number_of_bedrooms = caulfield_north['Bedroom2'].values
    price = caulfield_north['Price'].values
    slope, intercept = gradient_descent(number_of_bedrooms, price)
    print(f"Slope: {slope:.2f}, intercept: {intercept:.2f}")

    create_plot(
        plot_scatter_between_size_and_price_with_regression_line,
        caulfield_north,
        save=True,
        filename='melbourne-regplot-1.png',
        slope=slope,
        intercept=intercept,
    )

    create_plot(
        plot_sns_regression,
        caulfield_north,
        save=True,
        filename='melbourne-regplot-2.png',
    )

    experiment_with_learning_rates(
        number_of_bedrooms, price,
        learning_rates=[1e-4, 2e-4, 5e-4, 0.001, 0.002, 0.005, 0.01, 0.05, 0.1, 0.5],
    )

    create_plot(
        plot_loss_function,
        number_of_bedrooms,
        y=price,
        save=True,
        filename='melbourne-loss-function.png'
    )
