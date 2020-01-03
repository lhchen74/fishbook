import threading
import time
from werkzeug.local import Local
# Local() 是使用字典实现的线程隔离对象，使用线程 id 作为 key
# LocalStack() 封装了 Local() 的线程隔离的栈结构
obj = Local()
obj.a = 'a'


def worker():
    obj.a = 'b'
    w_t = threading.current_thread()
    print(w_t.getName(), obj.a)


new_t = threading.Thread(target=worker, name="babb")
new_t.start()
time.sleep(1)

t = threading.current_thread()
print(t.getName(), obj.a)
