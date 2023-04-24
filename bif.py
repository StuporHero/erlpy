from asyncio import Queue, new_event_loop


def sequence():
    i = 1
    while True:
        yield i
        i += 1


process_id = sequence()
loop = new_event_loop()
post_office = {}


def init(func):
    loop.call_soon(func)
    loop.run_forever()


async def process_wrapper(pid, func, state, mailbox):
    should_recurse = False
    recursive_state = None
    async def receive():
        nonlocal pid
        return await mailbox.get()
    def recurse(*args):
        nonlocal should_recurse
        nonlocal recursive_state
        should_recurse = True
        recursive_state = args
    func.__globals__['receive'] = receive
    func.__globals__['recurse'] = recurse
    func.__globals__['spawn'] = spawn
    await func(*state)
    if mailbox.qsize() > 0:
        mailbox.task_done()
    if should_recurse:
        loop.create_task(process_wrapper(pid, func, recursive_state, mailbox))
    else:
        post_office.pop(pid)
        if len(post_office.keys()) == 0:
            loop.stop()


def spawn(func, *state):
    pid = next(process_id)
    post_office[pid] = mbox = Queue()
    loop.create_task(process_wrapper(pid, func, state, mbox))
    return pid


def send(pid, message):
    post_office[pid].put_nowait(message)
