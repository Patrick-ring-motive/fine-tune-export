from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio
import time
import os
from api.promises import *
import sys, threading
#from api.excepts import *
import copy

def logerr(e):
  if hasattr(e, 'message'):
    print(e.message)
  else:
    print(e)

def globalThis():
  return

globalThis.blankResponse = None

async def sendResponse(request, status):
  return request.send_response(status)

async def zsendResponse(request, status):
  try:
    await sendResponse(request, status)
  except Exception as e:
    logerr(e)

async def endHeaders(request):
  return request.end_headers()

async def zendHeaders(request):
  try:
    await endHeaders(request)
  except Exception as e:
    logerr(e)

async def sendHeader(request,k,v):
  return request.send_header(k,v)

async def zsendHeader(request,k,v):
  try:
    await sendHeader(request,k,v)
  except Exception as e:
    logerr(e)

async def sendHeaders(request, headers):
  if "status" in headers:
    await sendResponse(request, headers["status"])
  for k in headers:
    await sendHeader(request, k, headers[k])
  return await endHeaders(request)

async def zsendHeaders(request, headers):
  if "status" in headers:
    await zsendResponse(request, headers["status"])
  for k in headers:
    await zsendHeader(request, k, headers[k])
  return await zendHeaders(request)

async def readResponseBody(res, length):
  try:
    bdy = bytearray(length + 16)
    res.readinto(bdy)
    return bdy
  except:
    try:
      return res.read()
    except:
      return b''


def closeRequest(request):
  if 'close' in request.close:
    none()


def reboot():
  #httpd.shutdown()
  httpd.serve_forever()


async def atimeout(request, seconds):
  await asyncio.sleep(seconds)
  request.isTimedOut = true
  ct = 'text/html'
  code = 408
  writeEnd = b'408 /*<script src="/injects.js"></script><style hideme>html:has([hideme]){visibility:hidden;}</style>*/'
  if '.css' in request.path:
    ct = 'text/css'
    code = 200
    writeEnd = b''
  if '.js' in request.path:
    return closeRequest(request)
    ct = 'text/javascript'
    code = 200
    writeEnd = b''
  request.send_response(code)
  request.send_header('Content-type', ct)
  await endHeaders(request)
  rtrn = await writeResponseBody(request, writeEnd)
  if 'planetpython' in request.headers['Host']:
    closeRequest(request)
  await AQ(streamDetach, [request.wfile])
  if request.headers['Host'] in request.globalThis.hostShortCircuit:
    closeRequest(request)
  return rtrn

def zwrite_response_body(request, body):
    try:
        return request.wfile.write(body)
    except Exception as e:
        logerr(e)

async def writeResponseBody(request, body):
    return request.wfile.write(body)

async def zwriteResponseBody(request, body):
  try:
    return await writeResponseBody(request, body)
  except Exception as e:
    logerr(e)


async def readRequest(req, length):
  if length < 5:
    return b''
  return req.rfile.read(length)


async def connectClient(host):
  return http.client.HTTPSConnection(host)


async def connectRequest(connection, requestCommand, requestPath, requestBody,
                         requestHeaders):
  return connection.request(requestCommand,
                            requestPath,
                            body=requestBody,
                            headers=requestHeaders)


async def connectResponse(connection):
  return connection.getresponse()


async def connectClose(connection):
  connection.close()


async def streamDetach(stream):
  stream.detach()


async def readBody(req, host):
  reqBody = None
  requestBodyLength = req.headers['Content-Length']
  if (req.rfile.readable() and requestBodyLength):
    reqBody = await readRequest(req, int(requestBodyLength))
    if len(reqBody) < 5:
      reqBody = None
  return reqBody


def bustCache(path):
  hash = ''
  if '#' in path:
    hash = '#' + path.split('#')[1]
  char = '?'
  if '?' in path:
    char = '&'
  return path.split('#')[0] + char + 'bustcache=' + str(time.time()).replace(
    '.', '')


def stripHostParam(path):
  if '?hostname=' in path:
    if '&' in path:
      hostparts = path.split('?hostname=')
      params = hostparts[1].split('&')
      params[0] = ''
      params = '&'.join(params).split()
      params[0] = '?'
      path = hostparts[0] + ''.join(params)
    elif '#' in path:
      hostparts = path.split('?hostname=')
      hash = hostparts[1].split('#')
      hash[0] = ''
      path = hostparts[0] + '#'.join(hash)
  elif '&hostname=' in path:
    hostparts = path.split('&hostname=')
    if '&' in hostparts[1]:
      params = hostparts[1].split('&')
      params[0] = ''
      path = hostparts[0] + '&'.join(params)
    elif '#' in path:
      hostparts = path.split('&hostname=')
      hash = hostparts[1].split('#')
      hash[0] = ''
      path = hostparts[0] + '#'.join(hash)
  return path


httpd = {}


async def fetchResponse(req, host):
  connection = {}
  try:
    connectionPromise = await go(await promise(connectClient, [host]))
    reqBodyPromise = await go(await promise(readBody, [req, host]))
    reqHeaders = {}
    for header in req.headers:
      reqHeaders[header] = req.headers[header].replace(req.localhost, host)
    reqHeaders['Localhost'] = req.localhost
    reqHeaders['Cache-Control'] = 'max-age='
    reqHeaders['Expires'] = 'Tue, 19 Jan 2000 03:14:07 GMT'
    delete(reqHeaders, 'Etag')
    delete(reqHeaders, 'Expect-Ct')
    delete(reqHeaders, 'Cookie')
    reqBody = await reqBodyPromise
    connection = await connectionPromise
    await connectRequest(connection, req.command, req.path, reqBody,
                         reqHeaders)
    res = await connectResponse(connection)
    res.connection = connection
    return res
  except:
    res = NewResponse()
    NewResponse.status = 500
    res.connection = connection
    return res

async def fetchURL(url):
  connection = {}
  host = url.split('/')[2]
  path = url.split(host)[1]
  try:
    connection = await connectClient(host)
    await connectRequest(connection, 'GET', path,b'',{})
    res = await connectResponse(connection)
    res.connection = connection
    return res
  except:
    res = NewResponse()
    NewResponse.status = 500
    res.connection = connection
    return res

def NewResponse():
    conn = http.client.HTTPSConnection('www.python.org')
    conn.request('GET','/');
    return conn.getresponse()
