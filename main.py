# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
from Play import Board, Player

pandemic_board_game = Board()
print(pandemic_board_game.Washington.has_supply_center)
player = Player("farmer", pandemic_board_game.Elysium,  1, ["a"])
print(player.player_number)

print(len(pandemic_board_game.infection_deck))

counter = 1
list1 = [1, 2]
list2 = list1
while counter <= 3:
    list1.extend(list2)
    print(list1)
    print(len(list2))
    counter += 1
print(list1)


