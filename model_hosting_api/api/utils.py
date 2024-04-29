import asyncio
from .sementic_kernel_client import init_kernel

kernel = init_kernel()


async def run_prompt(prompt):
    response = await kernel.invoke('chat-gpt', prompt)
    return response
