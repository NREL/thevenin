import warnings

import numpy as np
import numpy.testing as npt

import pytest
import thevenin as thev
import matplotlib.pyplot as plt


def dict_params(num_RC_pairs: int = 0) -> dict:

    coeffs = np.array([84.6, -348.6, 592.3, -534.3, 275., -80.3, 12.8, 2.8])

    params = {
        'num_RC_pairs': num_RC_pairs,
        'soc0': 0.5,
        'capacity': 1.,
        'ce': 1.,
        'gamma': 0.,
        'mass': 0.5,
        'isothermal': False,
        'Cp': 1150.,
        'T_inf': 300.,
        'h_therm': 12.,
        'A_therm': 1.,
        'ocv': lambda soc: np.polyval(coeffs, soc),
        'M_hyst': lambda soc: 0.,
        'R0': lambda soc, T_cell: 0.05 + 0.05*soc - T_cell/1e4,
    }

    for j in range(1, num_RC_pairs + 1):
        params['R' + str(j)] = lambda soc, T: 0.01 + 0.01*soc - T/3e4
        params['C' + str(j)] = lambda soc, T: 10. + 10.*soc - T/3e1

    return params


@pytest.fixture(scope='function')  # cannot be module b/c appends
def soln():

    warnings.filterwarnings('ignore')

    sim = thev.Simulation()

    expr = thev.Experiment()
    expr.add_step('current_C', 1., (3600., 1.), limits=('voltage_V', 3.))
    expr.add_step('current_A', 0., (300., 1.))
    expr.add_step('current_C', -1., (3600., 1.), limits=('voltage_V', 4.3))
    expr.add_step('current_A', 0., (300., 1.))

    soln = sim.run(expr)

    return soln


@pytest.fixture(scope='function')
def rest():

    warnings.filterwarnings('ignore')

    sim = thev.Simulation()

    rest = thev.Experiment()
    rest.add_step('current_A', 0., (300., 1.))

    soln = sim.run(rest)

    return soln


def test_step_and_cycle_solutions(soln):

    # solvetime works
    step_soln = soln.get_steps(0)
    assert step_soln.solvetime

    # bad plot
    with pytest.raises(KeyError):
        step_soln.plot('fake', 'plot')

    # plots w/ and w/o units
    with plt.ioff():
        step_soln.plot('soc', 'soc')
        step_soln.plot('time_h', 'voltage_V')
        plt.close('all')

    # solvetime works and times stacked correctly
    cycle_soln = soln.get_steps((0, 1))
    assert cycle_soln.solvetime
    assert all(np.diff(cycle_soln.t) >= 0.)

    # bad plot
    with pytest.raises(KeyError):
        cycle_soln.plot('fake', 'plot')

    # plots w/ and w/o units
    with plt.ioff():
        cycle_soln.plot('soc', 'soc')
        cycle_soln.plot('time_h', 'voltage_V')
        plt.close('all')


def test_cycle_from_single_step(soln):

    step0 = soln.get_steps(0)
    assert isinstance(step0, thev.StepSolution)

    cycle = thev.CycleSolution(step0)
    assert isinstance(cycle, thev.CycleSolution)


def test_append_errors(soln):

    # append wrong size solution (different num_RC_pairs)
    sim0 = thev.Simulation(dict_params(0))
    sim1 = thev.Simulation(dict_params(1))

    expr = thev.Experiment()
    expr.add_step('current_C', 1., (3600., 1.), limits=('voltage_V', 3.))

    soln0 = sim0.run(expr)
    soln1 = sim1.run(expr)
    with pytest.raises(ValueError):
        soln0.append_soln(soln1)

    # only works with StepSolution and CycleSolution
    sim = soln._sim
    with pytest.raises(TypeError):
        soln.append_soln(sim)


def test_append_step_soln(soln):

    t_orig = soln.vars['time_s']
    V_orig = soln.vars['voltage_V']

    step0 = soln.get_steps(0)

    soln.append_soln(step0, t_shift=0.)
    assert len(soln.success) == 5

    t_new_times = t_orig[-1] + step0.vars['time_s']
    t_append = np.concatenate([t_orig, t_new_times])
    npt.assert_allclose(soln.vars['time_s'], t_append)

    V_append = np.concatenate([V_orig, step0.vars['voltage_V']])
    npt.assert_allclose(soln.vars['voltage_V'], V_append)


def test_append_cycle_soln(soln):

    t_orig = soln.vars['time_s']
    V_orig = soln.vars['voltage_V']

    soln.append_soln(soln, t_shift=0.)
    assert len(soln.success) == 8

    t_new_times = t_orig[-1] + t_orig
    t_append = np.concatenate([t_orig, t_new_times])
    npt.assert_allclose(soln.vars['time_s'], t_append)

    V_append = np.concatenate([V_orig, V_orig])
    npt.assert_allclose(soln.vars['voltage_V'], V_append)


def test_append_w_events(rest, soln):

    rest.append_soln(soln)
    assert len(rest.t_events) == 2
