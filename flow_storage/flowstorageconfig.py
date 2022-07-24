from typing import Dict


class FlowStorageConfig():
  '''
  Flow storage configuration
  '''

  def __init__(self, config: Dict) -> None:
      self._config = config
      return

  @property
  def storage_type(self) -> str:
    return self._config.get('type', 'fs')

  @property
  def storage_location(self) -> str:
    return self._config.get('location', '../data/storage')
