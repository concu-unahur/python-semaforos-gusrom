import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

comensal=threading.Semaphore(1)
cocinero=threading.Semaphore(0)
platosDisponibles = 3

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    while (True):
      cocinero.acquire()
      try:
        logging.info('Reponiendo los platos...')
        platosDisponibles = 3
      finally:
        comensal.release()

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    comensal.acquire()
    try:
      if platosDisponibles==0:
        cocinero.release()
        comensal.acquire()
      
      platosDisponibles -= 1
      logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
    finally:
      comensal.release()


Cocinero().start()

for i in range(5):
  Comensal(i).start()

