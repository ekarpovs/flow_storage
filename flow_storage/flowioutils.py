import os, re, os.path
import cv2
import numpy as np
import json
from typing import Callable, Dict, List, Tuple

from .flowtypes import FlowDataType

class FlowIOUtils():
  def __init__(self) -> None:
      pass

  @staticmethod
  def clean_ext_storage(path: str) -> None:
    for root, dirs, files in os.walk(path):
      for file in files:
        os.remove(os.path.join(root, file))
    return

  def reader(self, rtype: FlowDataType) -> Callable:
    readers = {
      FlowDataType.CV2_IMAGE: self._cv2_image_reader,
      FlowDataType.NP_ARRAY: self._np_array_reader,
      FlowDataType.LIST_NP_ARRAYS: self._list_np_arrays_reader,
      FlowDataType.JSON: self._json_reader,
      FlowDataType.LIST_TUPLES: self._list_tuples_reader,
      FlowDataType.KPNTS: self._keypoints_reader
    }
    return readers.get(rtype)

  def writer(self, rtype: FlowDataType) -> Callable:
    writers = {
      FlowDataType.CV2_IMAGE: self._cv2_image_writer,
      FlowDataType.NP_ARRAY: self._np_array_writer,
      FlowDataType.LIST_NP_ARRAYS: self._list_np_arrays_writer,
      FlowDataType.JSON: self._json_writer,
      FlowDataType.LIST_TUPLES: self._list_tuples_writer,
      FlowDataType.KPNTS: self._keypoints_writer
    }
    return writers.get(rtype)

  def cleaner(self, rtype: FlowDataType) -> Callable:
    cleaners = {
      FlowDataType.CV2_IMAGE: self._data_cleaner('jpg'),
      FlowDataType.NP_ARRAY: self._data_cleaner('npy'),
      FlowDataType.LIST_NP_ARRAYS: self._data_cleaner('json')
    }
    return cleaners.get(rtype, self._data_cleaner('json'))


  @staticmethod
  def _cv2_image_reader(ffn: str) -> np.dtype:
    ffn = f'{ffn}.jpg'
    return cv2.imread(ffn, cv2.IMREAD_UNCHANGED)

  @staticmethod
  def _np_array_reader(ffn: str) -> np.dtype:
    ffn = f'{ffn}.npy'
    return np.load(ffn)

  @staticmethod
  def _json_reader(ffn: str) -> Dict:
    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      data = json.load(f)
      return data

  @staticmethod
  def _list_np_arrays_reader(ffn: str) -> List[np.ndarray]:
    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      ld = json.load(f)
      data = [np.array(d) for d in ld]
      return data


  @staticmethod
  def _list_tuples_reader(ffn: str) -> List[np.ndarray]:
    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      ld = json.load(f)
      data = [np.array(d) for d in ld]
      return data


  @staticmethod
  def _keypoints_reader(ffn: str) -> np.ndarray:
    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      data = np.array(json.load(f))
      return data


  @staticmethod
  def _cv2_image_writer(ffn: str, arr: np.dtype) -> None:
    ffn = f'{ffn}.jpg'
    cv2.imwrite(ffn, arr)
    return

  @staticmethod
  def _np_array_writer(ffn: str, arr: np.dtype) -> None:
    ffn = f'{ffn}.npy'
    np.save(ffn, arr)
    return

  @staticmethod
  def _list_np_arrays_writer(ffn: str, data: List[np.ndarray]) -> None:
    ffn = f'{ffn}.json'
    sd = [d.tolist() for d in data]
    with open(ffn, 'w') as fp:
      json.dump(sd, fp, indent=2)
    return

  @staticmethod
  def _json_writer(ffn: str, data: Dict) -> None:
    ffn = f'{ffn}.json'
    with open(ffn, 'w') as fp:
      json.dump(data, fp, indent=2)
    return

  @staticmethod
  def _list_tuples_writer(ffn: str, data: List[Tuple]) -> None:
    ffn = f'{ffn}.json'
    with open(ffn, 'w') as fp:
      json.dump(data, fp, indent=2)
    return

  @staticmethod
  def _keypoints_writer(ffn: str, data: np.ndarray) -> None:
    ffn = f'{ffn}.json'
    with open(ffn, 'w') as fp:
      json.dump(data.tolist(), fp, indent=2)
    return


  @staticmethod
  def _data_cleaner(ext: str) -> None:
    extension = ext
    
    def _cleaner( fn: str):
      ffn = f'{fn}.{extension}'
      if os.path.exists (ffn) :
        os.remove (ffn)
      else :
        print(f'The {ffn} does not exist')
      return
    return _cleaner
