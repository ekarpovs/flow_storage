import os, os.path
import cv2
import numpy as np
import json
from typing import Dict, List, Tuple

class FlowIOUtilsFs():
  def __init__(self) -> None:
      pass

  def clean_ext_storage(self, path: str) -> None:
    for root, dirs, files in os.walk(path):
      for file in files:
        os.remove(os.path.join(root, file))
    return

# Readers
  def np_array_reader(self, ffn: str) -> np.ndarray:
    ffn = f'{ffn}.npy'
    return np.load(ffn)

  def json_reader(self, ffn: str) -> Dict:
    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      data = json.load(f)
      return data

  def list_np_arrays_reader(self, ffn: str) -> List[np.ndarray]:
    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      ld = json.load(f)
      data = [np.array(d) for d in ld]
      return data

  def list_tuples_reader(self, ffn: str) -> List[Tuple]:
    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      ld = json.load(f)
      data = [np.array(d) for d in ld]
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

    ffn = f'{ffn}.json'
    with open(ffn, 'rt') as f:
      data = json.load(f)
      list_kps = _list_dict_to_list_key_points(data)
      return list_kps

# Writers
  def np_array_writer(self, ffn: str, arr: np.ndarray) -> None:
    ffn = f'{ffn}.npy'
    np.save(ffn, arr)
    return

  def list_np_arrays_writer(self, ffn: str, data: List[np.ndarray]) -> None:
    ffn = f'{ffn}.json'
    sd = [d.tolist() for d in data]
    with open(ffn, 'w') as fp:
      json.dump(sd, fp, indent=2)
    return

  def json_writer(self, ffn: str, data: Dict) -> None:
    ffn = f'{ffn}.json'
    with open(ffn, 'w') as fp:
      json.dump(data, fp, indent=2)
    return

  def list_tuples_writer(self, ffn: str, data: List[Tuple]) -> None:
    ffn = f'{ffn}.json'
    with open(ffn, 'w') as fp:
      json.dump(data, fp, indent=2)
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

    ffn = f'{ffn}.json'
    kps = _list_key_points_to_List_dict(data)
    with open(ffn, 'w') as fp:
      json.dump(kps, fp, indent=2)
    return

# Cleaner
  def data_cleaner(self, ext: str) -> None:
    extension = ext
    
    def _cleaner( fn: str):
      ffn = f'{fn}.{extension}'
      if os.path.exists (ffn) :
        os.remove (ffn)
      else :
        print(f'The {ffn} does not exist')
      return
    return _cleaner
