'''
'''

from .flowdataref import FlowDataRef
from .flowstateiodata import FlowStateIOData
from .flowtypes import FlowIOType


class FlowStateStorage():
  def __init__(self, state_id: str) -> None:
      self._state_id = state_id
      self._input_data = FlowStateIOData(FlowIOType.IN)
      self._output_data = FlowStateIOData(FlowIOType.OUT)
      self._cache_data = FlowStateIOData(FlowIOType.CACHE)

  @property
  def state_id(self) -> str:
    return self._state_id

  @property
  def input_data(self) -> FlowStateIOData:
    return self._input_data

  @input_data.setter
  def input_data(self, data: FlowStateIOData) -> None:
    self._input_data = data
    return

  @property
  def output_data(self) -> FlowStateIOData:
    return self._output_data

  @output_data.setter
  def output_data(self, data: FlowStateIOData) -> None:
    self._output_data = data
    return

  @property
  def cache_data(self) -> FlowStateIOData:
    return self._cache_data

  @cache_data.setter
  def cache_data(self, data: FlowStateIOData) -> None:
    self._cache_data = data
    return

  def get_input_ref(self, ext_ref: str) -> FlowDataRef:
    return self.input_data.get_data_ref(ext_ref)

  def get_input_ext_data_ref(self, int_ref: str) -> FlowDataRef:
    return self.input_data.get_ext_data_ref(int_ref)
