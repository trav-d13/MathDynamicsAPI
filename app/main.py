# FastAPI
from fastapi import FastAPI, Request, Depends
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

# Endpoint Models
from pydantic import BaseModel, EmailStr

# Rate Limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Database
from sqlmodel import Session, select
from database import get_session, init_db
from models import User

# Fractals
from app.fractals.mandelbrot import mandelbrot_iteration_generation

limiter = Limiter(key_func=get_remote_address)

# TODO Include environmental variable that will void API key checks to allow for local development

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):  # Initialize database structure
    await init_db()  # Initialize the database at startup
    yield  # Control returns to FastAPI to run normally

app.router.lifespan_handler = lifespan

# Link limiter to FastAPI
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Data Models
class CreateUser(BaseModel):
    name: str
    email: EmailStr
    country: str #TODO Add validator to check Country is valid



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api_key")
async def generate_api_key(user_data: CreateUser, session: Session = Depends(get_session)):
    # TODO Create new user
    # TODO return API key to user
    pass


@app.get("/mandelbrot")
@limiter.limit("2/minute")
async def mandelbrot_set(request: Request, width: int, height: int, max_iterations: int, colour: str):
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