import pytest
import thevenin as thev

import numpy as np
import numpy.testing as npt


def test_ramp():

    demand = thev.loadfns.Ramp(5., 10.)

    tp = np.linspace(0, 20, 25)
    yp = 5.*tp + 10.

    npt.assert_allclose(demand(tp), yp)


def test_ramp_2_constant():

    # m cannot equal 0
    with pytest.raises(ValueError):
        _ = thev.loadfns.Ramp2Constant(0., 1.)

    # m cannot equal inf
    with pytest.raises(ValueError):
        _ = thev.loadfns.Ramp2Constant(-np.inf, 1.)

    # m > 0 with b >= step is invalid
    with pytest.raises(ValueError):
        _ = thev.loadfns.Ramp2Constant(10., 0.)

    # m < 0 with b <= step is invalid
    with pytest.raises(ValueError):
        _ = thev.loadfns.Ramp2Constant(-10., -5., -7.)

    # non-positive sharpness
    with pytest.raises(ValueError):
        _ = thev.loadfns.Ramp2Constant(6./1e-3, 6., sharpness=0.)

    with pytest.raises(ValueError):
        _ = thev.loadfns.Ramp2Constant(6./1e-3, 6., sharpness=-100.)

    # positive ramp
    demand = thev.loadfns.Ramp2Constant(6./1e-3, 6.)

    tp = np.linspace(0, 1e-3, 10)
    yp = 6./1e-3*tp + 0.

    npt.assert_allclose(demand(tp), yp, atol=1e-8)

    tp = np.linspace(1e-3, 100, 100)
    yp = 6.*np.ones_like(tp)

    npt.assert_allclose(demand(tp), yp)

    # negative ramp
    demand = thev.loadfns.Ramp2Constant(-6./1e-3, -6.)

    tp = np.linspace(0, 1e-3, 10)
    yp = -6./1e-3*tp + 0.

    npt.assert_allclose(demand(tp), yp, atol=1e-8)

    tp = np.linspace(1e-3, 100, 100)
    yp = -6.*np.ones_like(tp)

    npt.assert_allclose(demand(tp), yp)


def test_step_function():

    # Inputs must be 1D
    tp = np.array([[0, 1, 5]])
    yp = np.array([-1, 0, 1])
    with pytest.raises(ValueError):
        _ = thev.loadfns.StepFunction(tp, yp)

    # Inputs must be same length
    tp = np.array([0, 1])
    yp = np.array([-1, 0, 1])
    with pytest.raises(ValueError):
        _ = thev.loadfns.StepFunction(tp, yp)

    # tp must be strictly increasing
    tp = np.array([0, -1, 5])
    yp = np.array([-1, 0, 1])
    with pytest.raises(ValueError):
        _ = thev.loadfns.StepFunction(tp, yp)

    tp = np.array([0, 1, 5])
    yp = np.array([-1, 0, 1])

    demand = thev.loadfns.StepFunction(tp, yp, -np.inf)

    t_test = np.array([-10, 0.5, 4, 10])
    y_test = np.array([-np.inf, -1, 0, 1])

    assert np.isnan(demand(np.nan))
    npt.assert_allclose(demand(t_test), y_test, equal_nan=True)

    demand = thev.loadfns.StepFunction(tp, yp, -np.inf, ignore_nan=True)

    assert demand(np.nan) == yp[-1]


def test_ramped_steps():

    # Inputs must be 1D
    tp = np.array([[0, 1, 5]])
    yp = np.array([-1, 0, 1])
    with pytest.raises(ValueError):
        _ = thev.loadfns.RampedSteps(tp, yp, 1.)

    # Inputs must be same length
    tp = np.array([0, 1])
    yp = np.array([-1, 0, 1])
    with pytest.raises(ValueError):
        _ = thev.loadfns.RampedSteps(tp, yp, 1.)

    # t_ramp must be strictly positive
    tp = np.array([0, 1, 5])
    yp = np.array([-1, 0, 1])
    with pytest.raises(ValueError):
        _ = thev.loadfns.RampedSteps(tp, yp, 0.)

    # tp must be strictly increasing
    tp = np.array([0, -1, 5])
    yp = np.array([-1, 0, 1])
    with pytest.raises(ValueError):
        _ = thev.loadfns.RampedSteps(tp, yp, 1.)

    tp = np.array([0, 1, 5])
    yp = np.array([-1, 5, 10])

    demand = thev.loadfns.RampedSteps(tp, yp, 1e-3)

    t_test = np.array([-1, 0.5, 3, 10])
    y_test = np.array([0, -1, 5, 10])

    npt.assert_allclose(demand(t_test), y_test)

    def ramp(t): return 0. + (-1. - 0.) / 1e-3 * t
    t_test = np.linspace(0, 1e-3, 10)

    npt.assert_allclose(demand(t_test), ramp(t_test))

    def ramp(t): return -1. + (5. - -1.) / 1e-3 * (t - 1.)
    t_test = np.linspace(1, 1 + 1e-3, 10)

    npt.assert_allclose(demand(t_test), ramp(t_test))

    def ramp(t): return 5. + (10. - 5.) / 1e-3 * (t - 5.)
    t_test = np.linspace(5, 5 + 1e-3, 10)

    npt.assert_allclose(demand(t_test), ramp(t_test))
