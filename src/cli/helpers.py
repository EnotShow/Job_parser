from typing import Awaitable


def run_command_async(command: Awaitable) -> None:
    import asyncio

    asyncio.run(command)
