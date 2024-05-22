# FastAPI
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from contextlib import asynccontextmanager

# Rate Limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Database
from sqlmodel import Session, select
from app.database import get_session, init_db, User, fetch_or_create_user_key, validate_key

# API Models
from app.models import CreateUser

# Fractals
from app.fractals.mandelbrot import mandelbrot_iteration_generation, mandelbrot_iteration_generation_with_text

limiter = Limiter(key_func=get_remote_address)

# TODO Include environmental variable that will void API key checks to allow for local development


@asynccontextmanager
async def lifespan(app: FastAPI):  # Initialize database structure
    await init_db()  # Initialize the database at startup

    yield  # Control returns to FastAPI to run normally


app = FastAPI(lifespan=lifespan)

security = HTTPBearer()

# Link limiter to FastAPI
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
async def root():
    return {"message": "Hello World"}

async def validate_api_key(api_key: HTTPAuthorizationCredentials = Depends(security),
                           session = Depends(get_session)):
    flag = await validate_key(session=session,
                        api_key=api_key.credentials)
    if flag:
        return api_key.credentials
    else:
         raise HTTPException(status_code=403, detail="User API key not found")
    



@app.post("/api_key")
@limiter.limit("2/minute")
async def generate_api_key(request: Request, user_data: CreateUser, session: Session = Depends(get_session)):
    """
    Generate or fetch an API key for a user.
    
    This endpoint accepts user data, checks if the user already exists in the database,
    and returns the user's API key. If the user does not exist, it creates a new user and
    generates a new API key for them.

    Parameters:
      user_data (CreateUser): The user information required to create or fetch the API key.
      session (Session): The database session dependency.

    Returns:
      (JSON): A JSON object containing the API key.
    """
    key = await fetch_or_create_user_key(session=session, user_data=user_data)
    return {"api_key": key}


@app.get("/mandelbrot")
@limiter.limit("2/minute")
async def mandelbrot_set(request: Request, width: int, height: int, max_iterations: int, colour: str, explanation: bool, api_key: str = Depends(validate_api_key)):
    """Mandelbrot set endpoint, specifically tailored to showcase gradually finer details of the set based on the maximum iteration. 

    Parameters:
        width (int): The width of the complex number (c) grid. This can be thought of as the width of the returned gif.
        height (int): The height of the complex number (c) grid. This can be thought of as the height of the returned gif.
        max_iterations (int): The maximum iteration value
        colour (string): Specify the colour to be used for visualization. Colours available correspond to [matplotlib colourmaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
    
    Returns:
        (FileResponse): A file response of file type `.gif`
    """
    if explanation:
        mandelbrot_iter_gif_path = mandelbrot_iteration_generation_with_text(width=width,
                                                          height=height,
                                                          max_iterations=max_iterations,
                                                          colour=colour)
    else:
        mandelbrot_iter_gif_path = mandelbrot_iteration_generation(width=width,
                                                          height=height,
                                                          max_iterations=max_iterations,
                                                          colour=colour)
    
    return FileResponse(mandelbrot_iter_gif_path)