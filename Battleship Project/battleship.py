from battleship_classes import Player, Board, Ship
from copy import deepcopy
from battleship_constants_and_utils import(
    SHIP_INFO, print_boards, HORIZONTAL_SHIP, VERTICAL_SHIP,
    clear_screen
    )

def introduction():
    clear_screen()
    print("Hello, welcome to Battleships. This is a game where 2 " +
          "players \ntake turns plotting ships on a grid and guessing " +
          "where \nthey are.\n\nNOTE:\n\nWhen plotting your ships, " +
          "if your ship is vertical, imagine \nwhere you want your ship and" +
          "enter the TOP most coordinate." +
          "If it is \nhorizontal, enter the LEFT most coordinate.\n\n" +
          "Remember, make sure the other person isn't looking " +
          "at \nyou plot your ships because that is cheating.\n\n" +
          "Once you have plotted your ships, when guessing, these are " +
          "the \ndifferent symbols that will be displayed on your board:\n\n" +
          " . (when you miss)\n * (when you hit an an enemy ship)\n " +
          "# when you sink an enemy ship")
    
    input("\n\nHIT ENTER TO START ")

    
def print_turn(player_1, player_2):
    print(" It is {}'s turn to plot their ships. ".format(
        player_1.name) +
          "{}, look away.".format(player_2.name))
    input(" {}, hit enter when you are ready.".format(player_1.name))
    clear_screen()
    

def get_opponent(player, players):
    if player == players[0]:
        return players[1]
    elif player == players[1]:
        return players[0]

    
def main():
    introduction()
    clear_screen()
    player_1 = Player(1)
    player_2 = Player(2)
    players = [player_1, player_2]
    clear_screen()
    all_ships = [[],[]]

    for i in range(2):
        if players[i] == player_1:
            print_turn(player_1, player_2)
        else:
            print_turn(player_2, player_1)
        
            
        for ship in SHIP_INFO:
            all_ships[i].append(
                Ship(ship[1], ship[0]))

        for ship in all_ships[i]:
            ship.ask_coordinate(players[i])
            clear_screen()
            
    guess_board_1 = player_1.player_board
    guess_board_2 = player_2.player_board

    player_1_board_copy = deepcopy(players[0])
    player_2_board_copy = deepcopy(players[1])
    
    copies = [
        player_1_board_copy.player_board.board,
        player_2_board_copy.player_board.board,
        ]

    player_1.copy = copies[0]
    player_2.copy = copies[1]

    
    while True:
        for i in range(2):
            player_1.generate_display_board()
            player_2.generate_display_board()
            
            guess_boards = [
                guess_board_1.board,
                guess_board_2.board,
                ]

            display_boards = [
                players[0].display_board,
                players[1].display_board
                ]
            
            print(" Look away {}. ".format(
                get_opponent(players[i], players).name))
            input(" {}, hit ENTER to start your turn. ".format(
                players[i].name))

            clear_screen()
            

            if i == 0:
                print_boards([display_boards[0],guess_boards[1]], 1)
            else:
                print_boards([guess_boards[0],display_boards[1]], 0)
            
            players[i].make_guess(
                guess_boards[i],
                players[i],
                get_opponent(players[i], players),
                copies)
            

main()
