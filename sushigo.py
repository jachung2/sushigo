#Two player SushiGo, with minimax computer player.
#Brendan Cordy, 2015

from random import shuffle
from copy import deepcopy
from itertools import combinations

class Deck(object):
    def __init__(self):
        card_names = ['Tempura', 'Sashimi', 'Dumpling', 'DoubleMaki', 'TripleMaki', 'SingleMaki', 'SalmonNigiri', 'SquidNigiri', 'EggNigiri', 'Wasabi', 'Chopsticks']
        counts = [14, 14, 14, 12, 8, 6, 10, 5, 5, 6, 4]

        self.cards = []
        for i in range(len(counts)):
            for j in range(counts[i]):
                self.cards.append(card_names[i])

        shuffle(self.cards)

    def deal(self, n):
        return self.cards[0:n], self.cards[n:2*n]

class GameState(object):
    def __init__(self):
        D = Deck()
        self.p1_hand, self.p2_hand = D.deal(6)
        self.p1_table, self.p2_table = [], []

    def swap(self):
        self.p1_hand, self.p2_hand = self.p2_hand, self.p1_hand

    def finished(self):
        return self.p1_hand == [] and self.p2_hand == []

    def get_hands(self):
        return self.p1_hand, self.p2_hand

    def add_to_p1_table(self, card):
        #Check for wasabi on table.
        if self.p1_table.count('Wasabi') > 0 and 'Nigiri' in card:
            self.p1_table.remove('Wasabi')
            self.p1_table.append(card + 'Wasabi')
        else:
            self.p1_table.append(card)

    def add_to_p2_table(self, card):
        #Check for wasabi on table.
        if self.p2_table.count('Wasabi') > 0 and 'Nigiri' in card:
            self.p2_table.remove('Wasabi')
            self.p2_table.append(card + 'Wasabi')
        else:
            self.p2_table.append(card)

    def get_tables(self):
        return self.p1_table, self.p2_table

    #Have p1 and p2 play their cards. A move is given by a two element list. The list [0,c]
    #represents playing the card c, while [1,[c1,c2]] denotes a chopstick swap for cards c1
    #and c2 (in that order).
    def play(self, p1_move, p2_move):
        p1_valid, p2_valid = False, False
        p1_chop, p2_chop = False, False

        #If p1's move is not a swap and p1 has the card being played in hand, all is good.
        if p1_move[0] == 0 and self.p1_hand.count(p1_move[1]) > 0:
            p1_valid = True
        #If p1's move is a swap and p1 has the cards being swapped for in hand, all is good.
        elif p1_move[0] == 1 and self.p1_table.count('Chopsticks') > 0 and self.p1_hand.count(p1_move[1][0]) > 0 and self.p1_hand.count(p1_move[1][1]) > 0:
            p1_valid, p1_chop = True, True

        #If p2's move is not a swap and p2 has the card being played in hand, all is good.
        if p2_move[0] == 0 and self.p2_hand.count(p2_move[1]) > 0:
            p2_valid = True
        #If p2's move is a swap and p2 has the cards being swapped for in hand, all is good.
        elif p2_move[0] == 1 and self.p2_table.count('Chopsticks') > 0 and self.p2_hand.count(p2_move[1][0]) > 0 and self.p2_hand.count(p2_move[1][1]) > 0:
            p2_valid, p2_chop = True, True

        if p1_valid and p2_valid:
            if p1_chop:
                self.p1_hand.remove(p1_move[1][0])
                self.add_to_p1_table(p1_move[1][0])

                self.p1_hand.remove(p1_move[1][1])
                self.add_to_p1_table(p1_move[1][1])

                self.p1_table.remove('Chopsticks')
                self.p1_hand.append('Chopsticks')

            else:
                self.p1_hand.remove(p1_move[1])
                self.add_to_p1_table(p1_move[1])

            if p2_chop:
                self.p2_hand.remove(p2_move[1][0])
                self.add_to_p2_table(p2_move[1][0])

                self.p2_hand.remove(p2_move[1][1])
                self.add_to_p2_table(p2_move[1][1])

                self.p2_table.remove('Chopsticks')
                self.p2_hand.append('Chopsticks')

            else:
                self.p2_hand.remove(p2_move[1])
                self.add_to_p2_table(p2_move[1])

            self.swap()

        else:
            print 'Invalid play'

    def eval_tables(self):
        p1_total = 0
        p1_maki = 0

        #Integer division!
        p1_total += 5 * (self.p1_table.count('Tempura') / 2)
        p1_total += 10 * (self.p1_table.count('Sashimi') / 3)
        p1_total += (self.p1_table.count('Dumpling') * (self.p1_table.count('Dumpling') + 1)) / 2
        p1_maki += self.p1_table.count('SingleMaki') + 2* self.p1_table.count('DoubleMaki') + 3 * self.p1_table.count('TripleMaki')
        p1_total += self.p1_table.count('EggNigiri')
        p1_total += 2 * self.p1_table.count('SalmonNigiri')
        p1_total += 3 * self.p1_table.count('SquidNigiri')
        p1_total += 3 * self.p1_table.count('EggNigiriWasabi')
        p1_total += 6 * self.p1_table.count('SalmonNigiriWasabi')
        p1_total += 9 * self.p1_table.count('SquidNigiriWasabi')

        p2_total = 0
        p2_maki = 0

        #Integer division!
        p2_total += 5 * (self.p2_table.count('Tempura') / 2)
        p2_total += 10 * (self.p2_table.count('Sashimi') / 3)
        p2_total += (self.p2_table.count('Dumpling') * (self.p2_table.count('Dumpling') + 1)) / 2
        p2_maki += self.p2_table.count('SingleMaki') + 2 * self.p2_table.count('DoubleMaki') + 3 * self.p2_table.count('TripleMaki')
        p2_total += self.p2_table.count('EggNigiri')
        p2_total += 2 * self.p2_table.count('SalmonNigiri')
        p2_total += 3 * self.p2_table.count('SquidNigiri')
        p2_total += 3 * self.p2_table.count('EggNigiriWasabi')
        p2_total += 6 * self.p2_table.count('SalmonNigiriWasabi')
        p2_total += 9 * self.p2_table.count('SquidNigiriWasabi')

        #Calculate maki points.
        if p1_maki > p2_maki and p2_maki > 0:
            p1_total += 6
            p2_total += 3

        if p2_maki > p1_maki and p1_maki > 0:
            p2_total += 6
            p1_total += 3

        if p2_maki == p1_maki and p1_maki > 0:
            p2_total += 3
            p1_total += 3

        if p1_maki > 0 and p2_maki == 0:
            p1_total += 6

        if p2_maki > 0 and p1_maki == 0:
            p2_total += 6

        return p1_total - p2_total

def main():
    G = GameState()
    game_mode = 0

    print "\nSushiGo!\n"
    while not(game_mode in ['1','2']):
        game_mode = raw_input("1. Human vs Human, 2. Human vs Robot: ")

    while not(G.finished()):
        p1_hand, p2_hand = G.get_hands()
        p1_table, p2_table = G.get_tables()

        print '\n'
        print "p1's hand: " + str(p1_hand) + '\n'
        print "p1's table: " + str(p1_table) + '\n'
        print "p2's hand: " + str(p2_hand) + '\n'
        print "p2's table: " + str(p2_table) + '\n'

        #Human vs Human
        if game_mode == '1':
            p1_input = raw_input("p1's play: ")

            #Parse human input, checking for a swap if it occurred.
            if p1_input[:9] == 'Swap for ':
                #[1,[c1,c2]] denotes a chopstick swap for cards c1 and c2 (in that order).
                p1_select = [1, [p1_input[(p1_input.index('for ') + 4):p1_input.index(' and')], p1_input[p1_input.index('and ') + 4:]]]
            else:
                #[0,c] denotes playing the card c.
                p1_select = [0, p1_input]

            p2_input = raw_input("p2's play: ")

            #Parse human input, checking for a swap if it occurred.
            if p2_input[:9] == 'Swap for ':
                #[1,[c1,c2]] denotes a chopstick swap for cards c1 and c2 (in that order).
                p2_select = [1, [p2_input[(p2_input.index('for ') + 4):p2_input.index(' and')], p2_input[p2_input.index('and ') + 4:]]]
            else:
                #[0,c] denotes playing the card c.
                p2_select = [0, p2_input]

        #Human vs Robot
        elif game_mode == '2':
            p1_input = raw_input("p1's play: ")

            #Parse human input, checking for a swap if it occurred.
            if p1_input[:9] == 'Swap for ':
                #[1,[c1,c2]] denotes a chopstick swap for cards c1 and c2 (in that order).
                p1_select = [1, [p1_input[(p1_input.index('for ') + 4):p1_input.index(' and')], p1_input[p1_input.index('and ') + 4:]]]
            else:
                #[0,c] denotes playing the card c.
                p1_select = [0, p1_input]

            #Find optimal robot move.
            p2_select = find_p2_best_move(deepcopy(G), -1000, 1000)[0]

            #Pretty printing for robot move.
            if p2_select[0] == 0:
                p2_play = p2_select[1]
            elif p2_select[0] == 1:
                p2_play = 'Swap for ' + p2_select[1][0] + ' and ' +  p2_select[1][1]

            print "p2's play: " + p2_play

        G.play(p1_select,p2_select)

    p1_table, p2_table = G.get_tables()
    score_diff = G.eval_tables()

    print '\n'
    print "p1's table: " + str(p1_table) + '\n'
    print "p2's table: " + str(p2_table) + '\n'

    if score_diff > 0:
        print "p1 wins by " + str(score_diff)
    elif score_diff < 0:
        print "p2 wins by " + str(-score_diff)
    else:
        print "p1 and p2 rejoice in their shared victory!"

#Minimax for p2.
def find_p2_best_move(G, alpha, beta):
    p1_hand, p2_hand = G.get_hands()
    p1_table, p2_table = G.get_tables()

    #If there is only one card to play, play it.
    if len(p2_hand) == 1:
        H = deepcopy(G)
        H.play([0,p1_hand[0]],[0,p2_hand[0]])
        return [0,p2_hand[0]], H.eval_tables()

    #Collect all possible moves for p1. Moves are cards in hand or chopstick swaps.
    p1_moves = [[0,c] for c in set(p1_hand)]
    if 'Chopsticks' in p1_table:
        p1_swaps_set = set(combinations(p1_hand,2))
        p1_swaps = [[1,list(s)] for s in p1_swaps_set]

        #Allow chopstick swaps for wasabi and nigiri in either order, so that
        #wasabi can either be applied immediately or saved for later.
        wasabi_swap_reorders = []
        for s in p1_swaps:
            if 'Wasabi' in s[1] and ('Nigiri' in s[1][0] or 'Nigiri' in s[1][1]):
                 wasabi_swap_reorders.append([1,[s[1][1],s[1][0]]])

        p1_swaps += wasabi_swap_reorders
        p1_moves += p1_swaps

    #Collect all possible moves for p2. Moves are cards in hand or chopstick swaps.
    p2_moves = [[0,c] for c in set(p2_hand)]
    if 'Chopsticks' in p2_table:
        p2_swaps_set = set(combinations(p2_hand,2))
        p2_swaps = [[1,list(s)] for s in p2_swaps_set]

        #Allow chopstick swaps for wasabi and nigiri in either order, so that
        #wasabi can either be applied immediately or saved for later.
        wasabi_swap_reorders = []
        for s in p2_swaps:
            if 'Wasabi' in s[1] and ('Nigiri' in s[1][0] or 'Nigiri' in s[1][1]):
                 wasabi_swap_reorders.append([1,[s[1][1],s[1][0]]])

        p2_swaps += wasabi_swap_reorders
        p2_moves += p2_swaps

    #Minimax it up.
    ev_p2 = 1000
    for p2_move in p2_moves:

        ev_p1 = -1000
        for p1_move in p1_moves:
            H = deepcopy(G)
            H.play(p1_move, p2_move)
            ev_p1 = max(ev_p1, find_p2_best_move(H, alpha, beta)[1])

        if ev_p1 < ev_p2:
            p2_bestmv = p2_move
        ev_p2 = min(ev_p1, ev_p2)

    return p2_bestmv, ev_p2

if __name__ == '__main__':
    main()
