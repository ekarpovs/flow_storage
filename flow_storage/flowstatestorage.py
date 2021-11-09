'''
'''

from typing import Dict, List

from flow_storage.flowdataref import FlowDataRef

from .flowstateiodata import FlowStateIOData

class FlowStateStorage():
  def __init__(self, state_id: str) -> None:
      self._state_id = state_id
      self._input_data: FlowStateIOData = None
      self._output_data: FlowStateIOData = None

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


  def get_input_ref(self, ext_ref: str) -> FlowDataRef:
    self.input_data.get_data_ref(ext_ref)