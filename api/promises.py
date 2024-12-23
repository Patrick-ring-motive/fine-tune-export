import asyncio
from api.xpy import *


#astart() starts unawaited async tasks declared at this level. go does the same but returns the the task passed to it. This lets me start a task and return the promise on the same line.
async def astart():
  a = await asyncio.sleep(0)
  return a


async def go(task):
  await asyncio.sleep(0)
  return task


async def promise(task, parameters):
  if len(parameters) > 0:
    task = asyncio.create_task(task(*parameters))
  else:
    task = asyncio.create_task(task())
  await astart()
  task.start = astart
  task.resolved = False
  return task
