import asyncio
import sys

# from core.scripts.adduser import add_user

command_list = {
    # "adduser": add_user
}


def execute_command(sys_argv: sys.argv):
    if len(sys_argv) >= 2:
        try:
            asyncio.run(command_list[sys_argv[1]]())
        except ValueError:
            print("Command not found")
        exit(1)
