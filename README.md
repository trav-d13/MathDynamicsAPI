# MathDynamicsAPI
A mathematical pattern API generator, returning patterns in GIF format... suitable for an awesome README.md visual

## API
### Local FastAPI Deployment
1. Navigate to project root directory
2. Ensure the virtual environment is active (linux/mac) `source {env_name}/bin/activate` or (windows) `{env_name}\Scripts\activate`
3. Run `fastapi dev app/main.py`

### Local Docker Deployment
1. Naviate to the root directory
2. Create the Docker container `docker build -t math_dynamics`
3. Run the docker container `docker run -p 8000:8000 math_dynamics`

## Notebooks
In order to explore more pattern, or try out different versions please use the `notebooks/` directory. 
In order to create a suitable environment containing all dependencies, please follow the below steps:
1. Naivate into the root project directory
2. Create a virtual environment (venv) using `python -m venv {env_name}`
3. Activate the environment (linux/mac) `source {env_name}/bin/activate` or (windows) `{env_name}\Scripts\activate`
4. Install all dependencies `pip install -r requirements.txt`
5. Create a Jupyter Notebooks kernel `python -m ipykernel install --user --name=myenv`
6. Any additional dependencies you install in the virtual environment are now available to your notebooks when using this kernel


## Available Patterns

### Mandelbrot Set Pattern
![Mandelbrot iteration](notebooks/pattern_samples/mandelbrot_iteration.gif)  

![Mandelbrot Zoom](notebooks/pattern_samples/mandelbrot_zoom.gif)

### Julia Set Pattern
![Julia Set](notebooks/pattern_samples/julia_set_variation.gif)