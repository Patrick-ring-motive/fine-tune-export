from api.llm.metapython import *
import os
import subprocess,sys;

try:
    import pandas
except:
    installLocal("pandas")
    import pandas
try:
    import bitsandbytes
except:
    installLocal("bitsandbytes")
    import bitsandbytes
try:
    import accelerate
except:
    installLocal("accelerate")
    import accelerate
try:
    import transformers
except:
    installLocal("transformers")
    import transformers
try:
    import datasets
except:
    installLocal("datasets")
    import datasets
try:
    import chardet
except:
    installLocal("chardet")
    import chardet
try:
    import trl
except:
    installLocal("trl")
    import trl
try:
    import peft
except:
    installLocal("peft")
    import peft
try:
    import sentencepiece
except:
    installLocal("sentencepiece")
    installLocal("flash-attn")
    import sentencepiece
try:
    import tensorboardX
except:
    installLocal("tensorboardX")
    import tensorboardX
