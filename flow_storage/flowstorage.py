import copy
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
      self._ws = ws
      self._storage: List[FlowStateStorage] = []
      self._utils = FlowIOUtils(config)
      self._init_strorage()
      return
  
  @property
  def storage(self) -> List[FlowStateStorage]:
    return self._storage

  def close(self) -> None:
    self._utils.impl.close()
    return

    return
  def reset(self) -> None:
    # Clean all external storage data
    self._utils.clean_ext_storage()         
    return

  def _get_state_sorage(self, state_id: str) -> FlowStateStorage:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        return state_storage
    return None

# Input
  def get_state_input_refs(self, state_id: str) -> List[FlowDataRef]:
    state_storage: FlowStateStorage = self._get_state_sorage(state_id)
    if state_storage is not None:
      return state_storage.input_data.data_refs
    return None

  def get_state_input_ref(self, state_id: str, ext_ref: str) -> FlowDataRef:
    state_storage: FlowStateStorage = self._get_state_sorage(state_id)
    if state_storage is not None:
      return state_storage.get_input_ref(ext_ref)
    return None

  def get_state_input_data(self, state_id: str) -> Dict:
    data = {}
    refs = self.get_state_input_refs(state_id)
    for ref in refs:
      if ref.ext_ref == '':
        continue
      # read the state data from the external storage
      reader = self._utils.reader(ref.data_type)
      data[ref.int_ref] = reader(ref.ext_ref)
    return data

# Output
  def get_state_output_refs(self, state_id: str) -> List[FlowDataRef]:
    state_storage: FlowStateStorage = self._get_state_sorage(state_id)
    if state_storage is not None:
      return state_storage.output_data.data_refs
    return None

  def get_state_output_data(self, state_id: str) -> Dict:
    data = {}
    refs = self.get_state_output_refs(state_id)
    for ref in refs:
      # read the state data from the external storage
      reader = self._utils.reader(ref.data_type)
      data[ref.int_ref] = reader(ref.ext_ref)
    return data

  def set_state_output_data(self, state_id: str, data: Dict) -> None:
    refs = self.get_state_output_refs(state_id)
    for ref in refs:
      # write the state data to the external storage
      writer = self._utils.writer(ref.data_type)
      stored_item = data.get(ref.int_ref)
      if stored_item is not None:
        writer(ref.ext_ref, stored_item)
    return

  def clean_state_output_data(self, state_id: str) -> None:
    refs = self.get_state_output_refs(state_id)
    for ref in refs:
      # clean the state data from the external storage
      cleaner = self._utils.cleaner(ref.data_type)
      cleaner(ref.ext_ref)
    return

# Storage
  def get_state_storage_by_idx(self, idx: int) -> FlowStateStorage:
    return self.storage[idx]

  def set_state_storage_by_idx(self, idx: int, item: FlowStateStorage) -> None:
    self.storage.insert(idx, item)
    return  
  
  @staticmethod
  def _data_type_str_to_flow_type(dt_str: str) -> FlowDataType:
    data_types = {
      "ndarray" : FlowDataType.NP_ARRAY,
      "List[ndarray]" : FlowDataType.LIST_NP_ARRAYS,
      "List[List[ndarray]]" : FlowDataType.LIST_OF_LISTS_NP_ARRAYS,
      "List[Tuple[uint]]" : FlowDataType.LIST_TUPLES,
      "List[KeyPoint]" : FlowDataType.LIST_KPNTS,
    }
    return data_types.get(dt_str, FlowDataType.JSON)

  def _init_strorage(self) -> None:
    prev_step = {'state_id': '', 'output_refs': []}
    for i, step in enumerate(self._ws):
      if 'info' in step.keys():
        continue
      exec = step.get('exec')
      st_id  = f'{i-1}-{exec.split(".")[1]}'
      st_storage = FlowStateStorage(st_id)

      # Create referenses
      func = operation_loader.get(exec)
      (_, _, input_refs, output_refs) = operation_loader.parse_oper_doc(func.__doc__)
      #  input data references:
      # internal refs - from operatiom definitions
      # external refs - from step links or the same as internal
      for input_ref in input_refs:
        if exec != 'glbstm.begin':
          internal_ref = f'{input_ref[0: input_ref.index(":")].strip()}'
          dtype_str = input_ref[input_ref.index(':')+1: input_ref.index(';')].strip()
          dtype = self._data_type_str_to_flow_type(dtype_str)
          data_ref = FlowDataRef(internal_ref)
          data_ref.data_type = dtype
          # define default stream
          prev_exec = prev_step.get('exec')
          prev_output_refs = prev_step.get('output_refs', None)
          if prev_output_refs is not None:
            for prev_output_ref in prev_output_refs:
              prev_ref = prev_output_ref[0: prev_output_ref.index(":")].strip()              
              if prev_ref is not None and prev_ref == internal_ref:
                prev_external_ref = f'{i-2}-{prev_exec}-{prev_ref.strip()}'
                data_ref.ext_ref = prev_external_ref
          # update by link if exists
          links = step.get('links', None)
          if links is not None:
            link = links.get(internal_ref, None)
            if link is not None:
              data_ref.ext_ref = link
              data_ref.is_link = True
          st_storage.input_data.set_data_ref(data_ref)
        
      #  output data references:
      for output_ref in output_refs:
        if exec != 'glbstm.end':
          internal_ref = f'{output_ref[0: output_ref.index(":")].strip()}'
          dtype_str = output_ref[output_ref.index(':')+1: output_ref.index(';')].strip()
          dtype = self._data_type_str_to_flow_type(dtype_str)
          external_ref = f'{i-1}-{exec}-{output_ref[0: output_ref.index(":")].strip()}'
          data_ref = FlowDataRef(internal_ref, external_ref, dtype)
          st_storage.output_data.set_data_ref(data_ref)
      
      self.set_state_storage_by_idx(i-1, st_storage)
      # save current refs for usage on the next step like default values of input refs
      prev_step['exec'] = exec 
      prev_step['output_refs'] = output_refs
    return