from random import shuffle


class CardData:
    """Static class for the card data"""

    def __init__(self):
        # noinspection SpellCheckingInspection
        raise RuntimeError('Az osztaly statikus, nem peldanyosithato')

    # noinspection SpellCheckingInspection
    colors = ('Kor', 'Karo', 'Treff', 'Pikk')
    # noinspection SpellCheckingInspection
    ranks = ('Ketto', 'Harom', 'Negy', 'Ot', 'Hat', 'Het', 'Nyolc', 'Kilenc', 'Tiz', 'Bubi', 'Dama', 'Kiraly', 'Asz')

    @staticmethod
    def get_value(what):
        values = {'Ketto': 2, 'Harom': 3, 'Negy': 4, 'Ot': 5, 'Hat': 6,
                  'Het': 7, 'Nyolc': 8, 'Kilenc': 9, 'Tiz': 10,
                  'Bubi': 10, 'Dama': 10, 'Kiraly': 10, 'Asz': 11}
        if not what in values.keys():
            raise ValueError('A megadott ertek nem talalhato')
        return values[what]

    is_playing = True


class Card:

    def __init__(self, color, rank):
        self.color = color
        self.rank = rank

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        if len(color) >= 3:
            self.__color = color
        else:
            raise ValueError('Az ertek nem egy kartyaszin')

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, rank):
        if len(rank) >= 2:
            self.__rank = rank
        else:
            raise ValueError('Az ertek minimum 2 karakteres legyen')

    def __str__(self):
        return self.rank + ' - ' + self.color


class Deck(list):

    def __init__(self):
        super().__init__()
        self.cards_deck = []
        for color in CardData.colors:
            for rank in CardData.ranks:
                self.append(Card(color, rank))

    def __str__(self):
        tmp = ''
        for card in self:
            tmp += card.__str__() + '\n'
        return tmp

    def mix(self):
        shuffle(self)

    def div(self):
        return self.pop()

    def append(self, card):
        if not isinstance(card, Card):
            raise TypeError('Csak kartya tipust lehet hozzaadni')
        super().append(card)


# d = Deck()
# print(d)

class Hand(list):

    def __init__(self):
        super().__init__()
        self.value = 0
        self.ace = 0

    def append(self, card):
        if not isinstance(card, Card):
            raise TypeError('Csak kartya tipust lehet hozzaadni')
        super().append(card)
        self.value += CardData.get_value(card.rank)
        if card.rank == 'Asz':
            self.ace += 1

    def set_aces(self):
        while self.value > 21 and self.ace:
            self.value -= 10
            self.ace -= 1


class Tokens:

    def __init__(self, summa=100):
        self.sum = summa
        self.bet = 0

    @property
    def sum(self):
        return self.__sum

    @sum.setter
    def sum(self, value):
        if value > 0:
            self.__sum = value
        else:
            raise ValueError('Az ertek nem lehet negativ vagy 0')

    @property
    def bet(self):
        return self.__sum

    @bet.setter
    def bet(self, value):
        if value >= 0 and self.sum - value >= 0:
            self.__bet = value
        else:
            raise ValueError('A tet csak egesz szam lehet,'
                             'es nem adhat meg tobb tetetmint amennyi zsetonja van.')

    def win_bet(self):
        self.__sum += self.bet

    def lose_bet(self):
        self.__sum -= self.bet

class Rules:
    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def betting(chips: Tokens):
        while True:
            try:
                chips.bet = int(input('Mennyi zsetont szeretne feltenni: '))
            except ValueError:
                print('Sajnalom az ertek nem megfelelo')
            else:
                break

    @staticmethod
    def draw(cards_deck: Deck, hand: Hand):
        hand.append(cards_deck.div())
        hand.set_aces()

    @staticmethod
    def draw_or_stop(cards_deck: Deck, hand: Hand):
        while True:
            var = input('Huzni szeretne vagy megallni? Nyomj egy "h"-t vagy "m"-t: ')
            if var[0].lower() == 'h':
                Rules.draw(cards_deck, hand)
            elif var[0].lower() == 'm':
                print('A jatekos megalt! Az oszto jatszik')
                CardData.is_playing = False
            else:
                print('ilyen opcio nincs')
                continue
            break

    @staticmethod
    def player_cards(card_player: Hand):
        print('A jatekos kezeben van:\n', *card_player, sep='\n')
        print('A jatekos kezeben levo lapok aktualis osszerteke: ', card_player.value)

    @staticmethod
    def not_show_all(card_player: Hand, card_dealer: Hand):
        print('Az oszto kezeben van: ')
        print('<Kartyalap rejtve>')
        print(card_dealer[1])
        Rules.player_cards(card_player)

    @staticmethod
    def show_all(card_player: Hand, card_dealer: Hand):
        print('Az oszto kezeben van:\n', *card_dealer, sep='\n')
        print('Az jatekos kezeben levo lapok osszerteke:\n', card_player.value)
        Rules.player_cards(card_player)

    @staticmethod
    def player_lose(chips: Tokens):
        print('A jatekos eluszott')
        chips.lose_bet()

    @staticmethod
    def player_win(chips: Tokens):
        print('A jatekos nyert')
        chips.win_bet()

    @staticmethod
    def dealer_lose(chips: Tokens):
        print('Az oszto eluszott')
        chips.win_bet()

    @staticmethod
    def dealer_win(chips: Tokens):
        print('Az oszto nyert')
        chips.lose_bet()

    @staticmethod
    def equal(chips: Tokens):
        print('Az allas dontetlen, az oszto nyert')
        chips.lose_bet()

tokens = Tokens()

while True:
    print('Udvozlunk a BlackJack jatekban! A cel a 21 elerese\n'
          'Az oszto addig huz, amig el nem eri a 17-t\n'
          'Az Asz a szabalyok szerint 11-t vagy 1-et er')
    deck = Deck()
    deck.mix()

    player = Hand()
    dealer = Hand()

    Rules.draw(deck, player)
    Rules.draw(deck, player)
    Rules.draw(deck, dealer)
    Rules.draw(deck, dealer)

    Rules.betting(tokens)
    Rules.not_show_all(player, dealer)
    while CardData.is_playing:
        Rules.draw_or_stop(deck, player)
        Rules.not_show_all(player, dealer)
        if player.value > 21:
            Rules.player_lose(tokens)
        if player.value <= 21:
            while dealer.value < 17:
                Rules.draw(deck, dealer)
                if dealer.value > 21:
                    Rules.dealer_lose(tokens)
                elif dealer.value > player.value:
                    Rules.dealer_win(tokens)
                elif dealer.value < player.value:
                    Rules.player_win(tokens)
                else:
                    Rules.equal(tokens)
    print('\nA jatekos egyenlete: ', tokens.sum)
    new_game = input('Szeretne meg 1x jatszani? i-igen vagy n-nem: ')
    if new_game[0].lower() == 'i':
        CardData.is_playing = True
        continue
    print('Koszonjuk a jatekot!')
    break