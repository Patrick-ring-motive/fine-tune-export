import os
#os.chdir('/workspace/pring/fine-tune/');
import sys
sys.path.append('/workspace/pring/fine-tune/server/Async-Python-Server')
import torch
import transformers
print(os.getcwd())
#os.chdir('/workspace/pring/fine-tune/server/Async-Python-Server');
print(os.getcwd())
from api.llm.metapython import *
from api.llm.installs import *
importLib("pandas")
from urllib.parse import quote
from urllib.parse import unquote
import time



import gc
torch.cuda.empty_cache()
gc.collect()
gc.collect()

magic('nvidia-smi')

import sys
fromImport("datasets",["load_dataset"])
fromImport("transformers",["AutoModelForCausalLM", "AutoTokenizer","BitsAndBytesConfig","HfArgumentParser","TrainingArguments","pipeline","TextStreamer","TextIteratorStreamer","logging"])
fromImport("peft",["LoraConfig", "PeftModel"])
from trl import SFTTrainer
import time
from threading import Thread
from api.xpy import *


model_name = "Weblet/llama-2-usaaef2c"

max_seq_length = 512 # Maximum sequence length to use
device_map = {"": 0} #  Load the entire model on the GPU 0

import gc
gc.collect()
gc.collect()

import locale
locale.getpreferredencoding = lambda: "UTF-8"

model=AutoModelForCausalLM.from_pretrained(
    model_name,
    low_cpu_mem_usage=True,
    return_dict=True,
    torch_dtype=torch.float16,
    device_map=device_map,
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right" # Fix weird overflow issue with fp16 training

logging.set_verbosity(logging.CRITICAL)

streamer = TextStreamer(tokenizer, skip_prompt=True)

def streamWriter(str):
    txt=''
    transaction_id=''
    for s in str:
        txt+=tokenizer.decode(s)
        if 'TRANSACIONT_ID' in txt:
            transaction_id=txt.split('TRANSACIONT_ID')[1].split('<')[0].split('[')[0];
            transaction_id
   # print(txt)
    stream=streamWriter.responseStream
    if at(streamWriter.requestMap,[transaction_id]) != None:
        stream = at(streamWriter.requestMap,[transaction_id])
    if stream != None:
        zwrite_response_body(streamWriter.responseStream, b(f"{txt} "))
streamWriter.responseStream=None
streamWriter.requestMap={}
streamer.put=streamWriter
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=max_seq_length,streamer=streamer)

prompt_seed = """You are a chatbot called Hawkeye with the purpose of serving USAA members.
Your goal is to give sound financial advice to USAA members and to direct USAA members where to find additional resources to guide them through their financial journey."""


def talk(prompt):
    result = pipe(f"<s>[INST] {prompt} [/INST]")
    return result[0]['generated_text']
async def talks(prompt,transaction_id=''):
    return pipe(f"<pre>{prompt_seed}</pre>{transaction_id}<s>[INST] As an inquiring USAA Member, I am curious. {prompt} [/INST]")


print(talk(prompt_seed))


from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio
import time
import os
from api.xpy import *
import sys
import socket
import platform
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
      print(f"Recieved {request.path}")
      if(request.path.startswith('/talk')):
          transaction_id=f"TRANSACTION_ID{time.time()}".replace('.','');
          streamWriter.responseStream=request
          streamWriter.requestMap[transaction_id]=request;
          await zsendHeaders(request,{'status':200,'Content-type':'text/plain'})
          content=await talks(unquote(f"{at(request.path.split('/talk?'),[1])}"),transaction_id=transaction_id)
          text=f"[FULLTEXT]{content[0]['generated_text']}"
          print(f'responding{text}')
          await zwriteResponseBody(request, b(text))
          del streamWriter.requestMap[transaction_id]
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

println("\n\nPlatform Node: ",platform.node())
println("Version Info: ",sys.version_info)
println("Hostname: ",socket.gethostname())
println("FQDN: ",socket.getfqdn())

httpd = ThreadingHTTPServer(('', 8080), handler)
httpd.timeout = 30
httpd.serve_forever()