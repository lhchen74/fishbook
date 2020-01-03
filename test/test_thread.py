import threading
import time


def worker():
    w_t = threading.current_thread()
    time.sleep(3)
    print(w_t.getName())


new_t = threading.Thread(target=worker, name="babb")
new_t.start()

t = threading.current_thread()
print(t.getName())


