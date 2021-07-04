# chem-eng-solver

This package is intended to provide tools for solving common chemical engineering problems.
These types of problems typically involve solving one or more equations with a equivalent number of unknowns (if the problem is constrained), perhaps at two different reference points.
For example, suppose that you have an incompressible fluid in a tank at point 1 that is at atmospheric pressure and is flowing into a pool that is 30 feet lower in elevation.
What is the velocity of the fluid at point 2?
This type of question could be answered using the [Bernoulli principle](https://en.wikipedia.org/wiki/Bernoulli%27s_principle):

$$
\frac{1}{2} \rho v_1^2 + \rho g h_1 + p_1 = \frac{1}{2} \rho v_2^2 + \rho g h_2 + p_2
$$

where $$rho$$ is the density of the fluid with velocity $$v_i$$, $$h_i$$ is the height, $$p_i$$ the pressure, and $$i$$ the reference points 1 and 2.
If the problem were being solved analytically, you would cancel out terms ($$p_1 = p_2$$ so that drops out, $$v_1 = 0$$, etc.) and rearrange to solve for the unknown variable ($$v_2$$) and perform any required units conversions.
However thinking about this more problem more generically, the key requirements to solve these types of problems are:

* Flexibily defining input arguments and underlying equations so that they can easily be reused for whatever the specific problem statement requires.
* Selecting/applying an appropriate numerical method to solve 1 or more nonlinear equations / ODEs.
* Conveniently automated unit conversions to tranforms inputs into standard SI units for calculations as well as output results in the required units.

The goal of this package is to provide methods for accomplishing each of these tasks.

# Installation

Not released yet :) however the goal is to publish this package on [PyPI](https://pypi.org/) so that it can be installed via `pip`.

# Examples

See the `examples` directory for worked problems.

# Development

Clone this repo using git, then activate a virtual environment, for example with [venv](https://docs.python.org/3/library/venv.html):

```bash
$ python3 -m venv /path/to/desired/venv/chem-eng-solver/
$ source /path/to/desired/venv/chem-eng-solver/bin/activate
```

To install all of the dependencies necessary for development, run:

```bash
pip install -e /path/to/desired/venv/chem-eng-solver
```
# Documentation

WIP
