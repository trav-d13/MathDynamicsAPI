import pytest
from app.fractals.mandelbrot import mandelbrot_calc, mandelbrot_frame, mandelbrot_iteration_generation
from unittest.mock import MagicMock
import numpy as np
import app

@pytest.mark.parametrize("c, max_iteration, expected", [
    (0, 100, 100),
    (2, 100, 1),
    (-1 + 0.2j, 100, 100),
    (-0.1 + 0.65j, 10, 10)
])
def test_mandelbrot(c, max_iteration, expected):
    """Tests the above known values according to the Mandelbrot calculation based on iterations"""
    assert mandelbrot_calc(c, max_iteration) == expected


def test_mandelbrot_frame():
    """Tests the shape of the produce frame is consistent with expectations"""
    width, height, iteration, max_iteration = 10, 10, 10, 50
    result = mandelbrot_frame(width, height, iteration, max_iteration)
    assert result.shape == (width, height)  # Correct shape


def test_mandelbrot_iteration_generation(mocker):
    """Patches used to create independence for this test, to focus on iteration generation"""
    mocker.patch('app.fractals.mandelbrot.mandelbrot_frame', return_value=np.zeros((10, 10)))  # Replaces the mandelbrot_frame call
    mocker.patch('app.fractals.mandelbrot.save_frame')  # Replaces save_frame() method
    mocker.patch('imageio.mimsave')  # Replaces imageio.mimsave as this use I/O operations

    width, height, max_iterations, colour = 10, 10, 100, 'viridis'
    result = mandelbrot_iteration_generation(width, height, max_iterations, colour)
    
    assert 'app/resources/' in result  # Check the path essentials
    assert app.fractals.mandelbrot.save_frame.call_count == (max_iterations - 2) // 10 + 1  # Check the number of times save_frame was called
    assert app.fractals.mandelbrot.imageio.mimsave.called  # Check this method was called