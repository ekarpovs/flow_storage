import os, os.path
import cv2
import numpy as np
import json
from typing import Callable, Dict, List, Tuple

from .flow_io_utils_impl import FlowIOUtilsImpl
from .flowtypes import FlowDataType, FlowStorageType
from .flowstorageconfig import FlowStorageConfig

class FlowIOUtils():
  def __init__(self, config: FlowStorageConfig) -> None:
    self.impl = FlowIOUtilsImpl(config)
    return

  def clean_ext_storage(self) -> Callable:
    return self.impl.clean_ext_storage()

  def reader(self, rtype: FlowDataType) -> Callable:
    readers = {
      FlowDataType.NP_ARRAY: self.impl.np_array_reader,
      FlowDataType.LIST_NP_ARRAYS: self.impl.list_np_arrays_reader,
      FlowDataType.LIST_OF_LISTS_NP_ARRAYS: self.impl.list_of_lists_np_arrays_reader,
      FlowDataType.JSON: self.impl.json_reader,
      FlowDataType.LIST_TUPLES: self.impl.list_tuples_reader,
      FlowDataType.LIST_KPNTS: self.impl.list_keypoints_reader
    }
    return readers.get(rtype)

  def writer(self, rtype: FlowDataType) -> Callable:
    writers = {
      FlowDataType.NP_ARRAY: self.impl.np_array_writer,
      FlowDataType.LIST_NP_ARRAYS: self.impl.list_np_arrays_writer,
      FlowDataType.LIST_OF_LISTS_NP_ARRAYS: self.impl.list_of_lists_np_arrays_writer,
      FlowDataType.JSON: self.impl.json_writer,
      FlowDataType.LIST_TUPLES: self.impl.list_tuples_writer,
      FlowDataType.LIST_KPNTS: self.impl.list_keypoints_writer
    }
    return writers.get(rtype)

  def cleaner(self, rtype: FlowDataType) -> Callable:
    cleaners = {
      FlowDataType.NP_ARRAY: self.impl.data_cleaner('npy'),
      FlowDataType.LIST_NP_ARRAYS: self.impl.data_cleaner('json'),
      FlowDataType.LIST_KPNTS: self.impl.data_cleaner('json')
    }
    return cleaners.get(rtype, self.impl.data_cleaner('json'))
