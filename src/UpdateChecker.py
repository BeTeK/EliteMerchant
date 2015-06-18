import os
import os.path
import json
from urllib import request, parse
import time
import Options
import sys
import gzip
from io import BytesIO
from io import StringIO
import datetime

updateUrl='http://mahti.serv.fi/~elite/version.json'

def readJSON(filename):
  try:
    with open(Options.getPath(filename), "r") as file:
      return json.loads(file.read())
  except Exception as ex:
    print(ex)
    return None

def downloadFile(url):
  print('Downloading versionfile')
  # compression header:
  #Accept-Encoding: gzip, deflate, sdch

  file_name = url.split('/')[-1]
  header={
    #"Accept-Encoding": "gzip, deflate, sdch"
    #"Accept-Encoding": "gzip"
  }
  lastupdate=0
  updateinterval=0.5

  def formatprogress(file_size_dl,file_size):
    if file_size is not None:
      return "\r%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    else:
      return "\r%10d" % file_size_dl

  rq=request.Request(url,None,header)
  with request.urlopen(rq) as req:
    meta = req.info()
    block_sz = 8192
    filebuffer=b''
    file_size=None

    if meta.get("Content-Length") is not None:  # if we known file length, have fancy progress indication
      file_size = int(meta.get("Content-Length"))
      print("Downloading: %s Bytes: %s" % (file_name, file_size))
    else:
      print("Downloading: %s" % file_name)

    while True:
      buffer = req.read(block_sz)
      if not buffer:
          break
      filebuffer+=buffer
      if time.time()-updateinterval > lastupdate: # console may slow us down so keep update intervals
        lastupdate=time.time()
        sys.stdout.write(formatprogress(len(filebuffer),file_size))

    with open(Options.getPath(file_name), 'wb') as file:
      if meta.get('Content-Encoding') == 'gzip': # gunzip
        buf = StringIO( filebuffer )
        #buf = BytesIO( filebuffer )
        f = gzip.GzipFile(fileobj=buf)
        filebuffer = f.read()
      file.write(filebuffer)

    sys.stdout.write(formatprogress(len(filebuffer),file_size))
    print("  -  Done!")

    last_modified = meta.get('last-modified')
    #time_struct = time.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    #timestamp=time.mktime(time_struct)
    Options.set("Merchant-versionfile-lastmodified",last_modified)

    return last_modified


def update(force=False): # return None or 'http://downloadurl'
  file_name = updateUrl.split('/')[-1]
  if Options.get("Merchant-version",'?')=='?': # can't check for version without local build (nonbinary linux, macos)
    return None
  if force or checkUpdated(updateUrl) or not os.path.exists( file_name ):
    downloadFile(updateUrl)

  return checkVersionFile(updateUrl)

def checkVersionFile(url):
  file_name = url.split('/')[-1]
  versionjson=readJSON(Options.getPath(file_name))
  if versionjson is not None:
    # ignore if version is same - or version unknown (nonbinary linux, macos)
    if versionjson['versionTxt']==Options.get("Merchant-version",'?') or Options.get("Merchant-version",'?')=='?':
      return None
    else:
      print('New version available! v'+versionjson['versionTxt'])
      return versionjson
  else:
    print('versionfile not valid JSON')
    return None

def checkUpdated(url):
  with request.urlopen(url, timeout=30) as conn:
    meta=conn.info()
    last_modified = meta.get('last-modified')
    #time_struct = time.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    #timestamp=time.mktime(time_struct)
    if last_modified != Options.get("Merchant-versionfile-lastmodified",0):
      return True
  return False
