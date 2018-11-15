from util import get_path
import os
import nomen
import yaml
import copy


def test_serialization():
  os.environ["TMP"] = "/tmp"
  cfg = nomen.Config(yaml_path=get_path("config.yml"), make_flags=False)
  tmp_path = get_path("tmp_config.yml")
  with open(tmp_path, "w") as f:
    f.write(str(cfg))
  tmp_cfg = nomen.Config(yaml_path=tmp_path, make_flags=False)
  assert str(tmp_cfg) == str(cfg)
  # test yaml variables
  assert tmp_cfg.second_house.windows == cfg.second_house.windows
  os.remove(tmp_path)


def test_loading():
  cfg = nomen.Config(yaml_path=get_path('local_config.yml'), make_flags=False)
  assert cfg.model.learning_rate == 0.232

if __name__ == "__main__":
  test_serialization()
  test_loading()
