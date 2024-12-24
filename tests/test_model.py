import warnings

import pytest
import numpy as np
import thevenin as thev
from scipy.integrate import cumulative_trapezoid


@pytest.fixture(scope='function')
def dict_params():

    coeffs = np.array([84.6, -348.6, 592.3, -534.3, 275., -80.3, 12.8, 2.8])

    params = {
        'num_RC_pairs': 0,
        'soc0': 0.5,
        'capacity': 1.,
        'ce': 1.,
        'mass': 0.5,
        'isothermal': False,
        'Cp': 1150.,
        'T_inf': 300.,
        'h_therm': 12.,
        'A_therm': 1.,
        'ocv': lambda soc: np.polyval(coeffs, soc),
        'R0': lambda soc, T_cell: 0.05 + 0.05*soc - T_cell/1e4,
    }

    return params


@pytest.fixture(scope='function')
def model_0RC(dict_params):
    return thev.Model(dict_params)


@pytest.fixture(scope='function')
def model_1RC(dict_params):
    model = thev.Model(dict_params)

    model.num_RC_pairs = 1
    model.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
    model.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

    model.pre()

    return model


@pytest.fixture(scope='function')
def model_2RC(dict_params):
    model = thev.Model(dict_params)

    model.num_RC_pairs = 2
    model.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
    model.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1
    model.R2 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
    model.C2 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

    model.pre()

    return model


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
        _ = thev.Model(['wrong_type'])

    # invalid/excess key/value pairs
    with pytest.raises(ValueError):
        dict_params['fake'] = 'parameter'
        _ = thev.Model(dict_params)


def test_model_w_yaml_input(constant_steps, dynamic_current, dynamic_voltage,
                            dynamic_power):

    # using default file
    with pytest.warns(UserWarning):
        model = thev.Model()

    # using default file by name
    with pytest.warns(UserWarning):
        model = thev.Model('params')

    # using default file by name w/ extension
    with pytest.warns(UserWarning):
        model = thev.Model('params.yaml')

    soln = model.run(constant_steps)
    assert soln.success
    # assert any(soln.i_events)

    soln = model.run(dynamic_current)
    assert soln.success

    soln = model.run(dynamic_voltage)
    assert soln.success

    soln = model.run(dynamic_power)
    assert soln.success


def test_bad_yaml_inputs():

    # only .yaml extensions
    with pytest.raises(ValueError):
        _ = thev.Model('fake.fake')

    # file doesn't exist
    with pytest.raises(FileNotFoundError):
        _ = thev.Model('fake')


def test_preprocessor_raises(dict_params, dynamic_current):

    # missing attrs
    with pytest.raises(AttributeError):
        model = thev.Model(dict_params)

        model.num_RC_pairs = 1
        model.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4

        model.pre()

    with pytest.raises(AttributeError):
        model = thev.Model(dict_params)

        model.num_RC_pairs = 1
        model.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

        model.pre()

    # extra attrs - warning
    with pytest.warns(UserWarning):
        model = thev.Model(dict_params)

        model.num_RC_pairs = 1
        model.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
        model.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1
        model.R2 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4

        model.pre()

    # changed sv size w/o reset
    with pytest.raises(ValueError):
        model = thev.Model(dict_params)

        model.num_RC_pairs = 1
        model.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
        model.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

        model.pre(initial_state=False)

    # soln size inconsistent with model
    with pytest.raises(ValueError):
        model = thev.Model(dict_params)
        soln = model.run(dynamic_current)

        model.num_RC_pairs = 1
        model.R1 = lambda soc, T_cell: 0.01 + 0.01*soc - T_cell/3e4
        model.C1 = lambda soc, T_cell: 10. + 10.*soc - T_cell/3e1

        model.pre(initial_state=soln)


def test_preprocessing_initial_state_options(model_0RC, constant_steps):
    sv0 = model_0RC._sv0.copy()
    svdot0 = model_0RC._svdot0.copy()

    soln = model_0RC.run(constant_steps)
    assert np.allclose(sv0, model_0RC._sv0)
    assert np.allclose(svdot0, model_0RC._svdot0)

    model_0RC.pre(initial_state=soln)
    assert np.allclose(soln.y[-1], model_0RC._sv0)
    assert np.allclose(soln.yp[-1], model_0RC._svdot0)

    model_0RC.pre(initial_state=False)
    assert np.allclose(soln.y[-1], model_0RC._sv0)
    assert np.allclose(soln.yp[-1], model_0RC._svdot0)

    model_0RC.pre()
    assert np.allclose(sv0, model_0RC._sv0)
    assert np.allclose(svdot0, model_0RC._svdot0)


def test_run_step(model_2RC, constant_steps):

    sv0 = model_2RC._sv0.copy()
    svdot0 = model_2RC._svdot0.copy()

    stepsoln = model_2RC.run_step(constant_steps, 0)

    assert stepsoln.success
    assert not np.allclose(sv0, model_2RC._sv0)
    assert not np.allclose(svdot0, model_2RC._svdot0)

    model_2RC.pre()

    assert np.allclose(sv0, model_2RC._sv0)
    assert np.allclose(svdot0, model_2RC._svdot0)


def test_run_options(model_0RC, constant_steps):
    sv0 = model_0RC._sv0.copy()
    svdot0 = model_0RC._svdot0.copy()

    soln = model_0RC.run(constant_steps)
    assert np.allclose(sv0, model_0RC._sv0)
    assert np.allclose(svdot0, model_0RC._svdot0)

    soln = model_0RC.run(constant_steps, reset_state=False)
    assert np.allclose(soln.y[-1], model_0RC._sv0)
    assert np.allclose(soln.yp[-1], model_0RC._svdot0)


def test_model_w_multistep_experiment(model_0RC, model_1RC, model_2RC,
                                      constant_steps):

    soln = model_0RC.run(constant_steps)
    assert soln.success
    assert any(status == 2 for status in soln.status)

    soln = model_1RC.run(constant_steps)
    assert soln.success
    assert any(status == 2 for status in soln.status)

    soln = model_2RC.run(constant_steps)
    assert soln.success
    assert any(status == 2 for status in soln.status)


def test_model_w_dynamic_current(model_0RC, model_1RC, model_2RC,
                                 dynamic_current):

    soln = model_0RC.run(dynamic_current)
    assert soln.success

    soln = model_1RC.run(dynamic_current)
    assert soln.success

    soln = model_2RC.run(dynamic_current)
    assert soln.success


def test_model_w_dynamic_voltage(model_0RC, model_1RC, model_2RC,
                                 dynamic_voltage):

    soln = model_0RC.run(dynamic_voltage)
    assert soln.success

    soln = model_1RC.run(dynamic_voltage)
    assert soln.success

    soln = model_2RC.run(dynamic_voltage)
    assert soln.success


def test_model_w_dynamic_power(model_0RC, model_1RC, model_2RC,
                               dynamic_power):

    soln = model_0RC.run(dynamic_power)
    assert soln.success

    soln = model_1RC.run(dynamic_power)
    assert soln.success

    soln = model_2RC.run(dynamic_power)
    assert soln.success


def test_resting_experiment(model_2RC):

    expr = thev.Experiment()
    expr.add_step('current_A', 0., (100., 1.))

    soln = model_2RC.run(expr)

    assert soln.success
    assert np.allclose(soln.vars['voltage_V'], soln.vars['voltage_V'][0])


def test_current_sign_convention(model_2RC, constant_steps):

    soln = model_2RC.run(constant_steps)

    discharge = soln.get_steps(0)
    assert all(np.diff(discharge.vars['voltage_V']) < 0.)

    charge = soln.get_steps(2)
    assert all(np.diff(charge.vars['voltage_V']) > 0.)


def test_constant_V_shift_w_constant_R0(model_0RC, constant_steps):

    model_0RC.R0 = lambda soc, T_cell: 1e-2
    model_0RC.pre()

    soln = model_0RC.run(constant_steps)

    discharge = soln.get_steps(0)
    ocv = model_0RC.ocv(discharge.vars['soc'])
    assert np.allclose(ocv - 1e-2, discharge.vars['voltage_V'])

    charge = soln.get_steps(2)
    ocv = model_0RC.ocv(charge.vars['soc'])
    assert np.allclose(ocv + 1e-2, charge.vars['voltage_V'])


def test_isothermal_flag(model_2RC, constant_steps):

    # with heat on
    model_2RC.isothermal = False
    model_2RC.pre()

    soln = model_2RC.run(constant_steps)
    assert soln.vars['temperature_K'].max() > model_2RC.T_inf
    assert all(soln.vars['temperature_K'] >= model_2RC.T_inf)

    # with heat off
    model_2RC.isothermal = True
    model_2RC.pre()

    soln = model_2RC.run(constant_steps)
    assert np.allclose(soln.vars['temperature_K'], model_2RC.T_inf)


@pytest.mark.filterwarnings("ignore:.*default parameter file.*:UserWarning")
def test_coulombic_efficiency():

    model_100 = thev.Model()
    model_100.soc0 = 1.
    model_100.ce = 1.
    model_100.pre()

    model_80 = thev.Model()
    model_80.soc0 = 1.
    model_80.ce = 0.8
    model_80.pre()

    expr = thev.Experiment()
    expr.add_step('current_C', 0.05, (3600.*30., 10.), limits=('soc', 0.))
    expr.add_step('current_C', -0.05, (3600.*30., 10.), limits=('soc', 1.))

    # check discharge capacity / charge capacity ~ 1.0
    soln_100 = model_100.run(expr)
    assert all(soln_100.success)

    dis = soln_100.get_steps(0)
    chg = soln_100.get_steps(1)

    cap_dis = cumulative_trapezoid(dis.vars['current_A'], dis.vars['time_h'],
                                   initial=0.)
    cap_chg = cumulative_trapezoid(chg.vars['current_A'], chg.vars['time_h'],
                                   initial=0.)

    assert round(abs(cap_dis).max() / abs(cap_chg).max(), 1) == 1.0

    # check discharge capacity / charge capacity ~ 0.8
    soln_80 = model_80.run(expr)
    assert all(soln_80.success)

    dis = soln_80.get_steps(0)
    chg = soln_80.get_steps(1)

    cap_dis = cumulative_trapezoid(dis.vars['current_A'], dis.vars['time_h'],
                                   initial=0.)
    cap_chg = cumulative_trapezoid(chg.vars['current_A'], chg.vars['time_h'],
                                   initial=0.)

    assert round(abs(cap_dis).max() / abs(cap_chg).max(), 1) == 0.8


def test_mutable_warning():
    from thevenin._model import short_warn

    with warnings.catch_warnings(record=True) as report:
        warnings.simplefilter('ignore')
        short_warn("This is a test warning.")

    assert len(report) == 0


def test_detected_warning():
    from thevenin._model import short_warn

    with pytest.warns(UserWarning):
        short_warn("This is a test warning")


def test_custom_format():
    from thevenin._model import formatwarning, short_warn

    with warnings.catch_warnings(record=True) as report:
        warnings.simplefilter('always')
        short_warn("This is a test warning.", Warning)

    args = (
        report[0].message,
        report[0].category,
        report[0].filename,
        report[0].lineno,
        report[0].line,
    )

    # ensure the same inputs, remove  any \n, \t, etc.
    custom = formatwarning(*args).strip()
    original = warnings.formatwarning(*args).strip()

    # custom format works
    assert custom == "[thevenin Warning] This is a test warning."

    # warnings from warnings.warn not impacted by custom format
    assert original != "[thevenin Warning] This is a test warning."
