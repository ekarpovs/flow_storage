from typing import Callable

from .flowtypes import FlowDataType


class FlowDataRef():
  def __init__(self, int_ref: str, ext_ref: str, data_type: FlowDataType) -> None:
      self._int_ref = int_ref
      self._ext_ref = ext_ref
      self._data_type = data_type
      return

  @property
  def int_ref(self) -> str:
    return self._int_ref

  @property
  def ext_ref(self) -> str:
    return self._ext_ref

  @ext_ref.setter
  def ext_ref(self, ref) -> str:
    self._ext_ref = ref
    return 
    
  @property
  def data_type(self) -> FlowDataType:
    return self._data_type