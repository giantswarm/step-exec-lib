[![build](https://github.com/giantswarm/step-exec-lib/actions/workflows/main.yml/badge.svg)](https://github.com/giantswarm/step-exec-lib/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/giantswarm/step-exec-lib/branch/master/graph/badge.svg)](https://codecov.io/gh/giantswarm/step-exec-lib)
[![PyPI Version](https://img.shields.io/pypi/v/step-exec-lib.svg)](https://pypi.org/project/step-exec-lib/)
[![Python Versions](https://img.shields.io/pypi/pyversions/step-exec-lib.svg)](https://pypi.org/project/step-exec-lib/)
[![Apache License](https://img.shields.io/badge/license-apache-blue.svg)](https://pypi.org/project/step-exec-lib/)

# step-exec-lib

A simple library to easily orchestrate a set of Steps into a filtrable pipeline.

**Disclaimer**: docs are still work-in-progress!

Each step provides a defined set of actions. When a pipeline is execute first all `pre` actions
of all Steps are executed, then `run` actions and so on. Steps can provide labels, so
you can easily disable/enable a subset of steps.

A ready to use python app template. Based on `pipenv`.
