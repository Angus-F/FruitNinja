from multiprocessing import Process, Pipe, Manager
import game
import new_cv
import test
import time


if __name__ == '__main__':
    mgr = Manager()
    pos = mgr.list()
    pos.append([300,200])
    # p1 = Process(target=test.main, args=(pos,))
    p1 = Process(target=new_cv.main, args=(pos,))
    # p2 = Process(target=test.main, args=(pos,))
q    p2 = Process(target=game.main, args=(pos,))
    p1.start()
    p2.start()
    p2.join()
    p1.join()