# nomen
Lightweight configuration with command line flags.

The goal of this package is to subsume tensorflow flags. One time I wrote forty five bugs using the tf.app.flags module, so I knew things had to change.

Hence, it is heavily based on [TensorFlow's flags](https://github.com/tensorflow/tensorflow/blob/ad5a583e7b9f095d1d0151fd24f9e5055d5dd6ab/tensorflow/python/platform/flags.py).

### Install
```
pip install nomen
```

### Usage
```
import nomen

cfg = nomen.Config()
cfg.define_float('learning_rate', 0.5, 'This is the learning rate')
with cfg.scope('model'):
  cfg.define_float('name', 'bob', 'Name of the model')
cfg.parse_args()

# Hierarchical option parsing means it will search one level higher
if the key is not found in the leaf node
print cfg['model/learning_rate']

# Get only part of the option tree
print cfg['model']

# Update the options
cfg.update({'model': {'name': 'alex'}})

# Write the nested dict as JSON
import json
with open('options.cfg', 'wb') as f:
  json.dump(cfg.json, f, indent=2)
```

### Contributing
Please help
