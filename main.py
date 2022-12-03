import pygame
import os
from game import Game
import asyncio
import random

async def main():
	g = Game()
	while g.running:
		g.game_loop()
		await asyncio.sleep(0)

asyncio.run(main())