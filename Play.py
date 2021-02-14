import random
import pandas as pd
import decimal as d

class Turn:
    def __init__(self, board, player):
        self.board_state = board
        self.game_end = False
        self.total_actions = 4
        self.player = player
        self.possible_actions = self.return_actions()

    def do_turn(self):
        while self.total_actions >= 0:
            self.possible_actions.sample(n=1)
            action_type = self.possible_actions["type"].values[0]

            if action_type == "step":
                location = self.possible_actions["where"].values[0]
                self.move(location)

            if action_type == "sail":
                location = self.possible_actions["where"].values[0]
                self.move(location)
                list_with_location_cards = [index for index, location_player_card in enumerate(self.player.cards) if location_player_card == location]
                chosen_card_to_remove = list_with_location_cards[0]
                new_player_deck = list(self.player.cards[:chosen_card_to_remove] + self.player.cards[:chosen_card_to_remove + 1])
                self.player.cards = new_player_deck

            if action_type == "charter":
                location = self.possible_actions["where"].values[0]
                self.move(location)
                list_with_location_cards = [index for index, location_player_card in enumerate(self.player.cards)
                                            if location_player_card == self.player.location]

                chosen_card_to_remove = list_with_location_cards[0]
                new_player_deck = list(self.player.cards[:chosen_card_to_remove] + self.player.cards[:chosen_card_to_remove + 1])
                self.player.cards = new_player_deck

            # if action_type == "build supply center":
            # if action_type == "make supplies":
            # if action_type == "deliver supplies":




    def return_sub_action_dataframe(self, type, where, actions, length=1):
        df = pd.DataFrame(
            {"action": type * length,
             "where":  where,
             "action_function": actions * length
             }
        )

        return df

    def return_actions(self):

        paths = list(self.player.location.paths)
        sail_paths = self.return_sail_locations()

        charter_paths = self.return_charter_list()
        action_dataframe = pd.DataFrame({"action": [], "where": [], "action_function": []})
        step_dataframe = self.return_sub_action_dataframe(
            type=["step"],
            where=paths,
            actions=[self.move],
            length=len(paths)
        )

        action_dataframe = pd.concat([action_dataframe, step_dataframe], axis=0, ignore_index=True)

        if len(sail_paths) > 0:
            sail_dataframe = \
                self.return_sub_action_dataframe(
                    type=["sail"],
                    where=sail_paths,
                    actions=[self.move],
                    length=len(sail_paths)
                )

            action_dataframe = pd.concat([action_dataframe, sail_dataframe], axis=0, ignore_index=True)

        if len(charter_paths) > 0:
            charter_dataframe = \
                self.return_sub_action_dataframe(
                    type=["charter"],
                    where=charter_paths,
                    actions=[self.move],
                    length=len(charter_paths)
                )

            action_dataframe = pd.concat([action_dataframe, charter_dataframe], axis=0, ignore_index=True)

        # toevoegen kleur van kaarten
        if self.count_total_cards_of_player_loc_color() == 5 and not self.player.location.has_supply_center:
            build_dataframe = \
                self.return_sub_action_dataframe(
                    type=["build supply center"],
                    where=[self.player.location],
                    actions=[self.build_supply_center]
                )

            action_dataframe = pd.concat([action_dataframe, build_dataframe], axis=0, ignore_index=True)

        if self.board_state.stockpile > 0:
            make_supplies_dataframe = \
                self.return_sub_action_dataframe(
                    type=["make supplies"],
                    where=[self.player.cards],
                    actions=[self.make_supplies]
                )

            action_dataframe = pd.concat([action_dataframe, make_supplies_dataframe], axis=0, ignore_index=True)

        if self.player.supplies_on_card > 0:

            deliver_supplies_dataframe = \
                self.return_sub_action_dataframe(
                    type=["deliver supplies"],
                    where=[self.player.location],
                    actions=[self.deliver_supplies]
                )

            action_dataframe = pd.concat([action_dataframe, deliver_supplies_dataframe], axis=0, ignore_index=True)

        return action_dataframe

    def return_sail_locations(self):
        if "produce supplies" in self.player.cards:
            sail_list = list(self.player.cards)
            sail_list.remove("produce supplies")
            return sail_list

        return list(self.player.cards)

    def return_charter_list(self):
        if self.check_charter():
            charter_list = list(self.board_state.city_list)
            charter_list.append(self.board_state.haven_list)
            return charter_list

        return list()

    def count_total_cards_of_player_loc_color(self):
        total_of_same_color = 0
        for player_card in self.player.cards:
            if hasattr(player_card, "name"):
                if player_card.color == self.player.location.color:
                    total_of_same_color += 1

        return total_of_same_color

    def check_game_end(self):
        if self.board_state.incidents == 8:
            self.game_end = True

        if len(self.board_state.player_deck) == 0:
            self.game_end = True

        if self.board_state.supply_centers == 3:
            self.game_end = True

    def check_charter(self):
        for card in self.player.cards:
            if card == self.player.location:
                return True

        return False

    def draw_player_cards(self):
        counter = 1
        while counter <= 2:
            last_card = len(self.board_state.player_deck) - 1
            draw_card = self.board_state.player_deck[last_card]

            if not draw_card == "epidemic":
                self.player.cards.append()

            if draw_card == "epidemic":
                self.work_through_epidemic()

            self.board_state.player_deck = self.board_state.player_deck[0:last_card]
            counter += 1

        if len(self.player.cards) > 7:
            cards_to_remove = self.player.cards - 7
            counter = 1
            while counter <= cards_to_remove:
                self.player.cards = self.player.cards[0:len(self.player.cards) - 1]

        self.check_game_end()

    def draw_infection_cards(self, is_epidemic, card_to_draw):
        infect_city = self.board_state.infection_deck[card_to_draw]
        if is_epidemic:
            self.board_state.stockpile += int(round(infect_city.supplies, 0))
            self.board_state.infection_deck = list(self.board_state.infection_deck[1:])
            infect_city.supplies = 0

        if not is_epidemic:
            if infect_city.supplies <= 0:
                infect_city.plagues += int(round(1, 0))
                self.board_state.incidents += round(1, 0)
                self.check_game_end()
            else:
                infect_city.supplies -= int(round(1, 0))
                self.board_state.stockpile += int(round(1, 0))

            self.board_state.infection_deck = list(self.board_state.infection_deck[0:card_to_draw])

        self.board_state.drawn_infection_deck.append(infect_city)

    def work_through_epidemic(self):
        self.draw_infection_cards(True, 0)

        self.board_state.memory_drawn_infection_deck = list(self.board_state.drawn_infection_deck)
        reshuffle_infection_cards = list(self.board_state.drawn_infection_deck)
        random.shuffle(reshuffle_infection_cards)
        self.board_state.infection_deck.extend(reshuffle_infection_cards)

        self.board_state.drawn_infection_deck = []
        self.board_state.infection_grade_pointer += int(round(1, 0))
        self.board_state.infection_grade = self.board_state.infection_grade_list[self.board_state.infection_grade_pointer]

    def infect(self):
        counter = 1
        while counter <= self.board_state.infection_grade:
            self.draw_infection_cards(False, len(self.board_state.infection_deck) - 1)
            counter += 1

    def build_supply_center(self):
        self.player.location.has_supply_center = True
        self.board_game.supply_centers += int(round(1, 0))

    def make_supplies(self):
        self.board_state.stockpile -= int(round(1, 0))
        self.player.supplies_on_card += int(round(1, 0))

    def deliver_supplies(self, number):
        self.player.location.supplies += int(round(number, 0))
        self.player.supplies_on_card -= int(round(number, 0))

    def move(self, new_location):
        self.player.location = new_location


class Board:
    def __init__(self):
        self.NewYork = Location("New York", "city", "blue")
        self.Washington = Location("Washington", "city", "blue")
        self.Jacksonville = Location("Jacksonville", "city", "yellow")
        self.Sao_Paulo = Location("Sao_Paulo", "city", "yellow")
        self.London = Location("London", "city", "blue")
        self.Cairo = Location("Cairo", "city", "black")
        self.Lagos = Location("Lagos", "city", "yellow")
        self.Tripoli = Location("Tripoli", "city", "black")
        self.Istanbul = Location("Istanbul", "city", "black")
        self.New_Urk = Location("New_Urk", "haven")
        self.Matrix = Location("Matrix", "haven")
        self.Elysium = Location("Elysium", "haven")

        self.NewYork.create_paths([self.Washington, self.Jacksonville, self.New_Urk])
        self.Washington.create_paths([self.Jacksonville, self.NewYork])
        self.Jacksonville.create_paths([self.Washington, self.Elysium])
        self.Sao_Paulo.create_paths([self.Elysium, self.Lagos])
        self.London.create_paths([self.New_Urk])
        self.Cairo.create_paths([self.Tripoli, self.Matrix])
        self.Lagos.create_paths([self.Sao_Paulo, self.Elysium])
        self.Tripoli.create_paths([self.Cairo, self.Matrix])
        self.Istanbul.create_paths([self.Cairo, self.Matrix])
        self.New_Urk.create_paths([self.London, self.NewYork, self.Matrix, self.Elysium])
        self.Matrix.create_paths([self.New_Urk, self.Cairo, self.Tripoli, self.Istanbul])
        self.Elysium.create_paths([self.Sao_Paulo, self.Lagos, self.New_Urk, self.Jacksonville, self.Matrix])

        self.player_list = []

        self.stockpile = 36
        self.incidents = 0

        self.haven_list = [self.New_Urk, self.Matrix, self.Elysium]
        self.city_list = [self.NewYork, self.Washington, self.Sao_Paulo, self.Lagos,
                          self.London, self.Cairo, self.Tripoli, self.Istanbul]

        self.infection_grade_list = [2, 2, 2, 3, 3, 4, 4, 5]
        self.infection_grade_pointer = 0
        self.infection_grade = self.infection_grade_list[self.infection_grade_pointer]
        self.supply_centers = 0

        self.player_deck = []
        self.infection_deck = self.shuffle_infection_deck()
        self.drawn_infection_deck = []
        self.memory_drawn_infection_deck = []

    def start_infecting(self):
        counter = 1
        while counter <= 3:
            last_card = len(self.infection_deck) - 1
            infect_city = self.infection_deck[last_card]

            if not infect_city.supplies == 0:
                infect_city.supplies -= 3
                infect_city.supplies = int(round(infect_city.supplies))
                self.stockpile += 3
                self.stockpile = int(round(self.stockpile, 0))

            self.infection_deck = list(self.infection_deck[0:last_card])
            self.drawn_infection_deck.append(infect_city)
            counter += 1

    def create_starting_supplies_per_location(self):
        locations = list(self.city_list)
        locations.extend(self.haven_list)
        stocks_per_city = self.stockpile/len(locations)
        for city in locations:
            city.supplies += int(round(stocks_per_city, 0))
            self.stockpile -= int(round(stocks_per_city, 0))

    def create_players(self, player_list):
        self.player_list = player_list

    def create_deck(self, size):
        deck = list(self.city_list)
        city_list = list(self.city_list)
        counter = 1
        while counter <= size:
            deck.extend(city_list)
            counter += 1

        return deck

    def define_sub_player_decks(self, deck):
        total_cards = len(deck)
        rest_cards = total_cards % 5

        length_sub_decks = int(total_cards / 5)
        sub_deck_lengths = [length_sub_decks, length_sub_decks, length_sub_decks,
                            length_sub_decks, length_sub_decks + rest_cards]

        return sub_deck_lengths

    def create_first_player_cards(self):
        for player in self.player_list:
            draw = self.player_deck[len(self.player_deck)-1]
            self.player_deck = self.player_deck[0:len(self.player_deck)-1]
            draw2 = self.player_deck[len(self.player_deck)-1]
            self.player_deck = self.player_deck[0:len(self.player_deck)-1]
            player.cards = [draw, draw2]

    def shuffle_player_deck(self):
        deck = self.create_deck(7)
        deck.extend(["produce supplies"] * 5)
        random.shuffle(deck)

        self.player_deck = list(deck)
        self.create_first_player_cards()

        sub_deck_lengths = self.define_sub_player_decks(deck)
        end_deck = []
        start_number = 0

        deck = list(self.player_deck)
        for total_cards_in_sub_deck in sub_deck_lengths:
            end_number = start_number + total_cards_in_sub_deck
            sub_deck = list(deck[start_number:end_number])
            sub_deck.append("epidemic")

            random.shuffle(sub_deck)
            end_deck.extend(sub_deck)

            start_number = end_number

        self.player_deck = list(end_deck)

    def shuffle_infection_deck(self):
        infection_deck = self.create_deck(3)
        random.shuffle(infection_deck)
        return infection_deck

    def create_player_deck(self):
        player_deck = self.create_deck(5)
        epidemics = ["epidemic", "epidemic", "epidemic", "epidemic", "epidemic"]
        player_deck.extend(epidemics)
        return player_deck


class Location:
    def __init__(self, name, location_type, color=None):
        self.name = name
        self.paths = []
        self.color = color
        self.location_type = location_type
        self.supplies = 0
        self.plagues = 0
        self.population = 3
        self.has_supply_center = False

    def create_paths(self, path_list):
        self.paths = path_list

    def add_supplies(self, supplies_added=1):
        self.supplies += supplies_added

    def remove_supplies(self, supplies_removed=1):
        self.supplies -= supplies_removed

    def add_plague(self):
        self.plagues += 1

    def remove_population(self):
        self.population -= 1


class Player:
    def __init__(self, role, location, player_number):
        self.role = role
        self.location = location
        self.abilities = ""
        self.cards = []
        self.supplies_on_card = 0
        self.player_number = player_number


# class Actions:
#     def __init__(self, board_game, player):
#         self.board_game = board_game
#         self.player = player
#
#     def build_supply_center(self):
#         self.player.location.has_supply_center = True
#         self.board_game.supply_centers += int(round(1, 0))
#
#     def make_supplies(self):
#         self.board_game.stockpile -= int(round(1, 0))
#         self.player.supplies_on_card += int(round(1, 0))
#
#     def deliver_supplies(self, number):
#         self.player.location.supplies += int(round(number, 0))
#         self.player.supplies_on_card -= int(round(number, 0))
#
#     def move(self, new_location):
#         self.player.location = new_location
