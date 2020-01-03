import time

from werkzeug.local import LocalStack
import threading

# LocalStack() 作为 Stack 的 功能
# s = LocalStack()
# s.push(1)
# print(s.top)
# print(s.top)
# print(s.pop())
# print(s.top)
#
# s.push(1)
# s.push(2)
# print(s.top)

my_local_stack = LocalStack()
my_local_stack.push(1)
print(threading.current_thread().getName(), my_local_stack.top)


def worker():
    print(threading.current_thread().getName(), my_local_stack.top)
    my_local_stack.push(2)
    print(threading.current_thread().getName(), my_local_stack.top)


child_thread = threading.Thread(target=worker, name='ChildThread')
child_thread.start()
time.sleep(1)

print(threading.current_thread().getName(), my_local_stack.top)

# MainThread 1
# ChildThread None
# ChildThread 2
# MainThread 1

