import pytest
from app.fractals.mandelbrot import mandelbrot_calc

@pytest.mark.parametrize("c, max_iteration, expected", [
    (0, 100, 100),
    (2, 100, 1),
    (-1 + 0.2j, 100, 100),
    (-0.1 + 0.65j, 10, 10)
])
def test_mandelbrot(c, max_iteration, expected):
    assert mandelbrot_calc(c, max_iteration) == expected
