import random
from battleship_constants_and_utils import (
    EMPTY, BOARD_SIZE, print_boards, clear_screen,
    X_AXIS, Y_AXIS, replace_coordinate, get_coordinate,
    print_board, VERTICAL_SHIP, HORIZONTAL_SHIP, MISS,
    HIT, SUNK, SHIP_INFO
    )

class Player():
    """A Class to represent each player"""
    def __init__(self, player):
        """player argument is the players number, eg (player) 1"""
        self.player = player
        self.player_board = Board()
        self.get_name()
        self.guesses = []
        

    def get_name(self):
        name = input(" Player {}, please enter your name:\n\n ".format(
            self.player)).title()
        if name:
            self.name = name
            print("\nWelcome {}\n".format(self.name))
            clear_screen()
        else:
            clear_screen()
            print(" That is not your name, it is nothing.")
            self.get_name()
        

    def make_guess(self, guess_board, player, opponent, copies):
        """Takes a guess as input from the player and checks whether
           or not there is a ship there"""

        guess = input(
            "\n {}, its your turn to guess: \n\n ".format(self.name)
            ).strip().lower()
        if guess not in self.player_board.all_coords:
            clear_screen()
            print(" That is not a valid coordinate, " +
                  "please enter a coordinate that is on the board " +
                  "e.g. {}".format(random.choice(
                      self.player_board.all_coords)))
            if self.player == 1:
                print_boards([self.player_board.board, opponent.player_board.board])
            else:
                print_boards([opponent.player_board.board, self.player_board.board]) 
            self.make_guess(guess_board, player, opponent, copies)
            
        elif guess in self.guesses:
            clear_screen()   
            print(" You have already guessed that coordinate, " +
                  "pick a different one.")
            if self.player == 1:
                print_boards([self.player_board.board, opponent.player_board.board])
            else:
                print_boards([opponent.player_board.board, self.player_board.board]) 
            self.make_guess(guess_board, player, opponent, copies)
            
        else:
            self.guesses.append(guess)
            if get_coordinate(guess, opponent.player_board.board) in str(
                VERTICAL_SHIP + HORIZONTAL_SHIP):
                opponent.player_board.hit_ship(player, opponent, guess, copies)
                self.make_guess(guess_board, player, opponent, copies)
            elif get_coordinate(guess, opponent.player_board.board) == EMPTY:
                replace_coordinate(
                    guess, opponent.player_board.board, MISS)
                clear_screen()    
                print(" {} has missed.".format(self.name))
        
        
        
        

class Board():
    
    def __init__(self):
        """Generates an empty board and all possible coordinates
           there is another list for all the ships the player
           will plot"""
        board = [] # The game board is stored in this list
        all_coords = []
        self.all_ships = []
        self.all_ship_names = {}
        
        for ship in SHIP_INFO:
            self.all_ship_names[
                ship[0]] = []    
        
        for i in range(BOARD_SIZE):
            board.append(EMPTY * BOARD_SIZE)
        self.board = board

        for i in range(BOARD_SIZE):
            for a in X_AXIS:
                all_coords.append('{}{}'.format(a, i+1))
        self.all_coords = all_coords


    def plot_ship(self, ship_coords, ship_name, rotation):
        """Takes valid ship coordinates from validate_coordiante
           and uses them to plot a ship on the board"""
        self.all_ship_names[ship_name].append(ship_coords)
        if rotation == 1:
            replacement = HORIZONTAL_SHIP
        elif rotation == 2:
            replacement = VERTICAL_SHIP

        print(ship_coords)
        for coord in ship_coords:
            self.board = replace_coordinate(
                coord, self.board, replacement
                )
        self.all_ships.append(ship_coords)
        

    def check_sunk(self, player, opponent, copies):
        """After a ship has been hit, it is checked to
           see if any ships have been sunk. If so, they
           will be marked as sunk"""
        for ship in self.all_ships:
            hit = 0
            for coord in ship:
                if get_coordinate(
                    coord, self.board) == HIT:
                    hit += 1
            if hit == len(ship):
                for coord in ship:
                      replace_coordinate(
                          coord, self.board, SUNK)
                          
                for key, value in self.all_ship_names.items():
                    if value[0] == ship:
                        ship_name = key
                        clear_screen()
                        print(" {} has destroyed a {}! {} gets another turn.".format(
                            player.name, ship_name, player.name))
                self.all_ships.remove(ship)
        if not self.all_ships:
            self.game_over(player, opponent, copies)
                    
            
            

    def hit_ship(self, player, opponent, hit_coord, copies):
        """After a ship is hit, it is marked on the grid
           as hit"""
        clear_screen()
        self.board = replace_coordinate(
            hit_coord, self.board, HIT)
        print(" {} has hit an enemy ship! {} gets another turn.".format(
            player.name, player.name))
        self.check_sunk(player, opponent, copies)
        if player.player == 1:
            print_boards([player.player_board.board, opponent.player_board.board])
        else:
            print_boards([opponent.player_board.board, player.player_board.board]) 
            

    def game_over(self, player, opponent, copies):
        """Once a player has destroyed all the other's ships,
           the game will finish and a message will be displayed"""
        clear_screen()
        print_boards(copies, True)
        print("\n {} wins! All of {}'s ships have been destroyed!".format(
            player.name, opponent.name))
        print(" Above shows where you both originally placed your ships.")
        input(" Thanks for playing! Press ENTER to exit.")
        clear_screen()
        exit()
                      
        
        

class Ship():

    def __init__(self, size, name):
        """Generates a ship with size and name"""
        self.size = size
        self.name = name
        self.alive = True

        
    def ask_coordinate(self, player):
        """Takes a coordinate as input from the user"""
        print_board(player.player_board.board)

        coordinate = input(
            "\n {}, where would you to place your {}(size: {})? \n ".format(
                player.name, self.name, self.size) +
            " Enter a coordinate (e.g. {}): \n\n ".format(
                random.choice(player.player_board.all_coords)
                )).strip().lower()

        self.validate_coordinate(coordinate, player)
        
        
    def validate_coordinate(self, coordinate, player):
        """Checks that the coordinate taken from function
           ask_coordinates is valid"""
        
        if not coordinate in player.player_board.all_coords:
            clear_screen()
            print(" That is not a valid coordinate, " +
                  "please enter a coordinate that is on the board " +
                  "e.g. {}".format(random.choice(
                      player.player_board.all_coords)))
            self.ask_coordinate(player)
        elif get_coordinate(
            coordinate, player.player_board.board
            ) in str(VERTICAL_SHIP + HORIZONTAL_SHIP):
            clear_screen()
            print(" You already have a ship there")
            self.ask_coordinate(player)
        else:
            self.validate_rotation(coordinate, player)


    def validate_rotation(self, coordinate, player):
        """Checks that the ship is able to fit onto the
           board with the rotation selected by the player"""
        
        rotation = input("\n Enter the number of your choice of rotation." +
                         "\n 1. Horizontal\n 2. Vertical.\n\n ").strip()
        if rotation:
            if rotation not in '12':
                print(" Please enter either 1(Horizontal) or 2(Vertical).")
                self.validate_rotation(coordinate, player)
            elif rotation == '1':
                index = X_AXIS.index(coordinate[0])
                spaces = len(
                    player.player_board.board[int(coordinate[1])-1][index:])
                if spaces >= self.size:
                    self.initiate_ship_plot(coordinate, 1, player)
                else:

                    self.unable_to_fit(spaces)
                    self.ask_coordinate(player)
            elif rotation == '2':
                spaces = BOARD_SIZE - int(coordinate[1]) + 1
                if spaces >= self.size:
                    self.initiate_ship_plot(coordinate, 2, player)
                else:
                    self.unable_to_fit(spaces)
                    self.ask_coordinate(player)
        else:
            print(" Please enter either 1(Horizontal) or 2(Vertical)")
            self.validate_rotation(coordinate, player)
                

    def unable_to_fit(self, spaces):
        """Prints a message showing what was wrong with the choice,
           put into a seperate procedure as it is used more than
           once"""
        clear_screen()
        print(" Your ship is not able to fit there as it " +
              "takes up {} spaces and there are ".format(self.size) +
              "only {} there.\n".format(spaces) +
              " Please pick a different location.")


    def initiate_ship_plot(self, coordinate, rotation, player):
        """Prepares a list of coordinates that will be plotted
           onto the ship, passes these coordinates into
           plot_a_ship"""

        ship_coords = [coordinate]
        if rotation == 1:
            x_index = X_AXIS.index(coordinate[0])
            for i in range(self.size - 1):
                ship_coords.append(
                    X_AXIS[x_index + 1] +
                    coordinate[1:]
                    )
                x_index += 1
        elif rotation == 2:
            y_index = Y_AXIS.index(coordinate[1])
            for i in range(self.size - 1):
                ship_coords.append(
                    coordinate[0] +
                    Y_AXIS[y_index + 1]
                    )
                y_index += 1

        self.check_collision(ship_coords, player, rotation)
        


    def check_collision(self, ship_coords, player, rotation):
        """loops through ship_coords and checks if the
           coordinates collide with any other ships"""
        coords_good = True
        for coord in ship_coords:
            if get_coordinate(
                coord, player.player_board.board
                ) in str(VERTICAL_SHIP+HORIZONTAL_SHIP):
                clear_screen()
                print(" You cannot place your ship there as it " +
                      "collides with another ship")
                coords_good = False
                self.ask_coordinate(player)

        if coords_good:
            player.player_board.plot_ship(ship_coords, self.name, rotation)

        
        
            
            
        
        


        

