# Workshop Flow Storage

## It is a part of the [Image Processing Workshop](https://github.com/ekarpovs/image-processing-workshop) project. Stores a flow steps output

### File system structure

    Anywhere in a file system:
_____
    |__ /data/ __ files for processing
    |
    

    |__ /flow_storage/ The project files
    |

## Local Installation

```bash
cd flow_storage
pip install -e . --use-feature=in-tree-build
```

## Test

```bash
python run.py -p <storage path> -d <fsm definition>
```
