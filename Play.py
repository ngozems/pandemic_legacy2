import random
from PandamicBoardGame import bladiblpe


class GameState:
    def __init__(self, board):
        self.BoardState = board
        self.GameEnd = False

    def check_game_end(self):
        if self.BoardState.incidents == 8:
            self.GameEnd = True

        if len(self.BoardState.player_deck) == 0:
            self.GameEnd = True

        if self.BoardState.supply_centers == 3:
            self.GameEnd = True


class Board:
    def __init__(self):
        self.NewYork = Location("New York", "city")
        self.Washington = Location("Washington", "city")
        self.Jacksonville = Location("Jacksonville", "city")
        self.Sao_Paulo = Location("Sao_Paulo", "city")
        self.London = Location("London", "city")
        self.Cairo = Location("Cairo", "city")
        self.Lagos = Location("Lagos", "city")
        self.Tripoli = Location("Tripoli", "city")
        self.Istanbul = Location("Istanbul", "city")
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

        self.stockpile = 0
        self.incidents = 0

        self.infection_grade = 2
        self.infection_grade_counter = 0
        self.supply_centers = 0

        self.player_deck = ""
        self.infection_deck = self.shuffle_infection_deck()

    def create_deck(self, size):
        deck = [self.NewYork, self.Washington, self.Sao_Paulo, self.Lagos,
                self.London,  self.Cairo, self.Tripoli, self.Istanbul]
        city_list = [self.NewYork, self.Washington, self.Sao_Paulo, self.Lagos,
                     self.London,  self.Cairo, self.Tripoli, self.Istanbul]
        counter = 1
        while counter <= size:
            deck.extend(city_list)
            print(len(city_list))
            counter += 1

        return deck

    def shuffle_infection_deck(self):
        infection_deck = self.create_deck(3)
        random.shuffle(infection_deck)
        return infection_deck

    def create_player_deck(self):
        player_deck = self.create_deck(5)
        epidemics = ["epidemic", "epidemic", "epidemic", "epidemic", "epidemic"]
        player_deck.extend(epidemics)
        return player_deck

    def move_infection_grade_token(self):
        self.infection_grade_counter += 1
        if self.infection_grade_counter % 2 == 0:
            self.infection_grade += 1

    def remove_from_stockpile(self):
        self.stockpile -= 1

    def add_to_stockpile(self):
        self.stockpile += 1

    def increase_incidents(self):
        self.incidents += 1


class Location():
    def __init__(self, name, location_type):
        self.name = name
        self.paths = []
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
    def __init__(self, role, location, player_number, card_list):
        self.role = role
        self.location = location
        self.abilities = ""
        self.cards = card_list
        self.supplies_on_card = 0
        self.player_number = player_number


class Actions:
    def __init__(self, board_game, player):
        self.board_game = board_game
        self.player = player

    # def make_step(self):
    #     ## do stuff

    def build_supply_center(self):
        self.player.location.has_supply_center = True
        self.board_game.supply_centers += 1
    #
    # def add_supplies_to_card(self):
    #     self.player.supplies_on_cards += 1
    #
    # def remove_from_stockpile(self):
    #     self.state.stockpile -= 1
    #
    # def add_to_stockpile(self):
    #     self.state.stockpile += 1
    #
    # def add_incident(self):
    #     self.state.incidents += 1
    #     if self.state.incidents == 8:
    #         return "Lose"
    #
    # def change_infection_grade(self):
    #     self.state.infection_grade_loc += 1
    #     self.state.infection_grade = self.infection_grade_mapping[self.infection_grade_loc]
    #
    # def draw_infection_card(self):
    #     total_inf_cards_in_deck = len(self.state.infection_deck)
    #     draw = self.state.infection_deck[total_inf_cards_in_deck]
    #     self.state.infection_deck = self.state.infection_deck[0: total_inf_cards_in_deck - 1]

        # in programmeren dat er supplies op de steden komen

        self.state.drawed_infection_deck.append(draw)

    def draw_player_card(self):
        total_player_cards_in_deck = len(self.state.player_deck)
        # in programmeren dat je verliest als je niks meer kan pakken

        draw = self.state.player_deck[total_player_cards_in_deck]
        self.state.player_deck = self.state.player_deck[0: total_player_cards_in_deck - 1]
