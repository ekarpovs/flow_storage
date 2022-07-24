from typing import List

from .flowtypes import FlowIOType
from .flowdataref import FlowDataRef


class FlowStateIOData():
  def __init__(self, io_type: FlowIOType) -> None:
    self._io_type = io_type
    self._data_refs: List[FlowDataRef] = []
    return

  @property
  def io_type(self) -> FlowIOType:
    return self._io_type

  @property
  def data_refs(self) -> List[FlowDataRef]:
    return self._data_refs

  @data_refs.setter
  def data_refs(self, refs: List[FlowDataRef]) -> None:
    self._data_refs = refs
    return

  def get_ext_data_ref(self, int_ref: str) -> FlowDataRef:
    for data_ref in self._data_refs:
      if data_ref.int_ref == int_ref:
        return data_ref
    return None

  def get_data_ref(self, ext_ref: str) -> FlowDataRef:
    for data_ref in self._data_refs:
      if data_ref.ext_ref == ext_ref:
        return data_ref
    return None

  def set_data_ref(self, data_ref: FlowDataRef) -> None:
    try:
      # replace the existing item
      idx = self._data_refs.index(data_ref)
      self._data_refs.insert(idx, data_ref)
    except Exception:
      # create new one
      self._data_refs.append(data_ref)
    return
