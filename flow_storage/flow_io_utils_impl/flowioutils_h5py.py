import json
import os
import cv2
import numpy as np
import h5py
import ast

from typing import Dict, List, Tuple

from ..flowstorageconfig import FlowStorageConfig


class FlowIOUtilsH5Py():
  def __init__(self, config: FlowStorageConfig) -> None:
    db_ffn = f'{config.storage_location}/data.hdf5'
    if os.path.exists (db_ffn) :
      os.remove (db_ffn)
    self._db = h5py.File(db_ffn, "a")
    return

  def close(self) -> None:
    self._db.close()
    return

  def clean_ext_storage(self) -> None:
    keys = self._db.keys()
    for key in keys:
      del self._db[key]
    return

# Readers
  def np_array_reader(self, fn: str) -> np.ndarray:
    dataset = self._db.get(fn)
    return np.array(dataset)

  def json_reader(self, fn: str) -> Dict:
    dataset = self._db.get(fn)
    if dataset is not None:
      dataset = dataset.asstr()[()]
      dataset = json.loads(dataset)
    return dataset

  def list_np_arrays_reader(self, fn: str) -> List[np.ndarray]:
    dataset = self._db.get(fn)
    return list(np.array(dataset))

  def list_of_lists_np_arrays_reader(self, fn: str) -> List[List[np.ndarray]]:
    dataset = self._db.get(fn)
    return list(np.array(dataset))


  def list_tuples_reader(self, fn: str) -> List[Tuple]:
    dataset = self._db.get(fn).asstr()[()]
    return dataset

  def list_keypoints_reader(self, ffn: str) -> List[cv2.KeyPoint]:

    def _list_dict_to_list_key_points(data: List[Dict]) -> List[cv2.KeyPoint]:
      list_kps = []
      for kp_dict in data:
        angle = kp_dict.get('angle'),
        class_id = kp_dict.get('class_id'),
        ptl = kp_dict.get('pt'),
        x = ptl[0][0]
        y = ptl[0][1]
        octave = kp_dict.get('octave'),
        response = kp_dict.get('response'),
        size = kp_dict.get('size')
        # kp = cv2.KeyPoint(x, y, size, angle, response, octave, class_id)
        kp = cv2.KeyPoint(x, y, size)
        list_kps.append(kp)
      return list_kps

    data = {}
    return data

# Writers
  def np_array_writer(self, fn: str, arr: np.ndarray) -> None:
    keys = self._db.keys()
    if fn in keys:
      del self._db[fn]
    self._db.create_dataset(fn, data=arr)
    # dataset[fn] = arr.astype(h5py.opaque_dtype(arr.dtype))
    return

  def list_np_arrays_writer(self, fn: str, data: List[np.ndarray]) -> None:
    keys = self._db.keys()
    if fn in keys:
      del self._db[fn]
    self._db.create_dataset(fn, data=data)
    return

  def list_of_lists_np_arrays_writer(self, fn: str, data: List[List[np.ndarray]]) -> None:
    keys = self._db.keys()
    if fn in keys:
      del self._db[fn]

    # contours = []
    # max_length = max(map(len, cntrs))
    # for contour in cntrs:
    #   c_h, c_w, c_c = contour.shape
    #   contour_arr = np.full(max_length, 0, dtype=np.int32)
    #   # contour_arr = np.pad(contour, ((0, 0),(0, 0),(0, 0)))
    #   contour_arr = np.pad(contour, (0, 0))
    #   # contour_arr[:len(contour)] = contour
    
    self._db.create_dataset(fn, data=data)
    return


  def json_writer(self, fn: str, data: Dict) -> None:
    keys = self._db.keys()
    if fn in keys:
      del self._db[fn]
    str_data = json.dumps(data)
    self._db.create_dataset(fn, data=str_data)
    return

  def list_tuples_writer(self, fn: str, data: List[Tuple]) -> None:
    keys = self._db.keys()
    if fn in keys:
      del self._db[fn]
    str_data = json.dumps(data)
    self._db.create_dataset(fn, data=str_data)
    return

  def list_keypoints_writer(self, ffn: str, data: List[cv2.KeyPoint]) -> None:

    def _list_key_points_to_List_dict(data: List[cv2.KeyPoint]) -> List[Dict]:
      list_dict = []
      for kp in data:
        kp_dict = {
          'angle': kp.angle,
          'class_id': kp.class_id,
          'pt': kp.pt,
          'octave': kp.octave,
          'response': kp.response,
          'size': kp.size
          }
        list_dict.append(kp_dict)
      return list_dict

    return

# Cleaner
  def data_cleaner(self, ext: str) -> None:
    extension = ext
    
    def _cleaner( fn: str):
      keys = self._db.keys()
      if fn in keys:
        del self._db[fn]
      return
    return _cleaner
