import pytest
from importlib import reload
import os
import json


from util import cfg


def test_set_get():
  assert cfg['model/learning_rate'] == 0.2
  cfg['model']['learning_rate'] = 2.
  assert cfg['model/learning_rate'] == 2.
  cfg['model/learning_rate'] = 0.1
  assert cfg['model/learning_rate'] == 0.1
  cfg.update({'model': {'learning_rate': 100.}})
  assert cfg['model/learning_rate'] == 100.


def test_environment_variables():
  os.environ['TMP'] = '/tmp/'
  tmp_cfg = cfg.copy()
  tmp_cfg.update({'TMP': '$TMP'})
  print(str(tmp_cfg))
  assert tmp_cfg['TMP'] == '/tmp/'


if __name__ == '__main__':
  test_environment_variables()
