.. chem-eng-solver documentation master file, created by
   sphinx-quickstart on Fri Nov 12 23:30:32 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
chem-eng-solver
===============

This package is intended to provide tools for solving common chemical engineering problems.
These types of problems typically involve solving one or more equations with a equivalent number of unknowns (if the problem is constrained), perhaps at two different reference points.
For example, suppose that you have an incompressible fluid in a tank at point 1 that is at atmospheric pressure and is flowing into a pool that is 30 feet lower in elevation.
What is the velocity of the fluid at point 2?
This type of question could be answered using the `Bernoulli principle <https://en.wikipedia.org/wiki/Bernoulli%27s_principle>`__:

.. math::

   \frac{1}{2} \rho v_{1}^2 + \rho g h_{1} + p_{1} = \frac{1}{2} \rho v_{2}^2 + \rho g h_{2} + p_{2}

where :math:`\rho` is the density of the fluid with velocity *v*, *h* is the height, *p* the pressure, and *i* the reference points 1 and 2.
If the problem were being solved analytically, you would cancel out terms, rearrange to solve for the unknown variable, and perform any required units conversions.
However thinking about this more problem more generically, the key requirements to solve these types of problems are:

* Flexibily defining input arguments and underlying equations so that they can easily be reused for whatever the specific problem statement requires.
* Selecting / applying an appropriate numerical method to solve 1 or more nonlinear equations / ODEs.
* Conveniently automated unit conversions to tranforms inputs into standard SI units for calculations as well as output results in the required units.

The goal of this package is to provide methods for accomplishing each of these tasks.


Installation
------------

Not released yet :) however the goal is to publish this package on `PyPI <https://pypi.org/>`__.


Examples
--------

See the ``examples`` directory for worked problems.


Development
-----------

This project is under development at: https://github.com/jonwilkey/chem-eng-solver.
To replicate the development environment, do the following:

1. Clone this repo to your local machine ``git clone git@github.com:jonwilkey/chem-eng-solver.git``.
2. Install poetry (see install instructions `here <https://github.com/python-poetry/poetry>`__.
3. Run ``poetry install``.


.. toctree::
   :maxdepth: 3
   :includehidden:
   :caption: Contents

   _apidoc/modules


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
