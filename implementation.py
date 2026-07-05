import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.optimize import curve_fit
from skimage.draw import disk
from skimage.filters import gaussian

# Simulated IR-uf-bSSFP signal model for T1 and T2 mapping
def signal_model(t, M0, T1, T2):
    return M0 * (1 - 2 * np.exp(-t / T1)) * np.exp(-t / T2)

# Generate synthetic data for testing
def generate_synthetic_data(shape=(64, 64), T1_range=(800, 1200), T2_range=(70, 110), noise_std=0.02):
    T1_map = np.random.uniform(T1_range[0], T1_range[1], size=shape)
    T2_map = np.random.uniform(T2_range[0], T2_range[1], size=shape)
    M0_map = np.ones(shape)
    time_points = np.linspace(0, 1, 20)  # Simulated time points in seconds
    signal = np.zeros((len(time_points), *shape))

    for i, t in enumerate(time_points):
        signal[i] = signal_model(t, M0_map, T1_map, T2_map)
        signal[i] += np.random.normal(0, noise_std, size=shape)  # Add noise

    return signal, T1_map, T2_map, time_points

# Nonlinear least squares fitting for T1 and T2 estimation
def fit_voxel_signal(time_points, signal):
    def fit_func(t, M0, T1, T2):
        return signal_model(t, M0, T1, T2)

    try:
        popt, _ = curve_fit(fit_func, time_points, signal, bounds=([0, 500, 50], [2, 2000, 200]))
        return popt[1], popt[2]  # T1, T2
    except RuntimeError:
        return np.nan, np.nan

# Voxel-wise T1 and T2 map estimation
def estimate_t1_t2_maps(signal, time_points):
    shape = signal.shape[1:]
    T1_map = np.zeros(shape)
    T2_map = np.zeros(shape)

    for i in range(shape[0]):
        for j in range(shape[1]):
            T1, T2 = fit_voxel_signal(time_points, signal[:, i, j])
            T1_map[i, j] = T1
            T2_map[i, j] = T2

    return T1_map, T2_map

# Simple U-Net for lung segmentation
class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2)
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(32, 16, kernel_size=2, stride=2), nn.ReLU(),
            nn.ConvTranspose2d(16, 1, kernel_size=2, stride=2), nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

# Generate synthetic lung mask
def generate_lung_mask(shape=(64, 64)):
    mask = np.zeros(shape)
    rr, cc = disk((32, 32), 20)
    mask[rr, cc] = 1
    return gaussian(mask, sigma=2) > 0.5

# Main function
if __name__ == '__main__':
    # Generate synthetic data
    signal, true_T1_map, true_T2_map, time_points = generate_synthetic_data()

    # Generate synthetic lung mask
    lung_mask = generate_lung_mask()

    # Train a simple U-Net for lung segmentation (dummy training for demonstration)
    unet = UNet()
    optimizer = optim.Adam(unet.parameters(), lr=0.001)
    criterion = nn.BCELoss()

    # Prepare data for training
    lung_mask_tensor = torch.tensor(lung_mask, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    signal_tensor = torch.tensor(signal.mean(axis=0), dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    for epoch in range(10):  # Dummy training loop
        optimizer.zero_grad()
        output = unet(signal_tensor)
        loss = criterion(output, lung_mask_tensor)
        loss.backward()
        optimizer.step()

    # Apply trained U-Net to segment lungs
    with torch.no_grad():
        predicted_mask = unet(signal_tensor).squeeze().numpy() > 0.5

    # Apply mask and estimate T1 and T2 maps
    masked_signal = signal[:, predicted_mask]
    T1_map, T2_map = estimate_t1_t2_maps(signal, time_points)

    # Print results
    print("True T1 Map (sample):", true_T1_map[predicted_mask][:5])
    print("Estimated T1 Map (sample):", T1_map[predicted_mask][:5])
    print("True T2 Map (sample):", true_T2_map[predicted_mask][:5])
    print("Estimated T2 Map (sample):", T2_map[predicted_mask][:5])