import os
os.chdir('/workspace/pring/fine-tune/');
import torch
import pandas
os.chdir('/workspace/pring/fine-tune/');
import transformers
os.chdir('/workspace/pring/fine-tune/');
from transformers import(AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig,HfArgumentParser,TrainingArguments,pipeline,logging)
print(os.getcwd())
os.chdir('/workspace/pring/fine-tune/server/Async-Python-Server');
print(os.getcwd())
from api.llm.metapython import *
from api.llm.installs import *


from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import asyncio
from api.promises import *
from api.excepts import *
from api.xhttp import *
from api.zfile import *
from api.xpy import *
import os
import mimetypes
mimetypes.init()



class handler(BaseHTTPRequestHandler):

  async def do_ASYNC(request, data):
      if(request.path=='/talk'):
          content=talk('hello')
          await zsendHeaders(request,{'status':200,'Content-type':'text/plain'})
          await zwriteResponseBody(request, content)
      else:
          path = f"{os.getcwd()}{request.path}".split("?")[0].split("#")[0];
          contentType = mimetypes.guess_type(path,strict=False)
          print(path,contentType[0])
          content = await zreadFileBytes(path)
          await zsendHeaders(request,{'status':200,'Content-type':contentType[0]})
          await zwriteResponseBody(request, content)

  def do_METHOD(request):
    asyncio.run(request.do_ASYNC(request))

  do_GET = do_METHOD
  do_OPTIONS = do_METHOD
  do_POST = do_METHOD
  do_PUT = do_METHOD
  do_PATCH = do_METHOD
  do_HEAD = do_METHOD
  do_DELETE = do_METHOD
  do_CONNECT = do_METHOD
  do_TRACE = do_METHOD