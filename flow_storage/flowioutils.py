from typing import Callable

from .flow_io_utils_impl import FlowIOUtilsImpl
from .flowtypes import FlowDataType as fdt
from .flowstorageconfig import FlowStorageConfig


class FlowIOUtils():
  def __init__(self, config: FlowStorageConfig) -> None:
    self.impl = FlowIOUtilsImpl(config)
    return

  def clean_ext_storage(self) -> Callable:
    return self.impl.clean_ext_storage()

  def reader(self, rtype: fdt) -> Callable:
    readers = {
        fdt.NP_ARRAY: self.impl.np_array_reader,
        fdt.LIST_NP_ARRAYS: self.impl.list_np_arrays_reader,
        fdt.LIST_OF_LISTS_NP_ARRAYS: self.impl.list_of_lists_np_arrays_reader,
        fdt.JSON: self.impl.json_reader,
        fdt.LIST_TUPLES: self.impl.list_tuples_reader,
        fdt.LIST_KPNTS: self.impl.list_keypoints_reader
    }
    return readers.get(rtype)

  def writer(self, rtype: fdt) -> Callable:
    writers = {
        fdt.NP_ARRAY: self.impl.np_array_writer,
        fdt.LIST_NP_ARRAYS: self.impl.list_np_arrays_writer,
        fdt.LIST_OF_LISTS_NP_ARRAYS: self.impl.list_of_lists_np_arrays_writer,
        fdt.JSON: self.impl.json_writer,
        fdt.LIST_TUPLES: self.impl.list_tuples_writer,
        fdt.LIST_KPNTS: self.impl.list_keypoints_writer
    }
    return writers.get(rtype)

  def cleaner(self, rtype: fdt) -> Callable:
    cleaners = {
        fdt.NP_ARRAY: self.impl.data_cleaner('npy'),
        fdt.LIST_NP_ARRAYS: self.impl.data_cleaner('json'),
        fdt.LIST_KPNTS: self.impl.data_cleaner('json')
    }
    return cleaners.get(rtype, self.impl.data_cleaner('json'))
