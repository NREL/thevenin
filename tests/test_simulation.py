import pytest
import thevenin as thev

import numpy as np
import numpy.testing as npt

from scipy.integrate import cumulative_trapezoid


@pytest.fixture(scope='function')
def dict_params():

    coeffs = np.array([84.6, -348.6, 592.3, -534.3, 275., -80.3, 12.8, 2.8])

    params = {
        'num_RC_pairs': 0,
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

    return params


@pytest.fixture(scope='function')
def sim_0RC(dict_params):
    return thev.Simulation(dict_params)


@pytest.fixture(scope='function')
def sim_1RC(dict_params):
    sim = thev.Simulation(dict_params)

    sim.num_RC_pairs = 1
    sim.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
    sim.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

    sim.pre()

    return sim


@pytest.fixture(scope='function')
def sim_2RC(dict_params):
    sim = thev.Simulation(dict_params)

    sim.num_RC_pairs = 2
    sim.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
    sim.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1
    sim.R2 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
    sim.C2 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

    sim.pre()

    return sim


@pytest.fixture(scope='function')
def constant_steps():
    expr = thev.Experiment()
    expr.add_step('current_A', 1., (3600., 1.), limits=('voltage_V', 3.))
    expr.add_step('current_C', 0., (600., 1.))
    expr.add_step('current_A', -1., (3600., 1.), limits=('voltage_V', 4.3))
    expr.add_step('voltage_V', 4.3, (600., 1.))
    expr.add_step('power_W', 1., (600., 1.), limits=('voltage_V', 3.))

    return expr


@pytest.fixture(scope='function')
def dynamic_current():
    def load(t): return np.sin(2.*np.pi*t / 120.)

    expr = thev.Experiment()
    expr.add_step('current_A', load, (600., 1.))

    return expr


@pytest.fixture(scope='function')
def dynamic_voltage():
    def load(t): return 3.8 + 10e-3*np.sin(2.*np.pi*t / 120.)

    expr = thev.Experiment()
    expr.add_step('voltage_V', load, (600., 1.))

    return expr


@pytest.fixture(scope='function')
def dynamic_power():
    def load(t): return np.sin(2.*np.pi*t / 120.)

    expr = thev.Experiment()
    expr.add_step('power_W', load, (600., 1.))

    return expr


def test_bad_initialization(dict_params):

    # wrong params type
    with pytest.raises(TypeError):
        _ = thev.Simulation(['wrong_type'])

    # invalid/excess key/value pairs
    with pytest.raises(ValueError):
        dict_params['fake'] = 'parameter'
        _ = thev.Simulation(dict_params)


def test_sim_w_yaml_input(constant_steps, dynamic_current, dynamic_voltage,
                          dynamic_power):

    # using default file
    with pytest.warns(UserWarning):
        sim = thev.Simulation()

    # using default file by name
    with pytest.warns(UserWarning):
        sim = thev.Simulation('params')

    # using default file by name w/ extension
    with pytest.warns(UserWarning):
        sim = thev.Simulation('params.yaml')

    soln = sim.run(constant_steps)
    assert soln.success
    # assert any(soln.i_events)

    soln = sim.run(dynamic_current)
    assert soln.success

    soln = sim.run(dynamic_voltage)
    assert soln.success

    soln = sim.run(dynamic_power)
    assert soln.success


def test_bad_yaml_inputs():

    # only .yaml extensions
    with pytest.raises(ValueError):
        _ = thev.Simulation('fake.fake')

    # file doesn't exist
    with pytest.raises(FileNotFoundError):
        _ = thev.Simulation('fake')


def test_preprocessor_raises(dict_params, dynamic_current):

    # missing attrs
    with pytest.raises(AttributeError):
        sim = thev.Simulation(dict_params)

        sim.num_RC_pairs = 1
        sim.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4

        sim.pre()

    with pytest.raises(AttributeError):
        sim = thev.Simulation(dict_params)

        sim.num_RC_pairs = 1
        sim.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

        sim.pre()

    # extra attrs - warning
    with pytest.warns(UserWarning):
        sim = thev.Simulation(dict_params)

        sim.num_RC_pairs = 1
        sim.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
        sim.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1
        sim.R2 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4

        sim.pre()

    # changed sv size w/o reset
    with pytest.raises(ValueError):
        sim = thev.Simulation(dict_params)

        sim.num_RC_pairs = 1
        sim.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
        sim.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

        sim.pre(initial_state=False)

    # soln size inconsistent with sim
    with pytest.raises(ValueError):
        sim = thev.Simulation(dict_params)
        soln = sim.run(dynamic_current)

        sim.num_RC_pairs = 1
        sim.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
        sim.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

        sim.pre(initial_state=soln)


def test_preprocessing_initial_state_options(sim_0RC, constant_steps):
    sv0 = sim_0RC._sv0.copy()
    svdot0 = sim_0RC._svdot0.copy()

    soln = sim_0RC.run(constant_steps)
    npt.assert_allclose(sv0, sim_0RC._sv0)
    npt.assert_allclose(svdot0, sim_0RC._svdot0)

    sim_0RC.pre(initial_state=soln)
    npt.assert_allclose(soln.y[-1], sim_0RC._sv0)
    npt.assert_allclose(soln.yp[-1], sim_0RC._svdot0)

    sim_0RC.pre(initial_state=False)
    npt.assert_allclose(soln.y[-1], sim_0RC._sv0)
    npt.assert_allclose(soln.yp[-1], sim_0RC._svdot0)

    sim_0RC.pre()
    npt.assert_allclose(sv0, sim_0RC._sv0)
    npt.assert_allclose(svdot0, sim_0RC._svdot0)


def test_run_step(sim_2RC, constant_steps):

    sv0 = sim_2RC._sv0.copy()
    svdot0 = sim_2RC._svdot0.copy()

    stepsoln = sim_2RC.run_step(constant_steps, 0)

    assert stepsoln.success
    assert not np.allclose(sv0, sim_2RC._sv0)
    assert not np.allclose(svdot0, sim_2RC._svdot0)

    sim_2RC.pre()

    npt.assert_allclose(sv0, sim_2RC._sv0)
    npt.assert_allclose(svdot0, sim_2RC._svdot0)


def test_run_options(sim_0RC, constant_steps):
    sv0 = sim_0RC._sv0.copy()
    svdot0 = sim_0RC._svdot0.copy()

    soln = sim_0RC.run(constant_steps)
    npt.assert_allclose(sv0, sim_0RC._sv0)
    npt.assert_allclose(svdot0, sim_0RC._svdot0)

    soln = sim_0RC.run(constant_steps, reset_state=False)
    npt.assert_allclose(soln.y[-1], sim_0RC._sv0)
    npt.assert_allclose(soln.yp[-1], sim_0RC._svdot0)


def test_sim_w_multistep_experiment(sim_0RC, sim_1RC, sim_2RC, constant_steps):

    soln = sim_0RC.run(constant_steps)
    assert soln.success
    assert any(status == 2 for status in soln.status)

    soln = sim_1RC.run(constant_steps)
    assert soln.success
    assert any(status == 2 for status in soln.status)

    soln = sim_2RC.run(constant_steps)
    assert soln.success
    assert any(status == 2 for status in soln.status)


def test_sim_w_dynamic_current(sim_0RC, sim_1RC, sim_2RC, dynamic_current):

    soln = sim_0RC.run(dynamic_current)
    assert soln.success

    soln = sim_1RC.run(dynamic_current)
    assert soln.success

    soln = sim_2RC.run(dynamic_current)
    assert soln.success


def test_sim_w_dynamic_voltage(sim_0RC, sim_1RC, sim_2RC, dynamic_voltage):

    soln = sim_0RC.run(dynamic_voltage)
    assert soln.success

    soln = sim_1RC.run(dynamic_voltage)
    assert soln.success

    soln = sim_2RC.run(dynamic_voltage)
    assert soln.success


def test_sim_w_dynamic_power(sim_0RC, sim_1RC, sim_2RC, dynamic_power):

    soln = sim_0RC.run(dynamic_power)
    assert soln.success

    soln = sim_1RC.run(dynamic_power)
    assert soln.success

    soln = sim_2RC.run(dynamic_power)
    assert soln.success


def test_resting_experiment(sim_2RC):

    expr = thev.Experiment()
    expr.add_step('current_A', 0., (100., 1.))

    soln = sim_2RC.run(expr)

    assert soln.success
    npt.assert_allclose(
        soln.vars['voltage_V'],
        soln.vars['voltage_V'][0],
    )


def test_current_sign_convention(sim_2RC, constant_steps):

    soln = sim_2RC.run(constant_steps)

    discharge = soln.get_steps(0)
    assert all(np.diff(discharge.vars['voltage_V']) < 0.)

    charge = soln.get_steps(2)
    assert all(np.diff(charge.vars['voltage_V']) > 0.)


def test_constant_V_shift_w_constant_R0(sim_0RC, constant_steps):

    sim_0RC.R0 = lambda soc, T_cell: 1e-2
    sim_0RC.pre()

    soln = sim_0RC.run(constant_steps)

    discharge = soln.get_steps(0)
    ocv = sim_0RC.ocv(discharge.vars['soc'])
    npt.assert_allclose(
        discharge.vars['voltage_V'],
        ocv - 1e-2,
        rtol=1e-3,
    )

    charge = soln.get_steps(2)
    ocv = sim_0RC.ocv(charge.vars['soc'])
    npt.assert_allclose(
        charge.vars['voltage_V'],
        ocv + 1e-2,
        rtol=1e-3,
    )


def test_isothermal_flag(sim_2RC, constant_steps):

    # with heat on
    sim_2RC.isothermal = False
    sim_2RC.pre()

    soln = sim_2RC.run(constant_steps)
    assert soln.vars['temperature_K'].max() > sim_2RC.T_inf
    assert all(soln.vars['temperature_K'] >= sim_2RC.T_inf)

    # with heat off
    sim_2RC.isothermal = True
    sim_2RC.pre()

    soln = sim_2RC.run(constant_steps)
    npt.assert_allclose(soln.vars['temperature_K'], sim_2RC.T_inf)


@pytest.mark.filterwarnings("ignore:.*default parameter file.*:UserWarning")
def test_coulombic_efficiency():

    sim_100 = thev.Simulation()
    sim_100.soc0 = 1.
    sim_100.ce = 1.
    sim_100.pre()

    sim_80 = thev.Simulation()
    sim_80.soc0 = 1.
    sim_80.ce = 0.8
    sim_80.pre()

    expr = thev.Experiment()
    expr.add_step('current_C', 0.05, (3600.*30., 10.), limits=('soc', 0.))
    expr.add_step('current_C', -0.05, (3600.*30., 10.), limits=('soc', 1.))

    # check discharge capacity / charge capacity ~ 1.0
    soln_100 = sim_100.run(expr)
    assert all(soln_100.success)

    dis = soln_100.get_steps(0)
    chg = soln_100.get_steps(1)

    cap_dis = cumulative_trapezoid(dis.vars['current_A'], dis.vars['time_h'],
                                   initial=0.)
    cap_chg = cumulative_trapezoid(chg.vars['current_A'], chg.vars['time_h'],
                                   initial=0.)

    assert round(abs(cap_dis).max() / abs(cap_chg).max(), 1) == 1.0

    # check discharge capacity / charge capacity ~ 0.8
    soln_80 = sim_80.run(expr)
    assert all(soln_80.success)

    dis = soln_80.get_steps(0)
    chg = soln_80.get_steps(1)

    cap_dis = cumulative_trapezoid(dis.vars['current_A'], dis.vars['time_h'],
                                   initial=0.)
    cap_chg = cumulative_trapezoid(chg.vars['current_A'], chg.vars['time_h'],
                                   initial=0.)

    assert round(abs(cap_dis).max() / abs(cap_chg).max(), 1) == 0.8


@pytest.mark.filterwarnings("ignore:.*default parameter file.*:UserWarning")
def test_hysteresis():

    sim_woh = thev.Simulation()  # without hysteresis
    sim_woh.soc0 = 1.
    sim_woh.pre()

    assert sim_woh.gamma == 0.
    assert sim_woh.M_hyst(0.) == 0.

    sim_wh = thev.Simulation()  # with hysteresis
    sim_wh.soc0 = 1.
    sim_wh.gamma = 50.
    sim_wh.M_hyst = lambda soc: 0.07
    sim_wh.pre()

    assert sim_wh.gamma == 50.
    assert sim_wh.M_hyst(0.) == 0.07

    discharge = thev.Experiment(max_step=10.)
    discharge.add_step('current_C', 1., (3600., 10.), limits=('soc', 0.5))
    discharge.add_step('current_A', 0., (600., 10.))

    charge = thev.Experiment(max_step=10.)
    charge.add_step('current_C', -1., (3600., 10.), limits=('soc', 0.8))
    charge.add_step('current_A', 0., (600., 10.))

    soln = sim_woh.run(discharge, reset_state=False)
    npt.assert_allclose(soln.vars['hysteresis_V'], 0., atol=1e-9)
    npt.assert_almost_equal(
        soln.vars['voltage_V'][-1],
        sim_woh.ocv(0.5),
        decimal=2,
    )

    soln = sim_woh.run(charge, reset_state=False)
    npt.assert_allclose(soln.vars['hysteresis_V'], 0., atol=1e-9)
    npt.assert_almost_equal(
        soln.vars['voltage_V'][-1],
        sim_woh.ocv(0.8),
        decimal=2,
    )

    soln = sim_wh.run(discharge, reset_state=False)
    npt.assert_allclose(soln.vars['hysteresis_V'][-1], -0.07, rtol=1e-4)
    npt.assert_almost_equal(
        soln.vars['voltage_V'][-1],
        sim_wh.ocv(0.5) - 0.07,
        decimal=2,
    )

    soln = sim_wh.run(charge, reset_state=False)
    npt.assert_allclose(soln.vars['hysteresis_V'][-1], 0.07, rtol=1e-4)
    npt.assert_almost_equal(
        soln.vars['voltage_V'][-1],
        sim_wh.ocv(0.8) + 0.07,
        decimal=2,
    )

    # Check current is unaffected by hysteresis
    step = soln.get_steps(0)
    npt.assert_allclose(
        step.vars['current_A'],
        -1.*sim_wh.capacity,
        rtol=1e-3,
    )
