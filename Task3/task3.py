from threading import Thread, Lock

a = 0


def function(lock, arg):
    global a
    for _ in range(arg):
        lock.acquire()
        try:
            a += 1
        finally:
            lock.release()


def main():
    lock = Lock()
    threads = []
    for _ in range(5):
        thread = Thread(target=function, args=(lock, 1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]

    print("----------------------", a)  # ???


if __name__ == '__main__':
    main()
