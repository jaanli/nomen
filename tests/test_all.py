import nomen
import os
import yaml
import pytest

from util import get_path

os.environ["TMP"] = "/tmp"


def test_args():
  with open(get_path("config.yml"), 'r') as f:
    cfg = nomen.Config(yaml.safe_load(f))
  cfg.parse_args(['--list', '3', '27', '99'])
  assert cfg.list == [3, 27, 99]


def test_serialization():
  with open(get_path("config.yml"), 'r') as f:
    cfg = nomen.Config(yaml.safe_load(f), make_args=False)
  tmp_path = get_path("tmp_config.yml")
  with open(tmp_path, "w") as f:
    f.write(str(cfg))
  with open(tmp_path, 'r') as f:
    tmp_cfg = nomen.Config(yaml.safe_load(f), make_args=False)
  assert str(tmp_cfg) == str(cfg)
  # test yaml variables
  assert tmp_cfg.second_house.windows == cfg.second_house.windows
  os.remove(tmp_path)
  

def test_set_get():
  with open(get_path("config.yml"), 'r') as f:
    cfg = nomen.Config(yaml.safe_load(f), make_args=False)
  assert cfg['model']['learning_rate'] == 0.2
  assert cfg.model.learning_rate == 0.2
  cfg.model.learning_rate = 42.
  assert cfg.model.learning_rate == 42.


def test_update():
  fake_path = '/fake_path'
  os.environ['FAKE'] = fake_path 
  with open(get_path("config.yml"), 'r') as f:
    cfg = nomen.Config(yaml.safe_load(f), make_args=False)
  cfg.update({'test_path': '$FAKE'})
  assert str(cfg.test_path) == fake_path


def test_missing_value():
  with open(get_path('config.yml'), 'r') as f:
    cfg = nomen.Config(yaml.safe_load(f), make_args=False)
  with pytest.raises(AttributeError):
    cfg.first_house.nonexistent

  
if __name__ == '__main__':
  test_missing_value()
  test_set_get()
  test_update()
  test_args()
  test_serialization()
