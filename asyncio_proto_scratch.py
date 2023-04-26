from asyncio_proto import init, send, spawn

def main():
    a = spawn(running_total, 0)
    send(a, ('print',))
    spawn(prompt, a)



async def prompt(pid):
    command = tuple(input('Enter a command: ').split())
    send(pid, command)
    match command:
        case ('stop',):
            return
        case _:
            send(pid, ('print',))
            recurse(pid)


async def running_total(n):
    match await receive():
        case ('print',):
            print(f'Current total: {n}')
            recurse(n)
        case ('add', x):
            print(f'Adding {x}...')
            recurse(n + int(x))
        case ('stop',):
            return
        case (command,):
            print(f'Unrecognized command {command}.')
            recurse(n)


if __name__ == '__main__':
    init(main)
