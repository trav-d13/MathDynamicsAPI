import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os
import imageio

resource_path = 'app/resources/'

def mandelbrot(c, max_iteration):
    """Mandelbrot calculation to return the iteration at which the pattern becomes unbound, or achieves the max iteration.
    
    Parameters:
        c (complex): The point in the complex plane at which
        max_iteration (int): The maximum iteraton to consider for the mandelbrot set

    Returns:
        (int): The numer of iterations until the pattern becomes unbound (or the max_iterations)
    """
    z = c
    for n in range(max_iteration):
        if abs(z) > 2:  # Escape condition checking
            return n  # Return number of iterations before becoming unbound
        z = z*z + c
    return max_iteration  # Pattern still bound, returning max iteration

def mandelbrot_iteration_generation(width: int, height: int, max_iterations: int, colour: str):
    frames = []  # Store the frames

    for i in range(2, max_iterations + 1, 10):  # generate number of frames (steps of 5)
        frame_i = mandelbrot_frame(width=width, height=height, iteration=i, max_iteration=max_iterations)  # Create the frame rendered from iteration i
        save_frame(frames_store=frames, img=frame_i, iteration=i, colour=colour)  # Save the created frame
    
    file_name = os.path.join(resource_path, f'mandelbrot_iter_{width}_{height}_{max_iterations}_{colour}.gif')
    imageio.mimsave(file_name, frames, fps=1, loop=0)  # Generate GIF
    return file_name


def mandelbrot_frame(width: int, height: int, iteration: int, max_iteration: int):
    img = np.zeros((width, height))  # Create a blank image 

    for x in range(width):  # Iterate through frame grid
        for y in range(height):

            c = complex(-2 + 2.5 * x / width, -1.25 + 2.5 * y / height)  # Convert pixel coordinate to complex number
            m = mandelbrot(c, iteration)  # Compute the number of iterations
            color = 255 - int(m * 255 / max_iteration)  # Color depends on the number of iterations
            img[y, x] = color # Add value to the frame

    return img

def save_frame(frames_store: list, img: np.matrix, iteration: int, colour: str):
    fig, ax = plt.subplots()  # Create and save the current frame
    ax.imshow(img, extent=[-2, 0.5, -1.25, 1.25], cmap=colour)  # Setting visual limits
    ax.axis('off')  # Hide axes
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove padding and margins
    fig.patch.set_facecolor('none')  # No background
    ax.patch.set_alpha(0)  # Transparent axis

    with tempfile.TemporaryDirectory() as temp_frames_path:
        filename = os.path.join(temp_frames_path, f'frame_{iteration}.png')
        plt.savefig(filename, transparent=True)  # Save with transparency
        frames_store.append(imageio.imread(filename))  # Save the frame
        plt.close(fig)