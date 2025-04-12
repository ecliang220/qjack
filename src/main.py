from Game import Game


def main():
    qJackGame = Game()
    response = 'y'
    while (response == 'y'):
        qJackGame.play_round()
        response = input('Play another round? (y/n)')

if __name__ == '__main__':
    main()