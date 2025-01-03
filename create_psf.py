import numpy as np
from scipy.ndimage import gaussian_filter

def random_walk(steps, sigma):
    """Generate a 2D random walk."""
    changes = np.random.normal(0, sigma, (steps, 2))
    path = np.cumsum(changes, axis=0)
    return path - np.mean(path, axis=0)  # Center the path

def create_psf(size, gauss_sigma, walk_steps, walk_sigma):
    """Create a PSF with Gaussian blur and random walk."""
    psf = np.zeros((size, size))
    center = np.array([size, size]) / 2 - 0.5
    
    # Create random walk path
    walk_path = random_walk(walk_steps, walk_sigma)
    
    # Map the random walk to the PSF grid and add intensity
    for pos in walk_path:
        x, y = np.round(pos + center).astype(int)
        if 0 <= x < size and 0 <= y < size:
            psf[x, y] += 1
    
    # Apply Gaussian blur
    psf_blurred = gaussian_filter(psf, sigma=gauss_sigma)
    
    # Normalize PSF
    psf_final = psf_blurred / psf_blurred.sum()
    
    return psf_final

# Parameters
psf_size = 64  # Size of the PSF matrix
gaussian_blur_sigma = 2  # Sigma for Gaussian blur
random_walk_steps = 100  # Number of steps in the random walk
random_walk_sigma = 2  # Sigma for the step size in the random walk

# Create PSF
psf = create_psf(psf_size, gaussian_blur_sigma, random_walk_steps, random_walk_sigma)

# Optionally, visualize the PSF using matplotlib
import matplotlib.pyplot as plt
plt.imshow(psf, cmap='gray')
plt.colorbar()
plt.title('Point Spread Function (PSF)')
plt.show()