from typing import Callable

from .flowtypes import FlowDataType


class FlowDataRef():
  def __init__(self, int_ref: str='', ext_ref: str='', data_type: FlowDataType=FlowDataType.JSON, is_link: bool=False) -> None:
      self._int_ref = int_ref
      self._ext_ref = ext_ref
      self._data_type = data_type
      self._is_link = is_link
      return

  @property
  def int_ref(self) -> str:
    return self._int_ref

  @int_ref.setter
  def int_ref(self, ref: str) -> None:
    self._int_ref = ref
    return

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

  @data_type.setter
  def data_type(self, dtype: FlowDataType) -> None:
    self._data_type = dtype
    return

  @property
  def is_link(self) -> bool:
    return self._is_link

  @is_link.setter
  def is_link(self, is_link) -> None:
    self._is_link = is_link
    return 
