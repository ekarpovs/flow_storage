import os, re, os.path
import cv2
import numpy as np
import json
from typing import Callable, Dict, List

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
      FlowDataType.IMAGE: self._image_reader,
      FlowDataType.JSON: self._json_reader,
      FlowDataType.CNTRS: self._contours_reader,
      FlowDataType.KPNTS: self._keypoints_reader
    }
    return readers.get(rtype)

  def writer(self, rtype: FlowDataType) -> Callable:
    writers = {
      FlowDataType.IMAGE: self._image_writer,
      FlowDataType.JSON: self._json_writer,
      FlowDataType.CNTRS: self._contours_writer,
      FlowDataType.KPNTS: self._keypoints_writer
    }
    return writers.get(rtype)

  def cleaner(self, rtype: FlowDataType) -> Callable:
    cleaners = {
      FlowDataType.IMAGE: self._image_cleaner
    }
    return cleaners.get(rtype, self._json_cleaner)


  @staticmethod
  def _image_reader(ffn: str) -> np.dtype:
    ffn = f'{ffn}.jpg'
    return cv2.imread(ffn, cv2.IMREAD_UNCHANGED)

  @staticmethod
  def _json_reader(ffn: str) -> Dict:
    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      data = json.load(f)
      return data

  @staticmethod
  def _contours_reader(ffn: str) -> List[np.ndarray]:
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
  def _image_writer(ffn: str, image: np.dtype) -> None:
    ffn = f'{ffn}.jpg'
    cv2.imwrite(ffn, image)
    return

  @staticmethod
  def _json_writer(ffn: str, data: Dict) -> None:
    ffn = f'{ffn}.json'
    with open(ffn, 'w') as fp:
      json.dump(data, fp, indent=2)
    return

  @staticmethod
  def _contours_writer(ffn: str, data: List[np.ndarray]) -> None:
    ffn = f'{ffn}.json'
    sd = [d.tolist() for d in data]
    with open(ffn, 'w') as fp:
      json.dump(sd, fp, indent=2)
    return

  @staticmethod
  def _keypoints_writer(ffn: str, data: np.ndarray) -> None:
    ffn = f'{ffn}.json'
    with open(ffn, 'w') as fp:
      json.dump(data.tolist(), fp, indent=2)
    return


  @staticmethod
  def _image_cleaner(ffn: str) -> None:
    ffn = f'{ffn}.jpg'
    if os.path.exists (ffn) :
      os.remove (ffn)
    else :
      print(f'The {ffn} does not exist')
    return

  @staticmethod
  def _json_cleaner(ffn: str) -> None:
    ffn = f'{ffn}.json'
    if os.path.exists (ffn) :
      os.remove (ffn)
    else :
      print(f'The {ffn} does not exist')
    return
