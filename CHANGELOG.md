# thevenin Changelog

## [Unreleased](https://github.com/NREL/thevenin)

### New Features

### Optimizations

### Bug Fixes

### Breaking Changes

## [v0.2.1](https://github.com/NREL/thevenin/tree/v0.2.1)

### Bug Fixes
- Use `for` loops in `Solution` post-processing if arrays are incompatible ([#17](https://github.com/NREL/thevenin/pull/17))

## [v0.2.0](https://github.com/NREL/thevenin/tree/v0.2.0)

### New Features
- Allow the `CycleSolution` to append more solutions after it has been initialized ([#9](https://github.com/NREL/thevenin/pull/9))
- New `Prediction` and `TransientState` classes for an improved interface to Kalman filters ([#8](https://github.com/NREL/thevenin/pull/8))
- Added hysteresis (`hsyt`) to the model, controlled with `gamma` and `M_hyst` parameters ([#7](https://github.com/NREL/thevenin/pull/7))

### Optimizations
- Make `num_RC_pairs` read-only so now `pre` only needs to be called to reset the state ([#13](https://github.com/NREL/thevenin/pull/13))
- Use `np.testing` where possible in tests for more informative fail statements ([#10](https://github.com/NREL/thevenin/pull/10))
- Pre-initialize `CycleSolution` arrays rather than appending lists, much faster ([#7](https://github.com/NREL/thevenin/pull/7))
- Introduce `ExitHandler` to ensure `plt.show` doesn't get registered more than once, replaces `show_plot` option in `Solutions` ([#7](https://github.com/NREL/thevenin/pull/7))

### Bug Fixes
- Change to using `_T_ref` to scale the temperature equation since `T_inf` can be modified ([#12](https://github.com/NREL/thevenin/pull/12))
- Hyseteresis voltage was missing in `Qgen` heat transfer terms, now incorporated ([#11](https://github.com/NREL/thevenin/pull/11))

### Breaking Changes
- New hysteresis option means users will need to update old `params` inputs to also include `gamma` and `M_hyst` ([#7](https://github.com/NREL/thevenin/pull/7))

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

