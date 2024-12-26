# thevenin Changelog

## [Unreleased](https://github.com/NREL/thevenin)

### New Features

### Optimizations

### Bug Fixes

### Breaking Changes

## [v0.1.2](https://github.com/NREL/thevenin/tree/v0.1.2)

### New Features
- Added Coulombic efficiency (`ce`) as a parameter option ([#4](https://github.com/NREL/thevenin/pull/4))

### Optimizations
- Bounded exponential input to avoid overflow warnings inside the sigmoid function of `loadfns.Ramp2Constant` ([#6](https://github.com/NREL/thevenin/pull/6))

### Bug Fixes
- `*Solution.plot()` now has a `show_plot` option to register `plt.show()` and block at the end of a program ([#5](https://github.com/NREL/thevenin/pull/5)). This keeps figures from auto-closing at the end of scripts run in non-interactive environments. Interactive environments (IPython, Jupyter Notebook) are not affected. When set to `False`, users running in non-interactive environments must manually call `plt.show()`. The default is `True`.

### Breaking Changes
- New Coulombic efficiency option means users will need to update old `params` inputs to also include `ce`

## [v0.1.1](https://github.com/NREL/thevenin/tree/v0.1.1)

### Bug Fixes
- Corrected some docstrings

## [v0.1.0](https://github.com/NREL/thevenin/tree/v0.1.0)
This is the first official release of `thevenin`. Main features/capabilities are listed below.

### Features
- Support for any number of RC pairs
- Run constant or dynamic loads with current, voltage, or power control
- Parameters have temperature and state of charge dependence
- Experiment limits to trigger switching between steps
- Multi-limit support (end at voltage, time, etc. - whichever occurs first)

### Notes
- Implemented `pytest` with full package coverage
- Source/binary distributions available on [PyPI](https://pypi.org/project/thevenin)
- Documentation available on [Read the Docs](https://thevenin.readthedocs.io/)

