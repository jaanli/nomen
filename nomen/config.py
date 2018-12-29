import yaml
import argparse
import itertools
import collections
import copy
import json
import pathlib
import addict


_GLOBAL_PARSER = argparse.ArgumentParser()


class Config(object):
  """Create addict from yaml or dict; maybe create command-line flags."""
  def __init__(self, dictionary, make_args=True):
    config = addict.Dict(dictionary)
    self._config = _replace_variables(config)
    if make_args:
      self._add_args()

  def _add_args(self):
    for path in _walk(self._config):
      default_value = path.pop()
      arg_name = '/'.join(path)
      _add_argument(_GLOBAL_PARSER, arg_name, default_value)

  def parse_args(self, args=None):
    result, unparsed_args = _GLOBAL_PARSER.parse_known_args(args)
    for arg_name, val in vars(result).items():
      path = arg_name.split("/")
      last_key = path.pop()
      cfg = self._config
      for key in path:
        cfg = cfg[key]
      cfg[last_key] = val
    if unparsed_args and unparsed_args != ['test']:
      raise Warning('Unparsed args: %s' % unparsed_args)

  def __getattr__(self, item):
    return self._config.__getattr__(item)
  
  def __getitem__(self, key):
    return self._config.__getitem__(key)

  def __setitem__(self, name, value):
    self._config.__setitem__(name, value)

  def __setattr__(self, name, value):
    if name == '_config':
      self.__dict__[name] = value
    else:
      self._config.__setattr__(name, value)

  def __str__(self):
    return yaml.dump(self._config.to_dict(), default_flow_style=False)


def _walk(dictionary, key_path=[]):
  """Iterate through a nested dictionary."""
  for key, value in dictionary.items():
    if isinstance(value, dict):
      for path in _walk(value, key_path=[key]):
        yield path
    else:
      yield key_path + [key, value]


def _replace_variables(dictionary):
  """Replace environment variables in a nested dict."""
  for path in _walk(dictionary):
    value = path.pop()
    if isinstance(value, str) and value.startswith('$'):
      file_path = value[1:].split('/')
      env_var = file_path.pop(0)
      expanded = pathlib.os.environ[env_var]
      value = pathlib.os.path.join(expanded, '/'.join(file_path))
      value = pathlib.Path(value)
    key = '/'.join(path)
    last_key = path.pop()
    sub_dict = dictionary
    for key in path:
      sub_dict = sub_dict[key]
    sub_dict[last_key] = value
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
  elif type(default_value) == list:
    parser.add_argument('--' + arg_name,
                        nargs='+',
                        const=None,
                        default=default_value,
                        type=type(default_value[0]))
  else:
    parser.add_argument('--' + arg_name,
                        default=default_value,
                        nargs='?',
                        const=True,
                        type=type(default_value))
