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
print('Model learning rate', cfg.model.learning_rate)
print('Eval options', cfg['eval_data'])
```

Configurations define command line arguments:
```
python main.py \
	--model/learning_rate 0.001 \
	--log /tmp \
	--model/turbo
```

Configurations are portable - save and load using yaml:
```
with open('config.yml', 'w') as f:
  f.write(str(cfg))
```


### Install
```
pip install nomen
```

### Reasons for not using
It is easy to write subtle bugs with YAML parsing a boolean incorrectly. c.f. [problems with YAML](https://arp242.net/weblog/yaml_probably_not_so_great_after_all.html). TODO: switch `load` to `safe_load`. Consider switching to StrictYAML.


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
* How to design global options? In yaml?
