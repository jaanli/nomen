from unittest import TestCase

import nomen


class TestCfg(TestCase):
  def test_hierarchy(self):
    cfg = nomen.Config()
    cfg.define_float('learning_rate', 0.5, 'docstring')
    cfg.define_integer('hidden_size', 200, 'hidden')
    cfg.define_float('model/learning_rate', 0.8, 'docstr')
    with cfg.scope('variational'):
      cfg.define_float('learning_rate', 2., 'learning rate for variational')
    cfg.parse_args()
    # test getting
    print cfg
    self.assertEquals(cfg['hidden_size'], 200)
    # pop back up to globals if not found in lowest level of tree
    self.assertEquals(cfg['variational/hidden_size'], 200)
    self.assertEquals(cfg['variational/learning_rate'], 2.)
    with cfg.scope('variational'):
      self.assertEquals(cfg['learning_rate'], 2.)
    # test loading
    cfg['variational'].update({'learning_rate': 0.08})
    self.assertEquals(cfg['variational/learning_rate'], 0.08)
    dct = {'learning_rate': 0.00001, 'variational': {'learning_rate': 0.01}}
    cfg.update(dct)
    self.assertEquals(cfg['variational/learning_rate'], 0.01)
