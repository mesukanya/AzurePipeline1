import requests
import json
import os
from base64 import b64encode, b64decode,standard_b64encode

TOKEN = b'<dapi44b4b778ae2170aeb00962ba760adb05>'
headers = {"Authorization": b"Basic " + standard_b64encode(b"token:" + TOKEN)}
url = "https://eastus2.azuredatabricks.net/api/2.0"
dbfs_dir = "dbfs:/FileStore/"

def perform_query(path, headers, data={}):
  session = requests.Session()
  resp = session.request('POST', url + path, data=json.dumps(data), verify=True, headers=headers)
  return resp.json()

def mkdirs(path, headers):
  _data = {}
  _data['path'] = path
  return perform_query('/dbfs/mkdirs', headers=headers, data=_data)

def create(path, overwrite, headers):
  _data = {}
  _data['path'] = path
  _data['overwrite'] = overwrite
  return perform_query('/dbfs/create', headers=headers, data=_data)

def add_block(handle, data, headers):
  _data = {}
  _data['handle'] = handle
  _data['data'] = data
  return perform_query('/dbfs/add-block', headers=headers, data=_data)

def close(handle, headers):
  _data = {}
  _data['handle'] = handle
  return perform_query('/dbfs/close', headers=headers, data=_data)

def put_file(src_path, dbfs_path, overwrite, headers):
  handle = create(dbfs_path, overwrite, headers=headers)['handle']
  print("Putting file: " + dbfs_path)
  with open(src_path, 'rb') as local_file:
    while True:
      contents = local_file.read(2**20)
      if len(contents) == 0:
        break
      add_block(handle, b64encode(contents).decode(), headers=headers)
    close(handle, headers=headers)

mkdirs(path=dbfs_dir, headers=headers)
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
  if ".png" in f:
    target_path = dbfs_dir + f
    resp = put_file(src_path=f, dbfs_path=target_path, overwrite=True, headers=headers)
    if resp == None:
      print("Success")
    else:
      print(resp)
