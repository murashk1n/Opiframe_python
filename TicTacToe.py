import os
import random

X = 'X'
O = 'O'
EMPTY = ' '
COMP_MOVES = [4, 0, 2, 6, 8, 1, 3, 5, 7]

computer = ' '
player = ' '
answer = 0
count = 0
board = [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
isWinner = False
move = 1
nextMove = 0

winComb = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

def checkWinRow(c):
    global nextMove
    for row in range(8):
        if board[winComb[row][0]] == EMPTY and board[winComb[row][1]] == board[winComb[row][2]] == c:
            nextMove = winComb[row][0]
            return True
        elif board[winComb[row][0]] == board[winComb[row][2]] == c and board[winComb[row][1]] == EMPTY:
            nextMove = winComb[row][1]
            return True
        elif board[winComb[row][0]] == board[winComb[row][1]] == c and board[winComb[row][2]] == EMPTY:
            nextMove = winComb[row][2]
            return True

def displayBoard(board):
    print(f"\n\t {board[0]} | {board[1]} | {board[2]}\t O | 1 | 2")
    print("\t-----------\t-----------")
    print(f"\t {board[3]} | {board[4]} | {board[5]}\t 3 | 4 | 5")
    print("\t-----------\t-----------")
    print(f"\t {board[6]} | {board[7]} | {board[8]}\t 6 | 7 | 8\n")

def isCellEmpty(cell):
    return board[cell] == EMPTY

def chooseCornerCell():
    for i in range(0, 9, 2):
        if i == 4:
            continue
        if isCellEmpty(i):
            return i
    return 10

def randomMove(c):
    while True:
        random_num = random.randint(0, 8)
        if isCellEmpty(random_num):
            board[random_num] = c
            break

def computerTurnHardLevel():
    global move
    if move == 1 or move == 2:
        if isCellEmpty(4):
            board[4] = computer
            move += 1
        else:
            board[chooseCornerCell()] = computer
            move += 1
    else:
        if checkWinRow(computer) is True:
            board[nextMove] = computer
        elif checkWinRow(player) is True:
            board[nextMove] = computer
        elif chooseCornerCell() != 10:
            board[chooseCornerCell()] = computer
        else:
            randomMove(computer)

def checkWinner():
    global isWinner
    for row in range(8):
        if board[winComb[row][0]] != EMPTY and board[winComb[row][0]] == board[winComb[row][1]] == board[winComb[row][2]]:
            isWinner = True
            return board[winComb[row][0]]
    return EMPTY

def whoWinner():
    winner = checkWinner()
    if winner == player:
        print("\n You win!\n")
    elif winner == computer:
        print("\n Computer win!\n")
    else:
        print("\nDead heat\n")

def isFreeCell():
    for i in range(9):
        if board[i] == EMPTY:
            return True

def computerTurnMediumLevel():
    global count
    while not isWinner:
        if isCellEmpty(COMP_MOVES[count]):
            board[COMP_MOVES[count]] = O
            break
        count += 1

def playerTurn():
    global isWinner
    while not isWinner:
        if isFreeCell() is True:
            try:
                answer = int(input("\nYour turn: "))
                if answer > 8 or answer < 0:
                    print("\nIllegal move! Choose number between 0 and 8!\n\n")
                    continue
                if isCellEmpty(answer) is True:
                    board[answer] = player
                    displayBoard(board)
                    break
                else:
                    print("\nThat square is already occupied\n")
                    continue
            except ValueError:
                print("\nInvalid input! Please enter a number.\n")
                continue
        else:
            break

def computerTurn():
    global isWinner
    print("\nComputer turn: ")
    if isFreeCell() is True:
        if level == 2:
            computerTurnMediumLevel()
        elif level == 3:
            computerTurnHardLevel()
        else:
            randomMove(computer)
    displayBoard(board)

def startMenu():
    global player, computer,level
    print("Welcome to Tic-Tac-Toe.")
    print("Choose level 1-easy, 2-medium, 3-hard\n")
    try:
        level = int(input("\nYour choose: "))
        random_num = random.randint(0, 100)
        player, computer = (X, O) if random_num >= 50 else (O, X)
        print(f"\nRandom choose: {player} for you")
        print("\nMake your move by entering a number, 0-8")
        displayBoard(board)
    except ValueError:
        print("\nInvalid input! Please enter a number.\n")

def main():
    global isWinner
    startMenu()
    while not isWinner:
        os.system('clear' if os.name == 'posix' else 'cls')
        displayBoard(board)
        if player == X:
            playerTurn()
            checkWinner()
            computerTurn()
        else:
            computerTurn()
            checkWinner()
            if isFreeCell() is False:
                break
            playerTurn()
        if isFreeCell() is False:
            break
        checkWinner()
    whoWinner()

if __name__ == "__main__":
    main()