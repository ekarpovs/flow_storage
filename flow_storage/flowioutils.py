import os, re, os.path
import cv2
import numpy as np
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
      FlowDataType.JSON: self._json_reader,
      FlowDataType.IMAGE: self._image_reader,
      FlowDataType.POINTS: self._points_reader
    }
    return readers.get(rtype)

  def writer(self, rtype: FlowDataType) -> Callable:
    writers = {
      FlowDataType.JSON: self._json_writer,
      FlowDataType.IMAGE: self._image_writer,
      FlowDataType.POINTS: self._points_writer
    }
    return writers.get(rtype)

  def cleaner(self, rtype: FlowDataType) -> Callable:
    cleaners = {
      FlowDataType.JSON: self._json_cleaner,
      FlowDataType.IMAGE: self._image_cleaner,
      FlowDataType.POINTS: self._points_cleaner
    }
    return cleaners.get(rtype)


  @staticmethod
  def _image_reader(ffn: str) -> np.dtype:
    ffn = f'{ffn}.jpg'
    return cv2.imread(ffn, cv2.IMREAD_UNCHANGED)

  @staticmethod
  def _json_reader(ffn: str) -> Dict:
    return {}

  @staticmethod
  def _points_reader(ffn: str) -> List:
    return []

  @staticmethod
  def _image_writer(ffn: str, image: np.dtype) -> None:
    ffn = f'{ffn}.jpg'
    cv2.imwrite(ffn, image)
    return

  @staticmethod
  def _json_writer(ffn: str, data: Dict) -> None:
    ffn = f'{ffn}.json'
    pass

  def _points_writer(ffn: str, data: List) -> None:
    ffn = f'{ffn}.pts'
    pass

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

  @staticmethod
  def _points_cleaner(ffn: str) -> None:
    ffn = f'{ffn}.pts'
    if os.path.exists (ffn) :
      os.remove (ffn)
    else :
      print(f'The {ffn} does not exist')
    return
