# nomen
Lightweight configuration with command line flags.

[Nomen](https://en.wikipedia.org/wiki/Nomen_nudum) or _nomen nudum_ means _naked name_ in taxonomy. The goal of this package is to provide transparent configuration and command line flags.

Hence, it is heavily based on [TensorFlow's flags](https://github.com/tensorflow/tensorflow/blob/ad5a583e7b9f095d1d0151fd24f9e5055d5dd6ab/tensorflow/python/platform/flags.py).

### Install
```
pip install nomen
```

### Usage
```
# main.py
import nomen

cfg = nomen.Config()
cfg.define_float('learning_rate', 0.5, 'This is the learning rate')
with cfg.scope('model'):
  cfg.define_float('name', 'bob', 'Name of the model')

# Parse any command line flags, otherwise set values to defaults
cfg.parse_args()

# Hierarchical option parsing means it will search one level higher
if the key is not found in the leaf node
print cfg['model/learning_rate']

# Options can be set via the command line, e.g. `python main.py --model/learning_rate 0.01`

# Get only part of the option tree
print cfg['model']

# Update the options
cfg.update({'model': {'name': 'alex'}})

# Write the nested dict as JSON
import json
with open('options.cfg', 'wb') as f:
  json.dump(cfg.json, f, indent=2)
```

### Testing
```
# create a symbolic link to the package for testing
pip install -e i
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
* do not subclass from dict for pathdict
* when indexing subtree, return a pathdict!
* think about jinja2 templates? i.e. to merge multiple files? e.g. << ./global_config.yml
* make global options work?
* be able to iterate through dict?
