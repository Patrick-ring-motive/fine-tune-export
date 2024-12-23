def b(str):
  return bytes(f"{str}", 'utf8')

async def zreadFile(filename):
    return zread_file(filename)

def zread_file(filename):
  try:
    thisFile = open(filename, "r") 
    txt = thisFile.read()
    thisFile.close()
    return txt
  except Exception as e:
    if hasattr(e, 'message'):
        return e.message
    else:
        return f"{e}"

async def zreadFileBytes(filename):
    return zread_file_bytes(filename)

def zread_file_bytes(filename):
    try:
        thisFile = open(filename, mode="rb") 
        bts = thisFile.read()
        thisFile.close()
        return bts
    except Exception as e:
        if hasattr(e, 'message'):
            return b(e.message)
        else:
            return b(f"{e}")