import yaml
import argparse
import json
import pathlib
import addict
import os
import json


_GLOBAL_PARSER = argparse.ArgumentParser()


class MyAddict(addict.Dict):
  def __missing__(self, name):
    raise AttributeError(f'Attribute "{name}" does not exist!')


class Config(MyAddict):
  """Create addict from yaml or dict; maybe create command-line flags."""
  def __init__(self, dictionary, make_args=True):
    super()
    dictionary = _replace_variables(dictionary)
    self.update(MyAddict(dictionary))
    if make_args:
      self._add_args()

  def _add_args(self):
    for path in _walk(self):
      default_value = path.pop()
      arg_name = '/'.join(path)
      _add_argument(_GLOBAL_PARSER, arg_name, default_value)

  def parse_args(self, args=None):
    result, unparsed_args = _GLOBAL_PARSER.parse_known_args(args)
    for arg_name, val in vars(result).items():
      path = arg_name.split("/")
      last_key = path.pop()
      cfg = self
      for key in path:
        cfg = cfg[key]
      cfg[last_key] = val
    if unparsed_args and unparsed_args != ['test']:
      raise Warning('Unparsed args: %s' % unparsed_args)

  def update(self, *args, **kwargs):
    super().update(*args, **kwargs)
    self = _replace_variables(self)

  def __repr__(self):
    """Convert values that are paths into strings (otherwise yaml complains)."""
    dictionary = self.to_dict()
    for path in _walk(dictionary):
      value = path.pop()    
      if isinstance(value, pathlib.Path):
        value = str(value)
      last_key = path.pop()
      sub_dict = dictionary
      for key in path:
        sub_dict = sub_dict[key]
      sub_dict[last_key] = value
    tmp = json.loads(json.dumps(dictionary))
    return yaml.dump(tmp, default_flow_style=False)


def _walk(dictionary, key_path=[]):
  """Iterate through a nested dictionary."""
  for key, value in dictionary.items():
    if isinstance(value, dict):
      for path in _walk(value, key_path=[key]):
        yield path
    else:
      yield key_path + [key, value]

      
def _ispath(string):
  """Check if a string is a directory."""
  if string.startswith('$') or string.startswith('/'):
    return True
  else:
    return False

  
def _replace_variables(dictionary):
  """Replace environment variables in a nested dict."""
  for path in _walk(dictionary):
    value = path.pop()
    if isinstance(value, str) and _ispath(value):
      value = os.path.expandvars(value)
      value = pathlib.Path(value)
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
