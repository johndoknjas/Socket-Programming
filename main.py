from multiprocessing import Process, Pipe, Queue
import time
from random import randint
import sys

def sender_func(conn, q):
    # For now, generate random data for packets.
    print(randint(0,1))
    
    while True:
        q.put([randint(0,1024), True if randint(0,1) == 0 else False,
              True if randint(0,1) == 0 else False, 
              True if randint(0,1) == 0 else False])
        
        time.sleep(2)
    

def receiver_func(conn, q):
    
    while True:
        print(q.get())


def main():
    sender_conn, receiver_conn = Pipe()
    
    q = Queue()
    
    p1 = Process(target=sender_func, args=(sender_conn, q,))
    p1.start()
    
    p2 = Process(target=receiver_func, args=(receiver_conn, q,))
    p2.start()
    
    p1.join()
    p2.join()

if __name__ == '__main__':
    main()
    
    
    
    