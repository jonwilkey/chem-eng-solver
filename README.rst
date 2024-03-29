===============
chem-eng-solver
===============

.. image:: https://github.com/jonwilkey/chem-eng-solver/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/jonwilkey/chem-eng-solver/actions/workflows/ci.yml
   :alt: Github CI tests action status

.. image:: https://readthedocs.org/projects/chem-eng-solver/badge/?version=latest
   :target: https://chem-eng-solver.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


This package is intended to provide tools for solving common chemical engineering problems.
These types of problems typically involve solving one or more equations with a equivalent number of unknowns (if the problem is constrained), perhaps at two different reference points.
For example, suppose that you have an incompressible fluid in a tank at point 1 that is at atmospheric pressure and is flowing into a pool that is 30 feet lower in elevation.
What is the velocity of the fluid at point 2?
This type of question could be answered using the `Bernoulli principle <https://en.wikipedia.org/wiki/Bernoulli%27s_principle>`__:

.. image:: https://render.githubusercontent.com/render/math?math=%5Cfrac%7B1%7D%7B2%7D%20%5Crho%20v_1%5E2%20%2B%20%5Crho%20g%20h_1%20%2B%20p_1%20%3D%20%5Cfrac%7B1%7D%7B2%7D%20%5Crho%20v_2%5E2%20%2B%20%5Crho%20g%20h_2%20%2B%20p_2

where *rho* is the density of the fluid with velocity *v*, *h* is the height, *p* the pressure, and *i* the reference points 1 and 2.
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

See the `examples <https://github.com/jonwilkey/chem-eng-solver/tree/main/examples>`__ directory for worked problems.


Development
-----------

To setup this package for development, do the following:

1. Clone this repo to your local machine ``git clone git@github.com:jonwilkey/chem-eng-solver.git``.
2. Install poetry (see install instructions `here <https://github.com/python-poetry/poetry>`__.
3. Run ``poetry install``.

Documentation
-------------

Available here: https://chem-eng-solver.readthedocs.io/
