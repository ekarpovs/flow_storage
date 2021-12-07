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
      self._config = config
      self._ws = ws
      self._storage: List[FlowStateStorage] = []
      self.utils = FlowIOUtils()
      self._init_strorage()
      return
      
  @property
  def storage(self) -> List[FlowStateStorage]:
    return self._storage

  def reset(self) -> None:
    # Clean all external storage data
    FlowIOUtils.clean_ext_storage(self._config.storage_path)         
    return

  def get_state_input_refs(self, state_id: str) -> List[FlowDataRef]:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        return state_storage.input_data.data_refs
    return None

  def get_state_input_data(self, state_id: str, aliases: Dict[str, str]) -> Dict:
    data = {}
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        refs = state_storage.input_data.data_refs
        for ref in refs:
          if len(aliases) > 0:
            if ref.int_ref in aliases.keys():
              ref.ext_ref = aliases.get(ref.int_ref)  
          # read the state data from the external storage
          ffn = f'{self._config.storage_path}/{ref.ext_ref}'
          reader = self.utils.reader(ref.data_type)
          data[ref.int_ref] = reader(ffn)
        break
    return data

  def get_state_output_data(self, state_id: str) -> Dict:
    data = {}
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        refs = state_storage.output_data.data_refs
        for ref in refs:
          # read the state data from the external storage
          reader = self.utils.reader(ref.data_type)
          ffn = f'{self._config.storage_path}/{ref.ext_ref}'
          data[ref.int_ref] = reader(ffn)
        break
    return data


  def set_state_output_data(self, state_id: str, data: Dict) -> None:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        refs = state_storage.output_data.data_refs
        for ref in refs:
          # write the state data to the external storage
          writer = self.utils.writer(ref.data_type)
          ffn = f'{self._config.storage_path}/{ref.ext_ref}'
          stored_item = data.get(ref.int_ref)
          if stored_item is not None:
            writer(ffn, stored_item)
        break
    return

  def clean_state_input_data(self, state_id: str) -> None:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        refs = state_storage.input_data.data_refs
        for ref in refs:
          # clean the state data from the external storage
          cleaner = self.utils.cleaner(ref.data_type)
          ffn = f'{self._config.storage_path}/{ref.ext_ref}'
          cleaner(ffn)
        break
    return

  def clean_state_output_data(self, state_id: str) -> None:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        refs = state_storage.output_data.data_refs
        for ref in refs:
          # clean the state data from the external storage
          cleaner = self.utils.cleaner(ref.data_type)
          ffn = f'{self._config.storage_path}/{ref.ext_ref}'
          cleaner(ffn)
        break
    return


  def get_state_input_ref(self, state_id: str, ext_ref: str) -> FlowDataRef:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        return state_storage.get_input_ref(ext_ref)
    return None


  def set_state_input_refs(self, state_id: str, in_data_refs: List[FlowDataRef]) -> None:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        if len(state_storage.input_data.data_refs) == 0:
          state_storage.input_data.data_refs = in_data_refs
          break;
        else:
          exits_refs: List[FlowDataRef] = copy.deepcopy(state_storage.input_data.data_refs)
          for ref in exits_refs:
            if ref.is_alias:
              continue
            for in_ref in in_data_refs:
              if ref.int_ref == in_ref.int_ref and ref.ext_ref == in_ref.ext_ref:
                break
              state_storage.input_data.data_refs.append(in_ref)
    return

  def get_state_output_refs(self, state_id: str) -> List[FlowDataRef]:
    for state_storage in self.storage:
      if state_storage.state_id == state_id:
        return state_storage.output_data.data_refs
    return None

  def set_state_output_refs(self, state_id: str, out_data: List[FlowDataRef]) -> None:
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
  def _data_type_str_to_flow_type(dt_str: str) -> FlowDataType:
    data_types = {
      "np.dtype" : FlowDataType.IMAGE,
      "List[np.ndarray]" : FlowDataType.CNTRS,
      "np.ndarray" : FlowDataType.KPNTS,
    }
    return data_types.get(dt_str, FlowDataType.JSON)


  def _init_strorage(self) -> None:
    for i, step in enumerate(self._ws):
      if 'info' in step.keys():
        continue
      exec = step.get('exec')
      st_id  = f'{i-1}-{exec.split(".")[1]}'
      st_storage = FlowStateStorage(st_id)

      # Create referenses
      aliases = step.get('aliases', None)
      fn = operation_loader.get(exec)
      (_, _, input_refs, output_refs) = operation_loader.parse_oper_doc(fn.__doc__)
      #  input data references:
      # internal refs - from operatiom definitions
      # external refs - from step aliases or the same as internal
      for inref in input_refs:
        if exec != 'glbstm.begin':
          iref = f'{inref[0: inref.index(":")].strip()}'
          dtype_str = inref[inref.index(':')+1: inref.index(';')].strip()
          dtype = self._data_type_str_to_flow_type(dtype_str)
          eref = f'{i-1}-{exec}-{inref[0: inref.index(":")].strip()}'
          if aliases is not None:
            eref = aliases.get(iref, None)
            if eref is not None:
              data_ref = FlowDataRef(iref, eref, dtype, True)
              st_storage.input_data.set_data_ref(data_ref)
      
      #  output data references:
      for outref in output_refs:
        if exec != 'glbstm.end':
          iref = f'{outref[0: outref.index(":")].strip()}'
          dtype_str = outref[outref.index(':')+1: outref.index(';')].strip()
          dtype = self._data_type_str_to_flow_type(dtype_str)
          eref = f'{i-1}-{exec}-{outref[0: outref.index(":")].strip()}'
          data_ref = FlowDataRef(iref, eref, dtype)
          st_storage.output_data.set_data_ref(data_ref)
      
      # Add in/out data into the storage
      self.set_state_storage_by_idx(i-1, st_storage)    
    return