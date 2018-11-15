import nomen
import os
import pathlib


from util import get_path


def test_set_get():
  os.environ["TMP"] = "/tmp"
  cfg = nomen.Config(yaml_path=get_path("config.yml"), make_flags=False)
  assert cfg['model']['learning_rate'] == 0.2
  assert cfg.model.learning_rate == 0.2
  cfg.model.learning_rate = 42.
  assert cfg.model.learning_rate == 42.

  
if __name__ == '__main__':
  test_set_get()
