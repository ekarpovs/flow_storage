import os, re, os.path
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
      FlowDataType.IMAGE: self._image_reader,
      FlowDataType.JSON: self._json_reader,
      FlowDataType.POINTS: self._points_reader
    }
    return readers.get(rtype)

  def writer(self, rtype: FlowDataType) -> Callable:
    writers = {
      FlowDataType.IMAGE: self._image_writer,
      FlowDataType.JSON: self._json_writer,
      FlowDataType.POINTS: self._points_writer
    }
    return writers.get(rtype)

  def _image_reader(self, pat):
    pass

  def _json_reader(self):
    pass

  def _points_reader(self):
    pass

  def _image_writer(self):
    pass

  def _json_writer(self):
    pass

  def _points_writer(self):
    pass