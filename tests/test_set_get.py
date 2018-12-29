import nomen
import os
import pathlib
import yaml

from util import get_path


def test_set_get():
  os.environ["TMP"] = "/tmp"
  with open(get_path("config.yml"), 'r') as f:
    cfg = nomen.Config(yaml.load(f), make_args=False)
  assert cfg['model']['learning_rate'] == 0.2
  assert cfg.model.learning_rate == 0.2
  cfg.model.learning_rate = 42.
  assert cfg.model.learning_rate == 42.

  
if __name__ == '__main__':
  test_set_get()
