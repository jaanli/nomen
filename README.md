# nomen
[![Build Status](https://travis-ci.org/altosaar/nomen.svg?branch=master)](https://travis-ci.org/altosaar/nomen)

[Nomen](https://en.wikipedia.org/wiki/Nomen_nudum) :goat: or _nomen nudum_ means _naked name_ in taxonomy. The goal of this package is to provide python programs with highly-readable, minimalist configuration and command line flags based on YAML syntax.

Define a configuration with YAML syntax and any environment variables:

In file `config.yml`:
```
model:
  learning_rate: 0.1
  turbo: false
variational:
  learning_rate: 0.3

data:
  shape: &shape [28, 28, 1]
eval_data:
  shape: *shape

log: $LOG  ## will be replaced by the $LOG environment variable
```

Use the configuration!

File `main.py`
```
import nomen
cfg = nomen.Config('config.yml')
print('Model options', cfg['model'])
print('Eval options', cfg['eval_data'])
```

Configurations define command line arguments:
```
python main.py \
	--model/learning_rate 0.001 \
	--log /tmp \
	--model/turbo
```


### Install
```
pip install nomen
```


### Testing
```
# create a symbolic link to the package for testing
pip install -e .
# run all the tests
pytest
```

### Pushing to pypi
```
# build the package, possibly with a new version.py
python setup.py sdist bdist_wheel
# test the built package
pip install -i https://testpypi.python.org/pypi nomen
# upload to pypi
twine upload dist/*
# test again
pip install nomen --no-cache-dir
```


### Acknowledgments
Many thanks to Rajesh - this is based around his advice and ideas, which I've found it very useful.

### Contributing
Pull requests and issues welcome. Please help

### Wishlist / todo
* do not subclass from dict for pathdict. Composition over inheritance!
* when indexing subtree, return a pathdict!
* think about jinja2 templates? i.e. to merge multiple files? e.g. << ./global_config.yml
* make global options work?
* be able to iterate through dict?
