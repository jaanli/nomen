from util import cfg, get_path
import os
import nomen
import yaml
import copy


def test_serialization():
  tmp_path = get_path('tmp_config.yml')
  with open(tmp_path, 'w') as f:
    f.write(str(cfg))
  tmp_cfg = cfg.copy()
  tmp_cfg.update_from_yaml(tmp_path)
  assert str(tmp_cfg) == str(cfg)
  # test yaml variables
  assert tmp_cfg['second_house/windows'] == cfg['second_house/windows']
  os.remove(tmp_path)


def test_loading():
  tmp_cfg = cfg.copy()
  tmp_cfg.update_from_yaml(get_path('local_config.yml'))
  assert tmp_cfg['model/learning_rate'] == 0.232


if __name__ == '__main__':
  test_serialization()
  test_loading()
