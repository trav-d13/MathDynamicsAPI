from PIL import Image, ImageDraw, ImageFont
import textwrap

from enum import Enum

class Explanations(Enum):
    MANDELBROT_ITERATIVE = 'mandelbrot_iter'


def create_text_image(width: int, height: int, explanation: Explanations) -> Image.Image:
    text_image = Image.new("RGB", (width, height), "white")  # Create a new image with a white background
    draw = ImageDraw.Draw(text_image)
    font = ImageFont.load_default()

    # Define text wrapping
    lines = textwrap.wrap(explanations[explanation.value], width=40)
    y_text = 10  # Starting Y position for the text

    # Draw the text on the image
    for line in lines:
        draw.text((20, y_text), line, font=font, fill="black")
        y_text += 15  # Adjust line spacing

    return text_image


explanations = {
    'mandelbrot_iter': (
                "The Mandelbrot set is a set of complex numbers that produces a fractal when plotted. "
                "This set is named after Benoit B. Mandelbrot, who studied and popularized it in 1980. "
                "The boundary of the Mandelbrot set forms a complex and infinitely detailed fractal scape."
            )
}