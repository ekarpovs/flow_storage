class FlowStorageConfig():
  '''
  Flow storage configuration
  '''

  def __init__(self, path: str) -> None:
      self._path = path 
      return
      
  def path(self) -> str:
    return self._path

