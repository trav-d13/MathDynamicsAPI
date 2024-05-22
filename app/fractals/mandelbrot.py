import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os
import imageio
from PIL import Image, ImageDraw, ImageFont
import textwrap

from app.text_info import create_text_image, Explanations

resource_path = 'app/resources/'

def mandelbrot_calc(c, max_iteration):
    """Mandelbrot calculation to return the iteration at which the pattern becomes unbound, or achieves the max iteration.
    
    Parameters:
        c (complex): The point in the complex plane at which
        max_iteration (int): The maximum iteraton to consider for the mandelbrot set

    Returns:
        (int): The number of iterations until the pattern becomes unbound (or the max_iterations)
    """
    z = c
    for n in range(max_iteration):
        if abs(z) > 2:  # Escape condition checking
            return n  # Return number of iterations before becoming unbound
        z = z*z + c
    return max_iteration  # Pattern still bound, returning max iteration

def mandelbrot_iteration_generation(width: int, height: int, max_iterations: int, colour: str):
    """ Generate a Mandelbrot GIF, based on successive maximum iterations to reveal a finer pattern corresponding to higher
    maximum iteration scores

    The method will generate successive Mandelbrot frames, using a range of iteration values from 2-`max_iteration` in steps of 10.

    Parameters:
        width (int): The width of the complex number (c) grid. This can be thought of as the width of the returned gif.
        height (int): The height of the complex number (c) grid. This can be thought of as the height of the returned gif.
        max_iterations (int): The maximum iteration value
        colour (string): Specify the colour to be used for visualization. Colours available correspond to [matplotlib colourmaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html)

    Returns:
        (os.path): The file path to the newly created mandelbrot gif resource. 
    """
    frames = []  # Store the frames

    for i in range(2, max_iterations + 1, 10):  # generate number of frames (steps of 5)
        frame_i = mandelbrot_frame(width=width, height=height, iteration=i, max_iteration=max_iterations)  # Create the frame rendered from iteration i
        save_frame(frames_store=frames, img=frame_i, iteration=i, colour=colour)  # Save the created frame
    
    file_name = os.path.join(resource_path, f'mandelbrot_iter_{width}_{height}_{max_iterations}_{colour}.gif')
    imageio.mimsave(file_name, frames, fps=1, loop=0)  # Generate GIF
    return file_name

def mandelbrot_iteration_generation_with_text(width: int, height: int, max_iterations: int, colour: str):
    mandelbrot_gif_path = mandelbrot_iteration_generation(width, height, max_iterations, colour)
    gif = Image.open(mandelbrot_gif_path)  # Load the gif

    text_width = 300
    text_height = gif.height  # Extract height to match text image with GIF
    text_image = create_text_image(width=text_width, height=text_height, explanation=Explanations.MANDELBROT_ITERATIVE)  # Generate the text image

    frames = []
    try:
        while True:
            combined_width = gif.width + text_width  # Create a new image with the combined width
            combined_image = Image.new("RGB", (combined_width, gif.height), "white")

            combined_image.paste(gif, (0, 0))  # Paste the GIF and text image onto the combined image
            combined_image.paste(text_image, (gif.width, 0))

            frames.append(combined_image)

            gif.seek(gif.tell() + 1)  # Move to the next frame
    except EOFError:
        pass  # End of sequence

    # Save the combined frames as a new GIF
    file_name = os.path.join(resource_path, f'mandelbrot_iter_{width}_{height}_{max_iterations}_{colour}_text.gif')
    frames[0].save(file_name, save_all=True, append_images=frames[1:], loop=0, duration=gif.info['duration'])
    return file_name


def mandelbrot_frame(width: int, height: int, iteration: int, max_iteration: int):
    """Create a Mandelbrot frame based on the specified iteration value. 

    This generates a single frame that will be included within the complete gif. 

    Parameters:
        width (int): The width of the complex number (c) grid. This can be thought of as the width of the returned gif.
        height (int): The height of the complex number (c) grid. This can be thought of as the height of the returned gif.
        iteration (int): The current maximum iteration value under consideration. 
        max_iteration (int): The maximum iteration value.

    Returns:
        (np.matrix): A numpy array containing a single frame of the Mandelbrot set.
    """
    img = np.zeros((width, height))  # Create a blank image 

    for x in range(width):  # Iterate through frame grid
        for y in range(height):

            c = complex(-2 + 2.5 * x / width, -1.25 + 2.5 * y / height)  # Convert pixel coordinate to complex number
            m = mandelbrot_calc(c, iteration)  # Compute the number of iterations
            color = 255 - int(m * 255 / max_iteration)  # Color depends on the number of iterations
            img[y, x] = color # Add value to the frame

    return img

def save_frame(frames_store: list, img: np.matrix, iteration: int, colour: str):
    """Saving a numpy matrix frame into an image frame to be used when creating the Mandelbrot gif. 

    Frame is saved in a temporary folder, such that its memory is volatile. 

    The method returns no value, as the list is passed by reference.

    Parameters:
        frames_store (list): A list containing the frames that will make up the gif. 
        img (np.matrix): The current frame as a matrix to be transformed into an image
        iteration (int): The current maximum iteration value under consideration. This is the value used to generate the frame parameter.
        colour (string): Specify the colour to be used for visualization. Colours available correspond to [matplotlib colourmaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
    """
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