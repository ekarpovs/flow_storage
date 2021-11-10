class FlowStorageConfig():
  '''
  Flow storage configuration
  '''

  def __init__(self, path: str) -> None:
      self._storage_path = path 
      return

  @property    
  def storage_path(self) -> str:
    return self._storage_path

