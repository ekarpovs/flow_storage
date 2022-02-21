import cv2
import numpy as np
import h5py

from typing import Dict, List, Tuple

from ..flowstorageconfig import FlowStorageConfig


class FlowIOUtilsH5Py():
  def __init__(self, config: FlowStorageConfig) -> None:
      self._config = config

  def clean_ext_storage(self, path: str) -> None:
    return

# Readers
  # def load_dataset(path, datasetName):
  #   # open the database, grab the labels and data, then close the dataset
  #   db = h5py.File(path, "r")
  #   (labels, data) = (db[datasetName][:, 0], db[datasetName][:, 1:])
  #   db.close()
  #   # return a tuple of the data and labels
  #   return (data, labels)


  def np_array_reader(self, ffn: str) -> np.ndarray:
    ffn = f'{ffn}.npy'
    return np.load(ffn)

  def json_reader(self, ffn: str) -> Dict:
    data = {}
    return data

  def list_np_arrays_reader(self, ffn: str) -> List[np.ndarray]:
    data = {}
    return data

  def list_tuples_reader(self, ffn: str) -> List[Tuple]:
    data = {}
    return data

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
  # def dump_dataset(data, labels, path, datasetName, writeMethod="w"):
  #   # open the database, create the dataset, write the data and labels to dataset,
  #   # and then close the database
  #   db = h5py.File(path, writeMethod)
  #   dataset = db.create_dataset(datasetName, (len(data), len(data[0]) + 1), dtype="float")
  #   dataset[0:len(data)] = np.c_[labels, data]
  #   db.close() 

  def np_array_writer(self, ffn: str, arr: np.ndarray) -> None:
    return

  def list_np_arrays_writer(self, ffn: str, data: List[np.ndarray]) -> None:
    return

  def json_writer(self, ffn: str, data: Dict) -> None:
    return

  def list_tuples_writer(self, ffn: str, data: List[Tuple]) -> None:
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
      return
    return _cleaner
