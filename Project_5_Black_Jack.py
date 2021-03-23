# 5. project - Black Jack
import random


SEPARATOR = 55 * "-"

# card attributes
SUITS = ["♣", "♦", "♥", "♠"]
FACES = ["J", "Q", "K", "A"]
VALUES = list(range(2, 11)) + FACES


def create_deck():
    deck = []
    for suit in SUITS:
        for value in VALUES:
            deck.append(suit + str(value))
    return deck


def shuffle_deck(deck):
    random.shuffle(deck)
    return deck


def register_players():
    while True:
        n = input("How many players? (max 6) ")
        try:
            players = []
            if int(n) > 6:
                print("Max 6 players! ")
                continue
            for num in range(1, int(n) + 1):
                name = input(f"Player {str(num)}, please enter your name: ")
                players.append([name, 50])  # 50$ is entry money
            break
        except ValueError:
            print("Please enter number! ")
    players.append(["House", 1_000])
    return players


def put_bets(players):
    min_bet = 10
    for i, (player, money) in enumerate(players[:-1]):
        while True:
            bet = input(f"Player {player}, how much money do you want to bet? "
                        f"You have: {money} $ ")
            try:
                if int(bet) < min_bet:
                    print("Min. bet is 10 $.")
                    continue
                if min_bet <= int(bet) <= money:
                    players[i] += [int(bet), []]
                    players[i][1] -= int(bet)
                    break
                else:
                    print("You don't have enough money for this bet..")
            except ValueError:
                print("Please enter number!")
    players[-1] += [0, []]  # house
    if [] in players:
        players.remove([])  # remove players with not enough money


def serve_players(deck, players):
    for i in range(2):
        p = players if i == 0 else players[:-1]  # House gets only 1 card
        for player in p:
            card = deck.pop()
            player[3].append(card)


def show_table(players):
    print(SEPARATOR)
    template = "{:15} | {:20} | {:4} | {:4} $ |"
    print(template.format("NAME", "CARDS ", "SUM", "BET:"))
    for player in players:
        name, money, bet, hand = player
        table = template.format(name.upper(), " ".join(hand),
                                check_hand(hand), bet)
        print(table)
    print(SEPARATOR)


def check_hand(hand):
    on_hand = [card_value(card) for card in hand]
    if sum(on_hand) > 21 and 11 in on_hand:
        on_hand[on_hand.index(11)] = 1
    return sum(on_hand)


def card_value(card):
    value = card.strip("♣♦♥♠")
    if value in FACES[:-1]:
        return 10
    elif value == "A":
        return 11
    else:
        return int(value)


def play(players, deck):
    for player in players:
        name, money, bet, hand = player
        if name == "House":
            while check_hand(hand) < 17:
                hand.append(deck.pop())
            show_table(players)
        else:
            while True:
                show_table(players)
                on_hand = check_hand(hand)
                print(f"Player {name} your cards: {' '.join(hand)}")
                if on_hand == 21:
                    print("Black Jack!")
                    break

                if len(hand) == 2\
                        and card_value(hand[0]) == card_value(hand[1])\
                        and bet <= money:
                    split = input(
                        f"Player {name} do you want to split? y/n ")
                    if split.lower() == "y":
                        player = hand_split(players, player, deck)
                        on_hand = check_hand(hand)
                    else:
                        break
                elif len(hand) == 2 and bet <= money:
                    double_down = input(f"Player {name} Do you want to "
                                        f"double down? y/n ")
                    if double_down == "y":
                        player[1] -= bet
                        player[2] *= 2
                        player[3].append(deck.pop())
                        on_hand = check_hand(hand)
                        show_table(players)

                if on_hand >= 22:
                    print("Bust!")
                    break
                else:
                    draw = input(f"Player {name} Do you want to draw? y/n ")
                    if draw.lower() == "y":
                        hand, on_hand = draw_card(hand, deck)
                    else:
                        break


def hand_split(players, player, deck):
    name, money, bet, hand = player
    player[1] -= bet
    players.insert(-1, [name + "*", 0, bet, [hand[1], deck.pop()]])
    hand.pop()
    hand.append(deck.pop())
    print(f"Player {name} your cards: {' '.join(hand)}")
    return player


def draw_card(hand, deck):
    hand.append(deck.pop())
    on_hand = check_hand(hand)
    return hand, on_hand


def evaluate_game(players):
    house_hand = check_hand(players[-1][3])
    for i, (player, money, bet, hand) in enumerate(players[:-1]):
        on_hand = check_hand(hand)
        if on_hand == 21 and not house_hand == 21:
            players[i][1] += 1.5 * bet
            print(f"{player} you got Black Jack! You win: {1.5 * bet} $")
        elif on_hand == house_hand:
            players[i][1] += bet
            print(f"{player} It's a tie! You get your bet back: {bet} $")
        elif on_hand > 21 or on_hand < house_hand <= 21:
            players[-1][1] += bet
            print(f"{player} you lost your money: {bet} $")
        elif 21 > on_hand > house_hand or house_hand > 21:
            players[i][1] += 2 * bet
            print(f"{player} you win! You get: {2 * bet} $")
        if "*" in player:
            win_money = players[i][1]
            name = player.strip("*")

            for j, p in enumerate(players[:-1]):
                print(p[0])
                if name == p[0]:
                    players[j][1] += win_money
            players[i] = []
    if [] in players:
        players.remove([])
    for player in players:
        player.pop(-1)
        player.pop(-1)
    show_final_table(players)


def show_final_table(players):
    SEP = "-" * 28
    print(SEP)
    template = "{:15} | {:^6} $ |"
    print(template.format("NAME", "MONEY:"))
    for player in players:
        name, money = player
        table = template.format(name.upper(), money)
        print(table)
    print(SEP)


def main():
    players = register_players()
    while True:
        new_players = []
        for player in players:
            if player[1] >= 10:
                new_players.append(player)
        deck = create_deck()
        shuffle_deck(deck)
        put_bets(new_players)
        serve_players(deck, new_players)
        play(new_players, deck)
        evaluate_game(new_players)
        if len(new_players) < 2 or input("Play again? y/n ").lower() != "y":
            print("GAME OVER")
            break


main()
