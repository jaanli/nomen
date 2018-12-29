from util import get_path
import os
import nomen
import yaml
import copy


def test_serialization():
  os.environ["TMP"] = "/tmp"
  with open(get_path("config.yml"), 'r') as f:
    cfg = nomen.Config(yaml.load(f), make_args=False)
  tmp_path = get_path("tmp_config.yml")
  with open(tmp_path, "w") as f:
    f.write(str(cfg))
  with open(tmp_path, 'r') as f:
    tmp_cfg = nomen.Config(yaml.load(f), make_args=False)
  assert str(tmp_cfg) == str(cfg)
  # test yaml variables
  assert tmp_cfg.second_house.windows == cfg.second_house.windows
  os.remove(tmp_path)


if __name__ == "__main__":
  test_serialization()
