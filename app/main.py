# FastAPI
from fastapi import FastAPI
from fastapi.responses import FileResponse

# Fractals
from app.fractals.mandelbrot import mandelbrot_iteration_generation


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/mandelbrot")
async def mandelbrot_set(width: int, height: int, max_iterations: int, colour: str):
    """Mandelbrot set endpoint, specifically tailored to showcase gradually finer details of the set based on the maximum iteration. 

    Parameters:
        width (int): The width of the complex number (c) grid. This can be thought of as the width of the returned gif.
        height (int): The height of the complex number (c) grid. This can be thought of as the height of the returned gif.
        max_iterations (int): The maximum iteration value
        colour (string): Specify the colour to be used for visualization. Colours available correspond to [matplotlib colourmaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
    
    Returns:
        (FileResponse): A file response of file type `.gif`
    """
    mandelbrot_iter_gif_path = mandelbrot_iteration_generation(width=width,
                                                          height=height,
                                                          max_iterations=max_iterations,
                                                          colour=colour)
    
    return FileResponse(mandelbrot_iter_gif_path)