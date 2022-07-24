'''
 Flow storage tester
 Usage:
   python run.py -ws <ws path> [-t no/yes]
'''

import sys
import json
import argparse

from flow_model import FlowModel

from flow_storage import *

# Construct the argument parser and parse the arguments
def parseArgs():
  ap = argparse.ArgumentParser(description="flow storage")
  ap.add_argument("-w", "--ws", required = True,
	help = "full path to the worksheet")
  ap.add_argument("-t", "--trace", required = False,
  default="no",
	help = "print output")
  
  args = ap.parse_args()   
  kwargs = dict((k,v) for k,v in vars(args).items() if k!="message_type")
  return kwargs

# Reads the string from the file, parses the JSON data, 
# populates a Python dict with the data
def readJson(ffn):
  with open(ffn, 'rt') as f:
    data = json.load(f)
  return data

def set_runtime_environment(cfg):
  actions_paths = cfg.get('user-actions-paths')
  for path in actions_paths:
    sys.path.append(path)


# Main function
def main(**kwargs):
  ws = readJson(kwargs.get("ws"))
  model = FlowModel(ws)

  cfg_path = './cfg/cfg.json'
  cfg = readJson(cfg_path)
  set_runtime_environment(cfg)

  config = FlowStorageConfig(cfg)
  storage = FlowStorage(config, model.get_as_ws())
 
  for state in storage.storage:
    print('state_id', state.state_id)
    io_data = state.input_data
    if io_data is not None:
      print('input type', io_data.io_type)
      for data_ref in io_data.data_refs:
        print('data type', data_ref.data_type)
        print('internal ref', data_ref.int_ref)
        print('external ref', data_ref.ext_ref)
    io_data = state.output_data
    if io_data is not None:
      print('input type', io_data.io_type)
      for data_ref in io_data.data_refs:
        print('data type', data_ref.data_type)
        print('internal ref', data_ref.int_ref)
        print('external ref', data_ref.ext_ref)

# Entry point
if __name__ == "__main__":
    kwargs = parseArgs()
    main(**kwargs) 
