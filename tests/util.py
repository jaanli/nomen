import os
import nomen


def get_path(file_name):
  current_dir = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(current_dir, file_name)


cfg = nomen.Config(get_path('config.yml'))
