import json


class PathDict(dict):
  """Class to allow getting and setting of dictionary values with paths."""

  def __init__(self, *args, **kwargs):
    super(PathDict, self).__init__(*args, **kwargs)

  def __getitem__(self, key):
    keys = key.split('/')
    res = dict.__getitem__(self, keys[0])
    if len(keys) == 1:
      return res
    else:
      for key in keys[1:]:
        res = dict.__getitem__(res, key)
    return res

  def __setitem__(self, key, value):
    path = key.split('/')
    leaf_key = path.pop()
    tree = self
    for node in path:
      tree = tree[node]
    # if leaf_key not in tree:
    #   raise KeyError('Parameter %s not found' % leaf_key)
    dict.__setitem__(tree, leaf_key, value)
