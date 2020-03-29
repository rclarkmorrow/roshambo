#!/usr/bin/env python3

import random
# Defines available moves in game
moves = ['rock', 'paper', 'scissors']
# Defines inputs to quit game, play new game and end game
quit_game = ['quit', 'q']
new_game = ['yes', 'y']
end_game = ['no', 'n']

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

"""The Player class is the parent class for all of the Players
in this game"""


class Player():
    #  Initializes the Player class with values for subclasses so that
    #  initial moves are random in call cases"""
    def __init__(self):
        self.my_move = random.choice(moves)
        self.their_move = random.choice(moves)

    # The Player class remembers its previous move, and its opponent's
    # previous move.
    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move


class RandomPlayer(Player):
    # The RandomPlayer class always makes random moves.
    def move(self):
        return random.choice(moves)


class ReflectPlayer(Player):
    # The ReflectPlayer class makes a random move on round 1 but in subsequent
    # rounds copies the move its oppoment made in the previous round.
    def move(self):
        return self.their_move


class CyclePlayer(Player):
    # The CyclePlayer class makes a random move on round 1 but in subsequent
    # rounds cycles to the next move. It resets to the first available move
    # after it playst the last available move.
    def move(self):
        for move in range(len(moves)):
            if self.my_move == moves[move]:
                if move + 1 >= len(moves):
                    return moves[0]
                else:
                    return moves[move + 1]


class HumanPlayer(Player):
    # The HumanPlayer class accepts user input for each round. If user enters
    # invalid input, the prompts loops. If user enters quit command the game
    # exits after determing who won and displaying cumulative score.
    def move(self):
        input_text = ""
        for move in range(len(moves)):
            if move < len(moves)-1:
                input_text = input_text + (f"{moves[move]}, ")
            else:
                input_text = input_text + (f"{moves[move]}")

        while True:
            player_move = input((f"{input_text}? > "))
            if player_move.lower() in moves:
                return player_move
            elif player_move.lower() in quit_game:
                return "quit"


def beats(one, two):
    # Compares moves by players to return True if move one beats move two
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    # Initialises players and player scores
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.score_p1 = 0
        self.score_p2 = 0

        self.move1 = moves[0]

    # Determines results of the game and returns a string to print.
    def get_rounds(self):
        while True:
            rounds = input("How many rounds of roshambo would you like" +
                           " to play? > ")
            if rounds.isdigit():
                return int(rounds)
            elif rounds.lower() in quit_game:
                exit("\nGoobye!")

    def game_winner(self, score_p1, score_p2):
        if score_p1 > score_p2:
            return(f"\n*** YOU WIN THE GAME ***")
        elif score_p1 < score_p2:
            return(f"\n*** YOU LOSE THE GAME ***")
        else:
            return(f"\n*** THE GAME ENDS IN A TIE ***")

    # Asks player if they want to play another game. Condition exit if player
    # has previously entered the command to quit the game.
    def play_again(self):
        print("\nGame over!")
        if self.move1 not in moves:
            exit("\nGoodbye!")
        else:
            while True:
                new_game_input = input("\nWould you like to play again? > ")
                if new_game_input.lower() in new_game:
                    game = Game(HumanPlayer(), random.choice((ReflectPlayer(),
                                RandomPlayer(), CyclePlayer())))
                    game.play_game()
                elif new_game_input.lower() in end_game:
                    exit("\nGoodbye!")

    # Determines results of a round and returns a string to print.
    def round_winner(self, move1, move2):
        if beats(move1, move2):
            self.score_p1 += 1
            return("*** YOU WIN ***")
        elif beats(move2, move1):
            self.score_p2 += 1
            return("*** YOU LOSE ***")
        else:
            return("*** TIE ****")

    # Receives round results and returns a string to print.
    def print_round(self, move1, move2, winner, score_p1, score_p2):
        if self.move1 in moves:
            return (f"\nYou played: {move1}\nOpponened played: {move2}\n\n" +
                    f"{winner}\nScore -- You: {score_p1} Opponent: {score_p2}")
        else:
            return (f"\nScore -- You: {score_p1} Opponent: {score_p2}")

    # Fuction governs roud mechanics. Each player moves. Each player remembers
    # moves.Prints round results. Also records player move to validate game
    # exit if game exit commaned entered.
    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        self.move1 = move1

        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

        winner = (self.round_winner(move1, move2))

        print(self.print_round(move1, move2, winner, self.score_p1,
                               self.score_p2))

    # Governs game mechanics. Determines lenght of game. Runs rounds.
    # Prints game results.
    def play_game(self):
        print("\nWelcome to Rick's Roshambo. Enter 'quit' at any time to" +
              " exit the game.\n")
        rounds = (self.get_rounds())
        print("Game start!")
        for round in range(rounds):
            # Conditional breaks loop if player enters game exit command.
            if self.move1 not in moves:
                break
            else:
                print(f"\nRound {round +1}:")
            self.play_round()

        print(self.game_winner(self.score_p1, self.score_p2))
        self.play_again()


if __name__ == '__main__':
    # Launches game. Game is played between a human player and a randomly
    # selected computer opponent.
    game = Game(HumanPlayer(), random.choice((ReflectPlayer(), RandomPlayer(),
                CyclePlayer())))
    game.play_game()
