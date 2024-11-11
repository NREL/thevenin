import pytest
import numpy as np
import thevenin as thev


@pytest.fixture(scope='function')
def expr():
    return thev.Experiment()


def test_initialization(expr):

    assert expr._steps == []
    assert expr._kwargs == []
    assert expr._options == {}

    assert expr.steps == []
    assert expr.num_steps == 0


def test_tspan_construction(expr):

    # Using linspace
    expr.add_step('current_A', 0., (10., 7))

    step = expr._steps[-1]
    assert np.allclose(step['tspan'], np.linspace(0., 10., 7))

    # Using arange - evenly divisible
    expr.add_step('current_A', 0., (10., 2.))

    step = expr._steps[-1]
    assert np.allclose(step['tspan'], np.array([0., 2., 4., 6., 8., 10.]))

    # Using arange - not evenly divisible
    expr.add_step('current_A', 0., (10., 3.))

    step = expr._steps[-1]
    assert np.allclose(step['tspan'], np.array([0., 3., 6., 9., 10.]))


def test_add_step(expr):

    # wrong mode
    with pytest.raises(ValueError):
        expr.add_step('current_C', 1., (3600., 1.))

    # wrong tspan length
    with pytest.raises(ValueError):
        expr.add_step('current_A', 1., (0., 3600., 150))

    # wrong tspan type
    with pytest.raises(TypeError):
        expr.add_step('current_A', 1., (3600., '1'))

    # bad limits name
    with pytest.raises(ValueError):
        expr.add_step('current_A', 1., (3600., 1.), limits=('fake', 3.))

    # bad limits length
    with pytest.raises(ValueError):
        expr.add_step('current_A', 1., (3600., 1.),
                      limits=('voltage_V', 3., 'soc'))

    # bad limits value type
    with pytest.raises(TypeError):
        expr.add_step('current_A', 1., (3600., 1.), limits=('voltage_V', '3'))

    # test current and linspace construction
    expr.add_step('current_A', 1., (3600., 150))
    step = expr.steps[0]

    assert expr.num_steps == 1
    assert np.allclose(step['tspan'], np.linspace(0., 3600., 150))

    # test voltage and arange construction
    expr.add_step('voltage_V', 4., (3600., 1.))
    step = expr.steps[1]

    assert expr.num_steps == 2
    assert np.allclose(step['tspan'], np.arange(0., 3601., 1., dtype=float))

    # test power construction
    expr.add_step('power_W', 1., (3600., 1.))

    assert expr.num_steps == 3

    # test limit keyword
    expr.add_step('current_A', 1., (3600., 1.), limits=('voltage_V', 3.))

    assert expr.steps[-1]['limits'] == ('voltage_V', 3.)

    # test dynamic load
    expr.add_step('current_A', lambda t: 1., (3600., 1.))
    step = expr.steps[-1]

    assert callable(step['value'])


def test_print_steps(expr):

    # no error when empty
    expr.print_steps()
    assert True

    # also works with step(s)
    expr.add_step('current_A', 1., (3600., 1.))
    expr.print_steps()
    assert True
