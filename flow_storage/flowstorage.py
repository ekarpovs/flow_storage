from typing import Dict, List
import operation_loader

from .flowioutils import FlowIOUtils
from .flowstorageconfig import FlowStorageConfig
from .flowstatestorage import FlowStateStorage
from .flowstateiodata import FlowStateIOData
from .flowdataref import FlowDataRef
from .flowtypes import FlowDataType, FlowIOType

class FlowStorage():
  '''
  Flow storage
  '''

  def __init__(self, config: FlowStorageConfig, ws: List[Dict]) -> None:
      self._config = config
      self._ws = ws
      self._storage: List[FlowStateStorage] = []
      self._init_strorage()
      return
      
  @property
  def storage(self) -> List[FlowStateStorage]:
    return self._storage

  def reset(self) -> None:
    # Clean all external storage data
    FlowIOUtils.clean_ext_storage(self._config.path)         
    return

  def get_state_input(self, state_id: str) -> List[FlowDataRef]:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        return state_storage.input_data
    return None

  def get_state_input_ref(self, state_id: str, ext_ref: str) -> FlowDataRef:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        return state_storage.get_input_ref(ext_ref)
    return None


  def set_state_input(self, state_id: str, in_data: List[FlowDataRef]) -> None:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        state_storage.input_data = in_data
    return

  def get_state_output(self, state_id: str) -> List[FlowDataRef]:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        return state_storage.output_data
    return None

  def set_state_output(self, state_id: str, out_data: List[FlowDataRef]) -> None:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        state_storage.output_data = out_data
    return

  def get_state_storage_by_idx(self, idx: int) -> FlowStateStorage:
    return self.storage[idx]

  def set_state_storage_by_idx(self, idx: int, item: FlowStateStorage) -> None:
    self.storage.insert(idx, item)
    return  
  
  @staticmethod
  def _data_type_str_to_flow_type(dt_str: str):
    dtype = FlowDataType.IMAGE
    # if dt_str == 'np.dtype':
    #   dtype = FlowDataType.IMAGE
    return dtype


  def _init_strorage(self) -> None:
    for i, step in enumerate(self._ws):
      if 'info' in step.keys():
        continue
      exec = step.get('exec')
      st_id  = f'{i-1}-{exec.split(".")[1]}'
      st_storage = FlowStateStorage(st_id)
      # Create input data container for the state
      st_storage.input_data = FlowStateIOData(FlowIOType.IN)
      # Create output data container for the state
      st_storage.output_data = FlowStateIOData(FlowIOType.OUT)
      # Create referenses
      aliases = step.get('aliases', None)
      fn = operation_loader.get(exec)
      (_, _, input_refs, output_refs) = operation_loader.parse_oper_doc(fn.__doc__)
      #  input data references:
      # internal refs - from operatiom definitions
      # external refs - from step aliases or the same as internal    
      for inref in input_refs:
        iref = f'{i-1}-{exec}-{inref[0: inref.index(":")].strip()}'
        dt_str = inref[inref.index(':')+1: inref.index(';')].strip()
        dtype = self._data_type_str_to_flow_type(dt_str)
        eref = iref
        if aliases is not None:
          eref = aliases.get(iref, None)
        data_ref = FlowDataRef(iref, eref, dtype)
        st_storage.input_data.set_data_ref(data_ref)
      
      #  output data references:
      for outref in output_refs:
        iref = f'{i-1}-{exec}-{outref[0: outref.index(":")].strip()}'
        dt_str = outref[outref.index(':')+1: outref.index(';')].strip()
        dtype = self._data_type_str_to_flow_type(dt_str)
        eref = iref
        data_ref = FlowDataRef(iref, eref, dtype)
        st_storage.output_data.set_data_ref(data_ref)
      
      # Add in/out data into the storage
      self.set_state_storage_by_idx(i-1, st_storage)    
    return