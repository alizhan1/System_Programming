from multiprocessing import Process, Pipe
from multiprocessing.sharedctypes import Value, Array

def darth_vader(conn, value):
    message = "- Luke, I am {} father!\n".format(value)
    conn.send(message)
    conn.close()


def luke(conn, value):
    message = "- Then, I am {} child!\n".format(value)
    conn.send(message)
    conn.close()
    

if __name__ == '__main__':
    parent_con, child_con = Pipe()
    arr = Array("c", "your")


    p1 = Process(target=darth_vader, args=(parent_con, arr.value))
    p2 = Process(target=luke, args=(child_con, arr.value))

    p1.start()
    print(child_con.recv())
    p1.join()
    print("---------------------------")
    p2.start()
    print(parent_con.recv())
    p2.join()