import nomen
import os
import yaml

from util import get_path


def test_args():
  os.environ["TMP"] = "/tmp"
  with open(get_path("config.yml"), 'r') as f:
    cfg = nomen.Config(yaml.load(f))
  cfg.parse_args(['--list', '3', '27', '99'])
  assert cfg.list == [3, 27, 99]

  
if __name__ == '__main__':
  test_args()
