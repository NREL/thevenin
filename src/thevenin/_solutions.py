from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

import textwrap
from copy import deepcopy

import atexit
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import cumulative_trapezoid

from ._ida_solver import IDAResult

if TYPE_CHECKING:  # pragma: no cover
    from ._model import Model


class BaseSolution(IDAResult):
    """Base solution."""

    def __init__(self) -> None:
        """
        The base solution class is a parent class to both the StepSolution
        and CycleSolution classes. Inheriting from this class gives each
        solution instance a 'vars' dictionary, access to the 'plot' method,
        and ensures that the slicing of the solution vector into 'vars' is
        consistent between all solutions.

        """

        self.vars = {}

    def __repr__(self) -> str:  # pragma: no cover
        """
        Return a readable repr string.

        Returns
        -------
        readable : str
            A console-readable instance representation.

        """

        classname = self.__class__.__name__

        def wrap_string(label: str, value: list, width: int):
            if isinstance(value, Iterable):
                value = list(value)
            else:
                value = [value]

            indent = ' '*(len(label) + 1)

            if classname == 'StepSolution' and len(value) == 1:
                text = label + f"{value[0]!r}"
            else:
                text = label + "[" + ", ".join(f"{v!r}" for v in value) + "]"

            return textwrap.fill(text, width=width, subsequent_indent=indent)

        data = [
            wrap_string('    success=', self.success, 79),
            wrap_string('    status=', self.status, 79),
            wrap_string('    nfev=', self.nfev, 79),
            wrap_string('    njev=', self.njev, 79),
            wrap_string('    vars=', self.vars.keys(), 79),
        ]

        summary = f"    solvetime={self.solvetime},"
        for d in data:
            summary += f"\n{d},"

        readable = f"{classname}(\n{summary}\n)"

        return readable

    def plot(self, x: str, y: str, show_plot: bool = True, **kwargs) -> None:
        """
        Plot any two variables in 'vars' against each other.

        Parameters
        ----------
        x : str
            A variable key in 'vars' to be used for the x-axis.
        y : str
            A variable key in 'vars' to be used for the y-axis.
        show_plot : bool, optional
            For non-interactive environments only. When True (default) this
            registers `plt.show()` to run at the end of the program. If False,
            you must call `plt.show()` manually.
        **kwargs : dict, optional
            Keyword arguments to pass through to `plt.plot()`. For more info
            please refer to documentation for `maplotlib.pyplot.plot()`.

        Returns
        -------
        None.

        """

        plt.figure()
        plt.plot(self.vars[x], self.vars[y], **kwargs)

        if '_' in x:
            variable, units = x.split('_')
            xlabel = variable.capitalize() + ' [' + units + ']'
        else:
            xlabel = x

        if '_' in y:
            variable, units = y.split('_')
            ylabel = variable.capitalize() + ' [' + units + ']'
        else:
            ylabel = y

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        if show_plot and not plt.isinteractive():
            atexit.register(plt.show)

    def _to_dict(self) -> None:
        """
        Fills the 'vars' dictionary by slicing the SolverReturn solution
        states. Users should generally only access the solution via 'vars'
        since names are more intuitive than interpreting 'y' directly.

        Returns
        -------
        None.

        """

        model = self._model
        ptr = model._ptr

        time = self.t

        soc = self.y[:, ptr['soc']]
        T_cell = self.y[:, ptr['T_cell']]*model.T_inf
        eta_j = self.y[:, ptr['eta_j']]
        voltage = self.y[:, ptr['V_cell']]

        try:
            ocv = model.ocv(soc)
            R0 = model.R0(soc, T_cell)

            assert isinstance(ocv, np.ndarray)
            assert isinstance(R0, np.ndarray)
            assert ocv.shape == soc.shape
            assert R0.shape == soc.shape

        except (TypeError, AssertionError):

            ocv = np.empty_like(soc)
            R0 = np.empty_like(soc)
            for i in range(soc.size):
                ocv[i] = model.ocv(soc[i])
                R0[i] = model.R0(soc[i], T_cell[i])

        current = -(voltage - ocv + np.sum(eta_j, axis=1)) / R0
        capacity = cumulative_trapezoid(-current, x=time/3600., initial=0.)

        # stored time
        self.vars['time_s'] = time
        self.vars['time_min'] = time / 60.
        self.vars['time_h'] = time / 3600.

        # from state variables
        self.vars['soc'] = soc
        self.vars['temperature_K'] = T_cell
        self.vars['voltage_V'] = voltage

        # post-processed variables
        self.vars['current_A'] = current
        self.vars['power_W'] = current*voltage
        self.vars['capacity_Ah'] = soc[0]*model.capacity + capacity
        self.vars['eta0_V'] = current*R0

        for j, eta in enumerate(eta_j.T, start=1):
            self.vars['eta' + str(j) + '_V'] = eta


class StepSolution(BaseSolution):
    """Single-step solution."""

    def __init__(self, model: Model, ida_soln: IDAResult,
                 timer: float) -> None:
        """
        A solution instance for a single experimental step.

        Parameters
        ----------
        model : Model
            The model instance that was run to produce the solution.
        ida_soln : IDAResult
            The unformatted solution returned by IDASolver.
        timer : float
            Amount of time it took for IDASolver to perform the integration.

        """

        super().__init__()

        self._model = deepcopy(model)

        self.message = ida_soln.message
        self.success = ida_soln.success
        self.status = ida_soln.status

        self.t = ida_soln.t
        self.y = ida_soln.y
        self.yp = ida_soln.yp

        self.i_events = ida_soln.i_events
        self.t_events = ida_soln.t_events
        self.y_events = ida_soln.y_events
        self.yp_events = ida_soln.yp_events

        self.nfev = ida_soln.nfev
        self.njev = ida_soln.njev

        self._timer = timer

        self._to_dict()

    @property
    def solvetime(self) -> str:
        """
        Print a statement specifying how long IDASolver spent integrating.

        Returns
        -------
        solvetime : str
            An f-string with the solver integration time in seconds.

        """
        return f"{self._timer:.3f} s"


class CycleSolution(BaseSolution):
    """All-step solution."""

    def __init__(self, *soln: StepSolution, t_shift: float = 1e-3) -> None:
        """
        A solution instance with all experiment steps stitch together into
        a single cycle.

        Parameters
        ----------
        *soln : StepSolution
            All unpacked StepSolution instances to stitch together. The given
            steps should be given in the same sequential order that they were
            run.
        t_shift : float
            Time (in seconds) to shift step solutions by when stitching them
            together. If zero the end time of each step overlaps the starting
            time of its following step. The default is 1e-3.

        """

        super().__init__()

        self._solns = soln
        self._model = soln[0]._model

        sv_size = self._model._sv0.size

        self.message = []
        self.success = []
        self.status = []

        self.t = np.empty([0])
        self.y = np.empty([0, sv_size])
        self.yp = np.empty([0, sv_size])

        self.t_events = None
        self.y_events = None
        self.yp_events = None

        self.nfev = []
        self.njev = []

        self._timers = []

        for soln in self._solns:
            if self.t.size > 0:
                shift_t = self.t[-1] + soln.t + t_shift
            else:
                shift_t = soln.t

            if soln.t_events and self.t.size > 0:
                shift_t_events = self.t[-1] + soln.t_events + t_shift
            elif soln.t_events:
                shift_t_events = soln.t_events

            self.message.append(soln.message)
            self.success.append(soln.success)
            self.status.append(soln.status)

            self.t = np.hstack([self.t, shift_t])
            self.y = np.vstack([self.y, soln.y])
            self.yp = np.vstack([self.yp, soln.yp])

            if soln.t_events:
                if self.t_events is None:
                    self.t_events = shift_t_events
                    self.y_events = soln.y_events
                    self.yp_events = soln.yp_events
                else:
                    self.t_events = np.hstack([self.t_events, shift_t_events])
                    self.y_events = np.vstack([soln.y_events])
                    self.yp_events = np.vstack([soln.yp_events])

            self.nfev.append(soln.nfev)
            self.njev.append(soln.njev)

            self._timers.append(soln._timer)

        self._to_dict()

    @property
    def solvetime(self) -> str:
        """
        Print a statement specifying how long IDASolver spent integrating.

        Returns
        -------
        solvetime : str
            An f-string with the total solver integration time in seconds.

        """
        return f"{sum(self._timers):.3f} s"

    def get_steps(self, idx: int | tuple) -> StepSolution | CycleSolution:
        """
        Return a subset of the solution.

        Parameters
        ----------
        idx : int | tuple
            The step index (int) or first/last indices (tuple) to return.

        Returns
        -------
        :class:`StepSolution` | :class:`CycleSolution`
            The returned solution subset. A StepSolution is returned if 'idx'
            is an int, and a CycleSolution will be returned for the range of
            requested steps when 'idx' is a tuple.

        """

        if isinstance(idx, int):
            return deepcopy(self._solns[idx])
        elif isinstance(idx, (tuple, list)):
            solns = self._solns[idx[0]:idx[1] + 1]
            return CycleSolution(*solns)
