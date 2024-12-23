def none():
  return None


def Q(function, parameters):
  try:
    return function(*parameters)
  except:
    return None


async def AQ(function, parameters):
  try:
    return await function(*parameters)
  except:
    return None

def b(str):
  return bytes(f"{str}", 'utf8')

false = False
true = True


def delete(obj, attr):
  try:
    del obj[attr]
    return obj
  except:
    return obj

def println(*args, **kwargs):
    return print(*args,"\n",**kwargs)

def at(obj,index):
    try:
        try:
            return obj[index[0]]
        except:
            return obj[index]
    except:
        return None