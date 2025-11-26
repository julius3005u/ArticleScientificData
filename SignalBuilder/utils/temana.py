"""
Temana is a library of functions for temporal data analysis and artificial signal generation.
"""

import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import numpy as np
from scipy.interpolate import interp1d, make_interp_spline
import random

# Dataset Definition
class MyDataset(torch.utils.data.Dataset):
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def __len__(self):
        return len(self.x_train)

    def __getitem__(self, idx):
        return self.x_train[idx], self.y_train[idx]

# Definition of the Encoder Network Based on Convolutional Layers.
class CNNAutoencoder(nn.Module):
    """
    A convolutional neural network for autoencoding temporal signals.

    Args:
        n_input (int): Number of input features (subsampled signal length, 1000).
        n_hidden (int): Number of hidden units in each convolutional layer.
        n_output (int): Number of output features (full signal length, 5000).

    """

    def __init__(self, n_input, n_hidden, n_output):
        super(CNNAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv1d(n_input, n_hidden, kernel_size=1),
            nn.BatchNorm1d(n_hidden),
            #nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=1),
            nn.Conv1d(n_hidden, n_hidden, kernel_size=1),
            nn.BatchNorm1d(n_hidden),
            #nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=1)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose1d(n_hidden, n_hidden, kernel_size=3),
            nn.BatchNorm1d(n_hidden),
            #nn.ReLU(inplace=True),
            nn.Upsample(scale_factor=2),
            nn.ConvTranspose1d(n_hidden, n_output, kernel_size=1),
            nn.BatchNorm1d(n_output),
            #nn.ReLU(inplace=True)
        )


    def forward(self, x):
        """
        Forward propagation of the neural network.

        Args:
            x (tensor): Input tensor containing the subsampled signal (length 1000).

        Returns:
            tensor: Output tensor with the reconstructed signal (length 5000).
        """
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


# Function to generate random signals with high and low resolution.
def generate_signal(x, xm):
    """
        Input:
            x (array): Data vector for super-sampling.
            xm (array): Data vector for sub-sampling.
        Output:
            list: Super-sampled signal and sub-sampled signal.
    """
    choose = np.random.randint(0, 2, 1)
    A = (2 * np.random.rand() - 1) * np.random.randint(1, 6, 1)  # Amplitude
    B = (2 * np.random.rand() - 1) * np.random.randint(1, 10, 1)  # Frequency
    C = (2 * np.random.rand() - 1) * np.random.randint(1, 10, 1)  # Translation

    if choose == 0:
        # Generate the signal based on sine
        y = A * np.sin(B * x) + C
        ym = A * np.sin(B * xm) + C

    else:
        # Generate the signal based on cosine
        y = A * np.cos(B * x) + C
        ym = A * np.cos(B * xm) + C

    return [y, ym]


def generate_noise(x, xm):
    """
        Input:
            x (array): Data vector for super-sampling.
            xm (array): Data vector for sub-sampling.
        Output:
            list: Noise for super-sampling and sub-sampling.
    """
    choose = np.random.randint(0, 2, 1)
    A = (2 * np.random.rand() - 1) * np.random.uniform(0.1, 0.5, 1)  # Amplitude
    B = (2 * np.random.rand() - 1) * np.random.randint(100, 200, 1)  # Frequency

    if choose == 0:
        # Generate the noise based on sine
        r = A * np.sin(B * x)
        rm = A * np.sin(B * xm)
    else:
        # Generate the noise based on cosine
        r = A * np.cos(B * x)
        rm = A * np.cos(B * xm)
        
    return [r, rm]


def read_data(filename):
    """
    Reads data from a txt file.

    Input:
        filename (str): Name of the txt file.

    Returns:
        torch.Tensor: A PyTorch tensor containing the data from the txt file.
    """
    # Uncomment if manual reading is required:
    # with open(filename, "r") as f:
    #     data = f.read()
    # data = np.array([float(x) for x in data.split("\n")])
    
    data = np.loadtxt(filename)  # Load data from the txt file
    data = torch.tensor(data)    # Convert to a PyTorch tensor
    
    # Ensure data type is float32
    if data.type != torch.float32:
        data = data.float()
        
    return data


import torch.nn as nn

class Autoencoder(nn.Module):
    """
    Class that implements an autoencoder neural network.

    Args:
        n_input: Number of neurons in the input layer.
        n_hidden: Number of neurons in each hidden layer.
        n_output: Number of neurons in the output layer.
    """

    def __init__(self, n_input, n_hidden, n_output):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(n_input, n_hidden),
            nn.ReLU(),
            nn.Linear(n_hidden, n_hidden),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(n_hidden, n_hidden),
            nn.ReLU(),
            nn.Linear(n_hidden, n_output)
        )

    def forward(self, x):
        """
        Performs the forward propagation of the neural network.

        Args:
            x: Input to the neural network.

        Returns:
            Output of the neural network.
        """

        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    

# Dataset Definition
class MyDataset(torch.utils.data.Dataset):
    def __init__(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def __len__(self):
        return len(self.x_train)

    def __getitem__(self, idx):
        return self.x_train[idx], self.y_train[idx]
    

class CNNAutoencoder(nn.Module):
    """
    A convolutional neural network for temporal signal autoencoding.

    Args:
        n_input (int): Number of input features (subsample length, 1000).
        n_hidden (int): Number of hidden units in each convolutional layer.
        n_output (int): Number of output features (full signal length, 5000).
    """
    def __init__(self, n_input, n_hidden, n_output):
        super(CNNAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv1d(n_input, n_hidden, kernel_size=1),
            nn.BatchNorm1d(n_hidden),
            #nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=1),
            nn.Conv1d(n_hidden, n_hidden, kernel_size=1),
            nn.BatchNorm1d(n_hidden),
            #nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=1)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose1d(n_hidden, n_hidden, kernel_size=3),
            nn.BatchNorm1d(n_hidden),
            #nn.ReLU(inplace=True),
            nn.Upsample(scale_factor=2),
            nn.ConvTranspose1d(n_hidden, n_output, kernel_size=1),
            nn.BatchNorm1d(n_output),
            #nn.ReLU(inplace=True)
        )

    def forward(self, x):
        """
        Forward propagation of the neural network.

        Args:
            x (tensor): Input tensor containing the subsampled signal (length 1000).

        Returns:
            tensor: Output tensor with the reconstructed signal (length 5000).
        """

        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    

# Tension spline generator function. Taken from the Numerical Analysis book by David Kincaid.
def tension_spline_interpolator(x, y, tau):
    n = len(x) - 1
    
    # Step 1: Calculate hi, alpha, beta, gamma
    h = np.diff(x)
    alpha = 1/h - tau/np.sinh(tau * h)
    beta = tau * np.cosh(tau * h)/np.sinh(tau * h) - 1/h
    gamma = tau**2 * np.diff(y)/h

    # Step 2: Set up the tridiagonal system A * Z = Y
    A = np.zeros((n+1, n+1))
    Y = np.zeros(n+1)
    
    A[0, 0] = 1
    A[n, n] = 1
    for i in range(1, n):
        A[i, i-1] = alpha[i-1]
        A[i, i] = beta[i-1] + beta[i]
        A[i, i+1] = alpha[i]
        Y[i] = gamma[i] - gamma[i-1]
    
    # Solve the system for Z
    Z = np.linalg.solve(A, Y)
    
    # Step 3: Define the tension spline function
    def tension_spline(x_eval):
        result = np.zeros_like(x_eval)
        for i in range(n):
            mask = (x_eval >= x[i]) & (x_eval <= x[i+1])
            xi = x_eval[mask]
            t1 = Z[i] * np.sinh(tau * (x[i+1] - xi)) + Z[i+1] * np.sinh(tau * (xi - x[i]))
            t1 /= tau**2 * np.sinh(tau * h[i])
            t2 = (y[i] - Z[i]/tau**2) * (x[i+1] - xi) / h[i]
            t3 = (y[i+1] - Z[i+1]/tau**2) * (xi - x[i]) / h[i]
            result[mask] = t1 + t2 + t3
        return result
    
    return tension_spline


## Function to generate amplitude change reference points
def generate_amplitude_change_points(x0, x1):
    """
    Generates reference points for amplitude changes within a specified range.

    Args:
        x0 (float): Start of the range.
        x1 (float): End of the range.

    Returns:
        list: A list of tuples (x, y), where x is the position and y is the amplitude.
    """
    # Randomly select amplitude (between 1.0 and 10.0)
    choice = np.random.randint(0, 2, 1)
    amplitude = (2 * np.random.rand() - 1) * np.random.randint(1, 10, 1)  # Amplitude
    frequency = (2 * np.random.rand() - 1) * np.random.randint(1, 10, 1)  # Frequency
    phase = np.random.rand() * np.pi  # Phase

    # Randomly select the number of points (between 1 and 4)
    num_points = random.randint(1, 4)
    
    # Generate points in the range of x0 to x1
    partition = np.linspace(x0, x1, num_points + 2)
    reference_points = []

    for i in range(num_points + 2):
        x = partition[i]
        y = (amplitude * np.sin(frequency * (x - phase)))[0]
        y = np.abs(y)

        # Ensure the amplitude is not too low
        if y < 0.5:
            y = (amplitude * np.random.uniform(0.5, 1))[0]
            y = np.abs(y)
        
        reference_points.append((x, y))
    
    return reference_points


def linear_spline_interpolator(points):
    """
    Generates a linear spline interpolation function based on the provided reference points.

    Args:
        points (list of tuples): List of (x, y) coordinates representing the reference points.

    Returns:
        function: A linear interpolation function that can be evaluated at any x value.
    """
    # Separate the x and y coordinates from the input points
    x_coords, y_coords = zip(*points)
    
    # Create a linear interpolation function
    interpolator = interp1d(x_coords, y_coords, kind='linear', fill_value="extrapolate")
    
    return interpolator


def zero_order_spline_interpolator(points):
    """
    Generates a zero-order spline interpolation function based on the provided reference points.

    Args:
        points (list of tuples): List of (x, y) coordinates representing the reference points.

    Returns:
        function: A zero-order interpolation function that can be evaluated at any x value.
    """
    # Separate the x and y coordinates from the input points
    x_coords, y_coords = zip(*points)
    
    # Create a zero-order (stepwise) interpolation function
    interpolator = interp1d(x_coords, y_coords, kind='zero', fill_value="extrapolate")
    
    return interpolator


def n_degree_spline_interpolator(points, degree):
    """
    Generates an n-degree spline interpolation function based on the provided reference points.

    Args:
        points (list of tuples): List of (x, y) coordinates representing the reference points.
        degree (int): Degree of the spline interpolation (e.g., 1 for linear, 3 for cubic).

    Returns:
        function: An n-degree interpolation function that can be evaluated at any x value.
    """
    # Separate the x and y coordinates from the input points
    x_coords, y_coords = zip(*points)
    
    # Create the n-degree spline interpolation function
    interpolator = make_interp_spline(x_coords, y_coords, k=degree)
    
    return interpolator


# This function generates variable amplitude signals based on the splines generated previously.

def generate_variable_amplitude_signal(x, xm):
    """
    Input:
        x: Data vector for super-sampling.
        xm: Data vector for sub-sampling.
    Output:
        Signal for super-sampling and sub-sampling.

    """
    choose = np.random.randint(0, 2, 1)
    choose2 = np.random.randint(0, 2, 1)
    A = (2 * np.random.rand() - 1) * np.random.randint(1, 6, 1)  # Amplitude
    B = (2 * np.random.rand() - 1) * np.random.randint(1, 25, 1)  # Frequency
    C = (2 * np.random.rand() - 1) * np.random.randint(1, 10, 1)  # Translation
    D = np.random.rand() * np.pi  # Phase
    points = generate_amplitude_change_points(xm[0], xm[-1])

    if choose == 0:
        # Generate the signal based on sine
        y = A * np.sin(B * (x - D))
        ym = A * np.sin(B * (xm - D))
    else:
        # Generate the signal based on cosine
        y = A * np.cos(B * (x - D))
        ym = A * np.cos(B * (xm - D))

    points = generate_amplitude_change_points(x[0], x[-1])
    xs, ys = zip(*points)  # Unpack the points
    tau = np.random.choice([1, 3, 5, 8, 10, 12, 15, 20])

    if choose2 == 0:  # Splines with random tension
        y = tension_spline_interpolator(xs, ys, tau)(x) * y + C
        ym = tension_spline_interpolator(xs, ys, tau)(xm) * ym + C
    else:  # Splines with infinite tension
        y = zero_order_spline_interpolator(points)(x) * y + C
        ym = zero_order_spline_interpolator(points)(xm) * ym + C

    return [y, ym]


def generate_non_uniform_high_low_frequency_points(x0, x1):
    """
    Generates reference points with high and low frequencies in a non-uniform distribution.

    Args:
        x0 (float): Start of the interval.
        x1 (float): End of the interval.

    Returns:
        tuple: 
            - points: List of tuples containing (x, frequency) for each point.
            - high_freq_points: List of tuples containing (x, high_frequency) for high-frequency points.
            - variation_type: List of frequency variation types ("low", "high", "no_change").
    """
    # Randomly select high frequencies
    high_frequency = np.random.uniform(20, 100, 10)
    high_frequency = np.sort(high_frequency)
    # Randomly select low frequencies
    low_frequency = np.random.uniform(1, 5, 10)
    low_frequency = np.sort(low_frequency)
    
    # Randomly select the number of frequency change points
    num_points = random.randint(2, 11)
    tdom = np.zeros(num_points + 2)  # To include 0 and 1
    tdom[-1] = 1
    tdom[1:-1] = np.sort(np.random.rand(num_points))
    partition = x0 + (x1 - x0) * tdom
    
    points = []
    variation_type = []
    high_freq_tdom = [tdom[0]]  # Only includes high-frequency information
    high_freq_y = []
    
    # Initialize the type of variation
    current_variation = np.random.choice(["low", "high"], p=[0.96, 0.04])
    # Initialize the frequency
    y = 1
    for i in range(num_points + 2):
        # First iteration
        x = partition[i]
        
        if i == 0:            
            if current_variation == "low":
                y = np.random.choice(low_frequency)
                variation_type.append("low")
                high_freq_y.append(0)
            else:
                y = np.random.choice(low_frequency)  # Select a low frequency to carry the high frequency
                variation_type.append("high")
                high_freq_tdom.append(np.random.uniform(partition[i], partition[i+1], 1)[0])
                temp_high_freq = np.random.choice(high_frequency)
                high_freq_y.append(temp_high_freq)
                high_freq_y.append(temp_high_freq)

        else:
            # Force changes in high frequencies
            if variation_type[-1] == "high":
                current_variation = np.random.choice(["low", "no_change"], p=[0.95, 0.05])
            else:
                current_variation = np.random.choice(["low", "high", "no_change"], p=[0.20, 0.07, 0.73])
            if current_variation == "low":
                y = np.random.choice(low_frequency)
                high_freq_y.append(0)
                high_freq_tdom.append(x)
                variation_type.append(current_variation)

            elif current_variation == "high":
                y = np.random.choice(low_frequency)  # Select a low frequency to carry the high frequency
                variation_type.append("high")
                high_freq_tdom.append(x)
                if i != num_points + 1:
                    temp_high_freq = np.random.choice(high_frequency)
                    high_freq_tdom.append(np.random.uniform(partition[i], partition[i+1], 1)[0])
                    high_freq_y.append(temp_high_freq)
                    high_freq_y.append(temp_high_freq)
                else:
                    high_freq_y.append(0)
                    
            else:
                variation_type.append(variation_type[-1])
                high_freq_y.append(0)
                high_freq_tdom.append(x)
        
        points.append((x, y))
    high_freq_points = [(high_freq_tdom[i], high_freq_y[i]) for i in range(len(high_freq_tdom))]
    
    return points, high_freq_points, variation_type


def generate_signal_with_nu_high_frequency(x, xm):
    """
    Generates signals with non-uniform frequency changes, supporting both supersampling and subsampling.

    Args:
        x (array): Data vector for supersampling.
        xm (array): Data vector for subsampling.

    Returns:
        list: A list containing:
            - y (array): Supersampled signal.
            - ym (array): Subsampled signal.
            - noise (array): Noise added to the signal.
    """
    # Generate the non-uniform frequency change points
    points, high_freq_points, freq_type = generate_non_uniform_high_low_frequency_points(x[0], x[-1])
    xf, yf = zip(*points)  # Unpack the points
    tau = np.random.choice([1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2])

    # Equal weight for sine and cosine waves
    wave_choice = np.random.choice([0, 1], 1)
    # Less weight for abrupt frequency changes
    spline_choice = np.random.choice([0, 1], 1, p=[0.98, 0.02])

    A = (2 * np.random.rand() - 1) * np.random.randint(1, 6, 1)  # Amplitude
    B = tension_spline_interpolator(xf, yf, tau)  # Frequency
    C = (2 * np.random.rand() - 1) * np.random.randint(1, 10, 1)  # Translation
    D = np.random.rand() * np.pi  # Phase

    if wave_choice == 0:
        # Generate the signal using sine function
        y = A * np.sin(B(x) * (x - D))
        ym = A * np.sin(B(xm) * (xm - D))
    else:
        # Generate the signal using cosine function
        y = A * np.cos(B(x) * (x - D))
        ym = A * np.cos(B(xm) * (xm - D))

    # Generate amplitude change points
    points = generate_amplitude_change_points(x[0], x[-1])
    xs, ys = zip(*points)  # Unpack the points
    tau = np.random.choice(np.linspace(1, 2, 21))
    noise_amplitude = np.random.uniform(0.08, 0.2, 1)

    # Generate noise for both supersampling and subsampling
    noise = noise_amplitude * tension_spline_interpolator(xs, ys, tau)(x) * np.sin(zero_order_spline_interpolator(high_freq_points)(x) * x)
    noise_subsample = noise_amplitude * tension_spline_interpolator(xs, ys, tau)(xm) * np.sin(zero_order_spline_interpolator(high_freq_points)(xm) * xm)

    if spline_choice == 0:  # Random tension splines
        y = tension_spline_interpolator(xs, ys, tau)(x) * y + C + noise
        ym = tension_spline_interpolator(xs, ys, tau)(xm) * ym + C + noise_subsample
    else:  # Infinite tension splines
        y = zero_order_spline_interpolator(points)(x) * y + C + noise
        ym = zero_order_spline_interpolator(points)(xm) * ym + C + noise_subsample

    return [y, ym, noise]


def generate_signal_list_with_nu_high_frequency(x, len_x):
    """
    Generates signals with non-uniform frequency variations at multiple sampling rates.

    Args:
        x (array): Data vector for supersampling.
        len_x (list): List of sampling sizes for subsampled signals, e.g., [250, 500, 1000].

    Returns:
        list: A list containing:
            - y (array): Supersampled signal.
            - list_y (list of arrays): List of subsampled signals.
            - noise (array): Noise added to the supersampled signal.
    """
    # Generate frequency change points
    points, high_freq_points, freq_type = generate_non_uniform_high_low_frequency_points(x[0], x[-1])
    list_x = [np.linspace(x[0], x[-1], lx) for lx in len_x]  # Generate subsampled data vectors
    xf, yf = zip(*points)  # Unpack the frequency change points
    tau = np.random.choice([1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2])

    print("Frequency Type:", freq_type)
    print("Tension tau:", tau)

    # Randomly choose between sine and cosine wave
    wave_choice = np.random.choice([0, 1], 1)
    # Less weight is given to abrupt frequency variations
    spline_choice = np.random.choice([0, 1], 1, p=[0.98, 0.02])

    A = (2 * np.random.rand() - 1) * np.random.randint(1, 6, 1)  # Amplitude
    B = tension_spline_interpolator(xf, yf, tau)  # Frequency spline function
    C = (2 * np.random.rand() - 1) * np.random.randint(1, 10, 1)  # Translation
    D = np.random.rand() * np.pi  # Phase

    if wave_choice == 0:
        # Generate the signal based on the sine function
        y = A * np.sin(B(x) * (x - D))
        list_y = [A * np.sin(B(xm) * (xm - D)) for xm in list_x]
    else:
        # Generate the signal based on the cosine function
        y = A * np.cos(B(x) * (x - D))
        list_y = [A * np.cos(B(xm) * (xm - D)) for xm in list_x]

    # Generate amplitude change points
    points = generate_amplitude_change_points(x[0], x[-1])
    xs, ys = zip(*points)  # Unpack the amplitude change points
    tau = np.random.choice(np.linspace(1, 2, 21))
    print("Tension tau2:", tau)

    noise_amplitude = np.random.uniform(0.08, 0.2, 1)
    
    # Generate noise for supersampled and subsampled signals
    noise = noise_amplitude * tension_spline_interpolator(xs, ys, tau)(x) * np.sin(zero_order_spline_interpolator(high_freq_points)(x) * x)
    list_noise = [
        noise_amplitude * tension_spline_interpolator(xs, ys, tau)(xm) * np.sin(zero_order_spline_interpolator(high_freq_points)(xm) * xm)
        for xm in list_x
    ]

    if spline_choice == 0:  # Random tension splines
        y = tension_spline_interpolator(xs, ys, tau)(x) * y + C + noise
        list_y = [
            tension_spline_interpolator(xs, ys, tau)(xm) * ym + C + noise_subsample
            for xm, noise_subsample, ym in zip(list_x, list_noise, list_y)
        ]
    else:  # Infinite tension splines
        y = zero_order_spline_interpolator(points)(x) * y + C + noise
        list_y = [
            zero_order_spline_interpolator(points)(xm) * ym + C + noise_subsample
            for xm, noise_subsample, ym in zip(list_x, list_noise, list_y)
        ]

    return [y, list_y, noise]
