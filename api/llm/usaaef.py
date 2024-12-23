from api.llm.metapython import *
from api.llm.installs import *


import gc
torch.cuda.empty_cache()
gc.collect()
gc.collect()

import sys
fromImport("datasets",["load_dataset"])
fromImport("transformers",["AutoModelForCausalLM", "AutoTokenizer","BitsAndBytesConfig","HfArgumentParser","TrainingArguments","pipeline","logging"])
fromImport("peft",["LoraConfig", "PeftModel"])
from trl import SFTTrainer
import time



model_name = "Weblet/llama-2-usaaef2c"

max_seq_length = 512 # Maximum sequence length to use
device_map = {"": 0} #  Load the entire model on the GPU 0



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
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=max_seq_length)

def talk(prompt):
    result = pipe(f"<s>[INST] {prompt} [/INST]")
    return result[0]['generated_text']