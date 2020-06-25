from multiprocessing import Process, Pipe

def sender_func(conn):
    pass

def receiver_func(conn):
    pass


def main():
    sender_conn, receiver_conn = Pipe()
    
    p1 = Process(target=sender_func, args=(sender_conn,))
    p2 = Process(target=receiver_func, args=(receiver_conn,))
    
    p1.start()
    p2.start()
    
    
    
    p1.join()
    p2.join()

if __name__ == '__main__':
    main()
    
    
    
    