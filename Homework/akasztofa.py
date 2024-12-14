# 1. Kategorizalt szo listak kulonbozo nehezsegi szintel
# 2. Nehezsegi szint kivalasztasa
# 3. Veletlenszeru szo kivalasztas
# 4. Valamilyen akasztofa
# 5. Statisztika az aktualis allapotrol
# 6. Felhasznaloi input kezelese
# 7. Kiirt rejtett szot frissitese
# 8. Gyozelem/ Vereseg stb...
import random


def get_word_list(difficulty: str):
    """
    Kategorizalt szo listak kulonbozo nehezsegi szintel
    :param difficulty: Nehezsegi szint
    :return: A kategorizalt szavak listaja
    """
    easy_words = ['cat', 'dog', 'hat', 'sun', 'tree']
    medium_words = ['python', 'guitar', 'teacher', 'jungle', 'planet']
    hard_words = ['complicated', 'encyclopedia', 'worcestershire', 'onomatopoeia', 'anachronism']

    if difficulty == 'easy':
        return easy_words
    elif difficulty == 'medium':
        return medium_words
    return hard_words


def choose_difficulty() -> str:
    """
    Nehezsegi szint kivalasztasa
    :return: Nehezsegi szint
    """
    while True:
        diff = input('Valassz egy nehezsegi szintet (easy, medium, hard): ').lower()
        if diff in ['easy', 'medium', 'hard']:
            return diff
        print('Ervenytelen valasztas! Csak easy, medium vagy hard lehet!')



def choose_word(word_list: list[str]) -> str:
    """
    Veletlenszeru szo kivalasztas
    :param word_list: Szavakat tartalmazo lista
    :return: Kivalasztott szo
    """
    return random.choice(word_list).upper()


def draw_hangman(tries_left: int):
    """
    Akasztofa rajzolasa
    :param tries_left: probalkozasok szama
    :return:
    """
    stages = [
        '''
         ----------
         |        |
         |
         |
         |
        ----
        ''',
        '''
         ----------
         |        |
         |        O
         |
         |
        ----
        ''',
        '''
         ----------
         |        |
         |        O
         |        |
         |
        ----
        ''',
        '''
         ----------
         |        |
         |        O
         |       /|
         |
        ----
        ''',
        '''
        ----------
         |        |
         |        O
         |       /|\\
         |        
        ----
        ''',
        '''
        ----------
         |        |
         |        O
         |       /|\\
         |       /
        ----
        ''',
        '''
        ----------
         |        |
         |        O
         |       /|\\
         |       / \\
        ----
        '''
    ]
    print(stages[6 - tries_left])


def display_game_state(hidden_word: list[str], incorrect_quesses: list[str], tries_left: int):
    """
    Statisztika az aktualis allapotrol
    :param hidden_word: A rejtett szo
    :param incorrect_quesses: Tippelt betuk szama
    :param tries_left: Jo probalkozasok szama
    :return:
    """
    draw_hangman(tries_left)
    print('\nJelenlegi allas:')
    print(' '.join(hidden_word))
    print('Hibas probalkozasok szama: ', len(incorrect_quesses))
    print('Hibas probalkozasok: ', ''.join(incorrect_quesses))
    print('Hatralavo probalkozasok szama: ', tries_left)


def get_player_quess(incorrect_quess: list[str], correct_guess: list[str]) -> str:
    """
    Felhasznaloi input kezelese
    :param incorrect_quess: Hibas probalkozasok
    :param correct_guess: Helyes probalkozasok
    :return: Tipp
    """
    while True:
        guess = input('Kerlek adj meg egy betut: ').upper()
        if len(guess) != 1 or not guess.isalpha():
            print('Csak egyetlen betut adj meg!')
        elif guess in incorrect_quess or guess in correct_guess:
            print('Ezt a betut mar probaltad!')
        else:
            return guess


def update_hidden_word(word: str, hidden_word: list[str], guess: str):
    """
    Kiirt/rejtett szot frissitese
    :param word: A feladvany szava
    :param hidden_word: rejtett szo
    :param guess: tipp
    :return:
    """
    for i, char in enumerate(word):
        if char == guess:
            hidden_word[i] = guess


def is_game_lost(tries_left: int) -> bool:
    """
    Vesztett-e a jatekos
    :param tries_left: probalkozasok szama
    :return: Vesztett-e
    """
    return tries_left <= 0


def is_game_won(hidden_word: list[str]):
    """
    Nyert-e a jatekos
    :param hidden_word: Rejtett szo
    :return: Nyert-e
    """
    return '_' not in hidden_word


def display_statistic(stats: dict):
    """
    Statisztika megjelenitese
    :param stats: Statisztikai adatok
    :return:
    """
    print('\nJatek statisztikak:')
    print(f'Osszes jatek: {stats['total_games']}')
    print(f'Gyozelmek: {stats['games_won']}')
    print(f'Helyesen kitalalt szavak: {', '.join(stats['words_guessed'])}')
    print(f'Hatralavo probalkozasok a gyoztes jatekban: {stats['tries_remaining']}')


def update_statistics(stats: dict, won: bool, word: str, tries_left: int):
    """
    Statisztika modositasa
    :param stats: Statisztikai adatokat tartalmazo szotar
    :param won: nyert-e a jatekos
    :param word: A feladvany szava
    :param tries_left: Probalkozasok szama
    :return:
    """
    stats['total_games'] += 1
    if won:
        stats['games_won'] += 1
        stats['words_guessed'].append(word)
        stats['tries_remaining'].append(tries_left)


def main():
    stats = {'total_games': 0, 'games_won': 0, 'words_guessed': [], 'tries_remaining': []}
    print('Udvozoljuk az Akasztofa jatekban!')
    while True:
        difficulty = choose_difficulty()
        word_list = get_word_list(difficulty)
        word = choose_word(word_list)
        hidden_word = ['_'] * len(word)
        incorrect_guess = []
        correct_guess = []
        tries_left = 6
        game_over = False

        while not game_over:
            display_game_state(hidden_word, incorrect_guess, tries_left)
            guess = get_player_quess(incorrect_guess, correct_guess)
            if guess in word:
                correct_guess.append(guess)
                update_hidden_word(word, hidden_word, guess)
                if is_game_won(hidden_word):
                    print(f'\nGratulalunk! Megnyerted a jatekot! Ha helyes szo: {word}')
                    game_over = True
                    update_statistics(stats, True, word, tries_left)
                else:
                    incorrect_guess.append(guess)
                    tries_left -= 1
                    if is_game_lost(tries_left):
                        draw_hangman(0)
                        print(f'\nSajnalom vesztettel! A helyes szo: {word}')
                        game_over = True
                        update_statistics(stats, False, word, tries_left)
            display_statistic(stats)

        if not input('Szeretnél ujra jatszani? (Igen/Nem): ').lower().startswith('i'):
            print('Viszlat! Koszonom a jatekot.')
            break


main()