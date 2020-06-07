import random


class Card:
    """ An object describing a card

    Args:
        value (int): Value of the card
        color (str): The color(suit) of the card
    """
    def __init__(self, name, value, color):
        self.name = name
        self.value = value
        self.color = color

    def __str__(self):
        return '{} of {}'.format(self.name, self.color)

    __repr__ = __str__

    def card_value(self):
        pass


class Shoe:

    def __init__(self, cards):
        self.cards = cards
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_single_card(self):
        dealt_card = [self.cards.pop(0)]
        return dealt_card


class Player:

    def __init__(self, name):
        self.name = name
        self.money = 100
        self.hand = Hand

    def __str__(self):
        return 'Name: {}\tMoney: {}'.format(self.name, self.money)


class Dealer:

    def __init__(self):
        self.name = 'Dealer'
        self.hand = Hand

    def __str__(self):
        return 'Dealer: Place you bets!'


class Hand:

    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self._cards = cards

    def add_card(self, shoe):
        """ Adds card to the hand from the selected.
        shoe (Shoe): The show from wich the card comes from.

        """
        self._cards.extend(shoe.deal_single_card())

    @property
    def score(self):
        score = 0
        ace_in_hand = False
        for card in self._cards:
            if card.value == 1 and not ace_in_hand:
                score += card.value + 10
                ace_in_hand = True
                if score > 21 and ace_in_hand:
                    score -= 10
            else:
                score += card.value

        return score

    def __str__(self):
        return str(self._cards)


def build_deck():

    deck = []
    suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
    face_card = ['Jack', 'Queen', 'King']
    for color in suits:
        new_card = Card('Ace', 1, color)
        deck.append(new_card)
        for value in range(2, 11):
            name = str(value)
            new_card = Card(name, value, color)
            deck.append(new_card)
        for card in face_card:
            new_card = Card(card, 10, color)
            deck.append(new_card)

    return deck


def first_deal(shoe):

    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(shoe)
    dealer_hand.add_card(shoe)
    player_hand.add_card(shoe)

    return player_hand, dealer_hand


def player_turn(name, hand, shoe):

    player_bust = False
    while player_bust is False:
        vocabulary = {'Hit': 'h', 'hit': 'h', 'H': 'h', 'h': 'h',
                      'Stand': 's', 'stand': 's', 'S': 's', 's': 's'}
        action = input('Hit or Stand: ')
        if action in vocabulary:
            player_action = vocabulary[action]
            if player_action == 'h':
                print(name + ' Hits')
                hand.add_card(shoe)
                if hand.score > 21:
                    print(name + ' busts')
                    player_bust = True
                    return player_bust
                elif hand.score == 21:
                    break
            else:
                print(name + ' Stands')
                break
        else:
            print('Not a valid action')


def dealer_turn(dealer_hand, player_score, player_name, shoe):

    dealer_hand.add_card(shoe)
    dealer_score = dealer_hand.score
    if player_score <= 21:
        while dealer_score < 17:
            dealer_hand.add_card(shoe)
            dealer_score = dealer_hand.score
            print('Dealer takes a card')
        if dealer_score > 21:
            print('Dealer busts\n' + player_name + ' wins!')
        elif 21 >= dealer_score > player_score:
            print('Dealer wins!')
        elif dealer_score == player_score:
            print('Push')
        else:
            print(player_name + ' wins')
    else:
        print('Dealer wins')


def game_start():

    deck = build_deck()
    shoe = Shoe(deck)
    shoe.shuffle()
    dealer = Dealer()
    player = Player(input('Enter your name: '))
    player.hand, dealer.hand = first_deal(shoe)
    print(player)
    print(dealer)
    print('-'*40)
    player_turn(player.name, player.hand, shoe)
    dealer_turn(dealer.hand, player.hand.score, player.name, shoe)
    pass


if __name__ == '__main__':
    game_start()

