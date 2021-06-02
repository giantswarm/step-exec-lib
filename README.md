[![build](https://github.com/giantswarm/steps-exec-lib/workflows/build/badge.svg)](https://github.com/giantswarm/steps-exec-lib/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/giantswarm/steps-exec-lib/branch/master/graph/badge.svg)](https://codecov.io/gh/giantswarm/steps-exec-lib)
[![PyPI Version](https://img.shields.io/pypi/v/steps-exec-lib.svg)](https://pypi.org/project/steps-exec-lib/)
[![Python Versions](https://img.shields.io/pypi/pyversions/steps-exec-lib.svg)](https://pypi.org/project/steps-exec-lib/)
[![Apache License](https://img.shields.io/badge/license-apache-blue.svg)](https://pypi.org/project/steps-exec-lib/)

# step-exec-lib

A simple library to easily orchestrate a set of Steps into a filtrable pipeline.

**Disclaimer**: docs are still work-in-progress!

Each step provides a defined set of actions. When a pipeline is execute first all `pre` actions
of all Steps are executed, then `run` actions and so on. Steps can provide labels, so
you can easily disable/enable a subset of steps.

A ready to use python app template. Based on `pipenv`.
