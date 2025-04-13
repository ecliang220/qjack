from Game import Game


def main():
    playerName = input("Player Name: ")
    qJackGame = Game(playerName)
    response = 'y'
    while (response == 'y'):
        qJackGame.play_round()
        response = input('Play another round? (y/n)')

if __name__ == '__main__':
    main()