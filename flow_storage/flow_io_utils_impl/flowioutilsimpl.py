import cv2
import numpy as np

from abc import abstractmethod
from typing import Callable, Dict, List, Tuple
from ..flowtypes import *
from ..flowstorageconfig import FlowStorageConfig
from .flowioutils_fs import FlowIOUtilsFs
from .flowioutils_h5py import FlowIOUtilsH5Py

class FlowIOUtilsImpl():
  def __init__(self, config: FlowStorageConfig) -> None:
    self.impl = self.impl_factory(config)
    return


  def impl_factory(self, config: FlowStorageConfig):
    impl = {
      FlowStorageType.H5PY: FlowIOUtilsH5Py(config)
    }
    return impl.get(config.storage_type, FlowIOUtilsFs(config))

  def clean_ext_storage(self) -> None:
    return self.impl.clean_ext_storage()

# Readers
  def np_array_reader(self, ffn: str) -> Callable:
    return self.impl.np_array_reader(ffn)

  def json_reader(self, ffn: str) -> Dict:
    return self.impl.json_reader(ffn)

  def list_np_arrays_reader(self, ffn: str) -> List[np.ndarray]:
    return self.impl.list_np_arrays_reader(ffn)

  def list_tuples_reader(self, ffn: str) -> List[Tuple]:
    return self.impl.list_tuples_reader(ffn)

  def list_keypoints_reader(self, ffn: str) -> List[cv2.KeyPoint]:
    return self.impl.list_keypoints_reader(ffn)

# Writers
  def np_array_writer(self, ffn: str, arr: np.ndarray) -> None:
    return self.impl.np_array_writer(ffn, arr)

  def list_np_arrays_writer(self, ffn: str, data: List[np.ndarray]) -> None:
    return self.impl.list_np_arrays_writer(ffn, data)

  def json_writer(self, ffn: str, data: Dict) -> None:
    return self.impl.json_writer(ffn, data)

  def list_tuples_writer(self, ffn: str, data: List[Tuple]) -> None:
    return self.impl.list_tuples_writer(ffn, data)

  def list_keypoints_writer(self, ffn: str, data: List[cv2.KeyPoint]) -> None:
    return self.impl.list_keypoints_writer(ffn, data)

# Cleaner
  def data_cleaner(self, ext: str) -> None:
    return self.impl.data_cleaner(ext)
