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
    mandelbrot_iter_gif_path = mandelbrot_iteration_generation(width=width,
                                                          height=height,
                                                          max_iterations=max_iterations,
                                                          colour=colour)
    
    return FileResponse(mandelbrot_iter_gif_path)