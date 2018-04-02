import yaml
from .path_dict import PathDict
import os
import argparse
import itertools
import collections
import copy
import json


_GLOBAL_PARSER = argparse.ArgumentParser()


class Config(object):
  def __init__(self, yaml_path=None, dictionary=None, parsed=False):
    self._parsed = parsed
    assert yaml_path is None or dictionary is None
    if yaml_path is not None:
      with open(yaml_path, 'r') as f:
        config = PathDict(yaml.load(f))
    elif dictionary is not None:
      config = PathDict(dictionary)
    else:
      raise Exception('Must provide dictionary or path to yaml config!')
    self._config = _replace_variables(config)
    if not self._parsed:
      self._add_arguments()
      self._parse_args()

  def from_yaml(yaml_path):
    self._config = _replace_variables(config)

  def _add_arguments(self):
    for path in _walk(self._config):
      default_value = path.pop()
      arg_name = '/'.join(path)
      _add_argument(_GLOBAL_PARSER, arg_name, default_value)

  def _parse_args(self):
    result, unparsed = _GLOBAL_PARSER.parse_known_args()
    for arg_name, val in vars(result).items():
      self._config[arg_name] = val
    self._parsed = True
    if unparsed and unparsed != ['test']:
      raise Warning('Unparsed args: %s' % unparsed)

  def __getitem__(self, key):
    return self._config[key]

  def __setitem__(self, key, value):
    self._config[key] = value

  def update(self, dictionary):
    dictionary = PathDict(dictionary)
    dictionary = _replace_variables(dictionary)
    for key, value in dictionary.items():
      self._config[key] = value

  def copy(self):
    return copy.deepcopy(self)

  def __str__(self):
    return yaml.dump(dict(self._config), default_flow_style=False)

  def update_from_yaml(self, path):
    with open(path, 'r') as f:
      config = PathDict(yaml.load(f))
    config = _replace_variables(config)
    for path in _walk(config):
      value = path.pop()
      key = '/'.join(path)
      try:
        self[key] = value
      except KeyError:
        print('Warning: no key %s in config. Not updated!' % key)


def _walk(dictionary, key_path=[]):
  """Iterate through a nested dictionary."""
  for key, value in dictionary.items():
    if isinstance(value, dict):
      for path in _walk(value, key_path=[key]):
        yield path
    else:
      yield key_path + [key, value]


def _replace_variables(dictionary):
  assert isinstance(dictionary, PathDict)
  for path in _walk(dictionary):
    value = path.pop()
    if isinstance(value, str) and value.startswith('$'):
      file_path = value[1:].split('/')
      env_var = file_path.pop(0)
      expanded = os.environ[env_var]
      value = os.path.join(expanded, '/'.join(file_path))
    key = '/'.join(path)
    dictionary[key] = value
  return dictionary


def _add_argument(parser, arg_name, default_value):
  """Add arguments to the global parser. Null values inferred as strings."""
  if isinstance(default_value, bool):
    def str2bool(v):
      return v.lower() in ('true', 't', '1')
    parser.add_argument('--' + arg_name,
                        nargs='?',
                        const=True,
                        default=default_value,
                        type=str2bool)
  elif default_value == None:
    parser.add_argument('--' + arg_name,
                        nargs='?',
                        const=True,
                        default=None,
                        type=str)
  else:
    parser.add_argument('--' + arg_name,
                        default=default_value,
                        nargs='?',
                        const=True,
                        type=type(default_value))
