"""
A Python module for the Gomoku game.
"""
from copy import deepcopy # you may use this for copying a board
from random import randint #Used to randomly pick the move for the computer

def newGame(player1, player2):
    """
    Creates a new game to play
    Excpetions are entering an empty string

    Parameters 
    ----------
    player1 : String
        The name of the first player
    player2 : String
        The name of the second player

    Returns
    -------
    game : Dictionnary
        Stores the name of the first player as player1
        The second player as player2
        Stores who's turn it is as who and is automatically 1
        Saves the empty board as board

    """
    #Saving the new game
    game = {'player1': player1,'player2': player2, 'who': 1,
            'board': [[0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0]]}
    return game

def printBoard(board):
    """
    Displays the board being played on in a nicely formatted way
    Exceptions are a board with the wrong dimension are incorrect values

    Parameters
    ----------
    board : 2D Array
        The current state of the board that is being played on

    Returns
    -------
    No return out of the function
    It only prints out the board

    """
    #Creates a copy of the board to not affect the values
    board2 = deepcopy(board)
    #Converting the digit board to a "real" board
    for i in range(0,len(board2)):
        for j in range(0,len(board2[i])):
            if board2[i][j] == 1:
                board2[i][j] = 'X'
            elif board2[i][j] == 2:
                board2[i][j] = 'O'
            else:
                board2[i][j] = " "
    #Printing the header of the board
    print(" |a|b|c|d|e|f|g|h|")
    print(" +-+-+-+-+-+-+-+-+")
    #Printing each row of the board as a table
    for i in range(0,len(board2)):
        print(str(i+1)+"|" +"|".join(board2[i][j] for j in range(0,len(board2[i])))+"|")
    #Printing the bottom of the board
    print(" +-+-+-+-+-+-+-+-+")

def posToIndex(s):
    """
    Converts a player move to the equivalent index of a list to store it in a tuple
    Excpetions are a move which isn't on the board
    
    Parameters
    ----------
    s : String
        The move the player wants to make.

    Returns
    -------
    False if there was any exception
    A tuple of length 2 containing the index position of the move

    """    
    #Defining the valid letter positions
    row = ['a','b','c','d','e','f','g','h']
    #turning the position into a list and making any letter lower case
    s = list(s.replace(" ","").lower())
    #Making sure the letter and number of the move are the right way round
    try:
        s[0] = int(s[0])
    except: 
        try : 
            s[0],s[1]=s[1],s[0]
        #Returns false if the list is of length 1
        except IndexError: return(False)
    #Checking the move has converted to a valid move, returns false if it isn't
    try:
        s[0] = int(s[0])
        if len(s) != 2 or s[1] not in row or s[0] < 1 or s[0] > 8: return(False)
    except ValueError: return(False)
    #Return the move as a tuple as it is valid
    return((s[0]-1,row.index(s[1])))

def indexToPos(t):
    """
    Converting an index move to a human readable move
    Exceptions:
        A tuple which doesn't have a length of 2 
        Values of an index not equal to [0:8]

    Parameters
    ----------
    t : Tuple
        The index value of the move

    Returns
    -------
    The human readable form of the move as a string
    
    """
    #defining the letter for the human readable form
    row = ['a','b','c','d','e','f','g','h']
    #Returning the human readable form as a string
    return(str(row[t[1]])+str(t[0]+1)) 

def loadGame(filename):
    """
    Loading a game from a file to resume the state of play 
    Defaults to opening 'game.txt' if no filename is given

    Parameters
    ----------
    filename : string
        The file storing a previously played game with all values of the game
    Exceptions:
        The file is not there
        Not all the required information for a game is in the file
        The data is not of the right type

    Returns
    -------
    A file not found error if it can't find the file
    A value error if any other exception happens
    The dictionnary game if a valid game has been loaded
    """
    #If no file is specified defaults to 'game.txt'
    if not filename.strip():
        filename = 'game.txt'
    #Defining an empty board and an empty dictionnary
    board,game=[0]*8,{}
    try:
        #opens the file amd reurns a file not found error if it's not there
        with open(filename, mode='rt',encoding="utf8") as f:
            #Reading the game information into the game dictionary and raising a value error if any data is wrong
            try:
                game["player1"] = f.readline().strip('\n').capitalize()
                game["player2"] = f.readline().strip('\n').capitalize()
                game["who"] = int(f.readline().strip('\n'))
                if not game.get('player1').strip() or not game.get('player2').strip() or game.get('who') != 1 and game.get('who') != 2: raise ValueError
                for i in range(0,8):
                    board[i] = list(map(int,f.readline().strip('\n').split(",")))
                    if len(board[i]) != 8: raise ValueError
                    for j in range(0,len(board[i])):
                        if board[i][j] != 0 and board[i][j] != 1 and board[i][j] != 2: raise ValueError
                        
                if f.readline() != "": raise ValueError
                game["board"] = board
            except ValueError: raise ValueError
    except FileNotFoundError: raise FileNotFoundError()
    return(game)

def getValidMoves(board):
    """
    Calculates all the moves that can be made

    Parameters
    ----------
    board : 2D Array
        The current state of the game being played
    Exceptions:
        an inccorectly defined board
    Returns
    -------
    possmove: list
        the list of all possiible moves

    """
    #Defines an empty list 
    possmove = []
    for i in range(0,len(board)):
        for j in range(0,len(board[i])):
            if board[i][j] == 0:
                possmove.append((i,j))
    return(possmove)

def makeMove(board,move,who):
    """
    Updates the board with the move the player who's turn it is has made

    Parameters
    ----------
    board : 2D array
        The current state of the game being played
    move : Tuple
        The move to be made
    who : Integer
        The person who's turn it is
    Exceptions are the move being outside the range of the board
    Returns
    -------
    The updated board
    
    """
    #Saving the persons move and returning it
    board[move[0]][move[1]] = who
    return(board)

def hasWon(board,who):
    """
    Checking if the player has made the required moves to win having 5 moves alongside each other

    Parameters
    ----------
    board : 2D array
        Stores the current state of the game in play
    who : Integer
        The person who is being checkede if they won
    Exceptions are the board being incorrect or an incorrect person being checked
    Returns
    -------
    True if the player has won
    False if they have not

    """
    
    #Check horizontally for a win
    for i in range(0,len(board)):
        count = 0
        for j in range(0,len(board[i])-1):
            if board[i][j] == board[i][j+1]== who:
                count += 1
                if count >= 4: return(True)
            else: count = 0
    #Check vertical for win
    for i in range(0,len(board)):
        count = 0
        for j in range(0,len(board[i])-1):
            if board[j][i] == board[j+1][i] == who:
                count += 1
                if count >= 4: return(True)
            else: count = 0
    #Check diagonally for a win from top left to bottom right
    if diag_check(board, who, 0, 4, 1,0): return(True)
    #Check diagonal win from bottom left to top right
    if diag_check(board, who, 7, 3, -1,7): return(True)

    return(False)

def diag_check(board, who, x, y, sign, start): #My own function to make it more efficient
    """
    Checks the diagonal of the board for a win if the player has made 5 moves alongside each other

    Parameters
    ----------
    board : 2D Array
        Current state of the game in play
    who : Integer
        The person who is being checked if they won
    x : Integer
        The first row to check from
    y : Integer
        The last row to check too
    sign : Integer
        Which way to check the board
    start : Integer
        The columns to start from
    
    Exceptions:
        The board being incorrect or an incorrect person being checked
        Starting on rows and columns which are outside the size of the board
        Jumping too many rows 
    Returns
    -------
    True if the player won
    False if they have not
    
    """
    #Going along the rows and checking their diagonals
    for i in range(x,y,sign):
        k, count =0,0
        for j in range(i,7-start,sign): ##This accounts for variable diagonal length
            if board[j][k] == board[j+sign][k+1] == who:
                count += 1
                if count >= 4: return(True)
            else: count = 0
            k+=1
    #Goes accross the columns left and checks their diagonals
    for i in range(1,4):
        k, count = start, 0
        for j in range(i,7):
            if board[k][j] == board[k+sign][j+1] == who:
                count += 1
                if count >= 4: return(True)
            else: count = 0
            k += sign
    return(False)
            
def suggestMove1(board,who):
    """
    Checks the moves to decide an appropriate one
    Checks first if there is a move that would mean a win
    Then checks if a move stops the other player winning
    Then randomly decides a move to do if there isn't anything else

    Parameters
    ----------
    board : 2D array
        Stores the current state of the game in play    
    who : Integer
        The person who is being checkede if they won
    Excpetions are an incorrect board or player

    Returns
    -------
    A tuple with the index position for the move that should be played

    """
   #a List with all the possible moves and a copy of the board being played 
    poss_moves, board2 = getValidMoves(board), deepcopy(board)
    #Checking if the player can make a move to win and returning it if there is one
    for i in range(0,len(poss_moves)):
        if hasWon(makeMove(board2,poss_moves[i],who),who):
            return(poss_moves[i])
        else: board2 = deepcopy(board)
    #Checking if the player can make a move to stop the other player winning and returning it if there is one 
    if who == 1: 
        other_player = 2
    else: 
        other_player = 1 
    for i in range(0,len(poss_moves)):
        if hasWon(makeMove(board2,poss_moves[i],other_player),other_player):
            return(poss_moves[i])
        else: board2 = deepcopy(board)
    #Returning a random move if no better move can be made
    return(poss_moves[randint(0,len(poss_moves)-1)])

# ------------------- Main function --------------------
def play():
    """
    The main function for game to be run
    Outputs a welcome screen
    Determines if a game is being loaded or who the 2 players are. If they are human or not
    Then setups the game with the provided data and runs until a plaer wins or there is a draw

    Parameters
    ----------
    player1: String input
        The name of the first player or if a file should be loaded
    player2: String input
        The name of the second player if the game is not being loaded from a file
    move: string
        the move the human player wants to make
    Exceptions:
        Nothing being entered for a name
        Invalid moves outside the range of the board
    Returns
    -------
    The current state of the board and the player who needs to enter their move
    The result of the game when it finishes

    """
    #The welcome screen for the board
    print("*"*55)
    print("***"+" "*11+"WELCOME TO STEFAN'S GOMOKU!"+" "*11+"***")
    print("*"*55,"\n")
    print("Enter the players' names, or type 'C' or 'L'.\n")
    #Defining empty player names 
    player1,player2 = "", ""    
    #Getting the first player name until something valid is put in, loads the file if that is what is stated
    while not player1.strip():
        player1 = str(input("Enter the name of player 1: "))
    if player1.capitalize() == "L":
        game = loadGame(str(input("Enter the filename: ")))
    #Getting the second players name if not being loaded from the file and setting up a new game
    else:
        while not player2.strip():
            player2 = str(input("Enter the name of player 2: "))
            player1,player2 = player1.capitalize(),player2.capitalize()
            game = newGame(player1,player2)
    while True:
        #A human is playing
        if game.get('player'+str(game.get('who'))) != 'C':
            print()
            #Show the state of the board to the player and get them to input a move
            printBoard(game.get('board'))
            move = posToIndex(str(input("Player "+str(game.get('who'))+" enter your move: ")))
            #Gets an input until a valid move is inputted
            while move == False or not move in getValidMoves(game.get('board')):
                print("Invalid move try again")
                move = posToIndex(str(input("Player "+str(game.get('who'))+" enter your move: ")))
            #Makes the move to update board as it is now valid
            makeMove(game.get('board'),move,game.get('who'))
        #A computer is playing     
        else:
            #Uses suggestMove1 to make the move for the computer
            makeMove(game.get('board'),suggestMove1(game.get('board'),game.get('who')),game.get('who'))

        #Checking if the player who has played has won and ends the game appropriately if they have
        if hasWon(game.get('board'),game.get('who')):
            print("\nPlayer %d:"%game.get('who'), "%s has won\n"%game.get('player'+str(game.get('who'))))
            printBoard(game.get('board'))
            break 
        #Checking if there is a draw and ends the game appropriately if there is 
        elif len(getValidMoves(game.get('board'))) == 0:
            print("\nThere was a draw\n")
            printBoard(game.get('board'))
            break
        if game.get('who') == 1:
            game['who'] = 2
        else: game['who'] = 1

# the following allows your module to be run as a program
if __name__ == '__main__' or __name__ == 'builtins':
    play()