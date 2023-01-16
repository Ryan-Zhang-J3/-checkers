class CheckersGame:
    def __init__(self):
        self.board = [ [0, 2, 0, 2, 0, 2, 0, 2]
                     , [2, 0, 2, 0, 2, 0, 2, 0]
                     , [0, 2, 0, 2, 0, 2, 0, 2]
                     , [0, 0, 0, 0, 0, 0, 0, 0]
                     , [0, 0, 0, 0, 0, 0, 0, 0]
                     , [1, 0, 1, 0, 1, 0, 1, 0]
                     , [0, 1, 0, 1, 0, 1, 0, 1]
                     , [1, 0, 1, 0, 1, 0, 1, 0]
                     ]
        self.whoseMove = "white"
        self.isWon = ""

    def checkWinner(self) :
        redCheckers = 0
        whiteCheckers = 0
        for checkerRow in self.board:
            for checkerPos in checkerRow:
                if checkerPos == 1 or checkerPos == 3:
                    whiteCheckers += 1
                elif checkerPos == 2 or checkerPos == 4:
                    redCheckers += 1
        if redCheckers == 0 and whiteCheckers != 0:
            self.isWon = "white"
        elif redCheckers != 0 and whiteCheckers == 0:
            self.isWon = "red"
    
    def changeTurn(self) :
        if self.whoseMove == "white":
            self.whoseMove = "red"
        else:
            self.whoseMove = "white"
    
    def parseMove (self, move) :
        moveList = []
        coordinates = move.split()
        for i in range( len( coordinates ) ):
            y = int( coordinates[i][0] )
            x = int( coordinates[i][1] )
            if y not in range( 0, 8 ) or x not in range( 0, 8 ):
                raise ValueError("Invalid Move")
            moveList.append( (y, x))    
        return tuple( moveList )
    
    def move(self, move) :
        moves = self.parseMove( move )
        for i in range( len( moves ) - 1 ):
            y1 = moves[i][0]
            x1 = moves[i][1]
            y2 = moves[i+1][0]
            x2 = moves[i+1][1]
            if self.whoseMove == "white" and y2 == 0:
                self.board[y2][x2] = 3
            elif self.whoseMove == "red" and y2 == 7:
                self.board[y2][x2] = 4
            else:
                self.board[y2][x2] = self.board[y1][x1]
            self.board[y1][x1] = 0
        self.changeTurn()
        self.checkWinner()
        
    def isValidMove(self, move) : 
        moves = self.parseMove( move )
        Y = moves[0][0]
        X = moves[0][1]
        if self.whoseMove == "white" and self.board[Y][X] != 1 and self.board[Y][X] != 3:
            return False
        if self.whoseMove == "red" and self.board[Y][X] != 2 and self.board[Y][X] != 4:
            return False
        if len( moves ) < 2:
            return False

        isJump = False
        king = False

        for i in range( len( moves ) - 1 ):

            self.checkWinner()
            if self.isWon == "white" or self.isWon == "red":
                return False

            srcY = moves[i][0]
            srcX = moves[i][1]
            dstY = moves[i+1][0]
            dstX = moves[i+1][1]

            if isJump == False:
                isJump = ( abs( srcY - dstY ) == 2 )
            if isJump:
                enemy =  self.board[ int((srcY+dstY)/2 )][int((srcX+dstX)/2)]
                if self.whoseMove == "white" and enemy != 2 and enemy != 4 :
                    return False
                elif self.whoseMove == "red" and enemy != 1 and enemy != 3 :
                    return False

            if king == False:
                if self.whoseMove == "white" and srcY == 0 or self.whoseMove == "red" and srcY == 7 or self.board[srcY][srcX] == 3 or self.board[srcY][srcX] == 4:
                    king = True

            if self.whoseMove == "white":
                aheadY = 2 if isJump  else 1
            else:
                aheadY = -2 if isJump  else -1
            backY = 0 - aheadY if king else aheadY

            if self.board[dstY][dstX] == 0:
                validMove = ( ( dstY == srcY - aheadY ) or ( dstY == srcY - backY ) ) and ( dstX == srcX - aheadY or dstX == srcX + aheadY )
                if validMove == False:
                    return False
                if isJump == False:
                    if i+1 == len( moves ):
                        if self.whoseMove == "white" and dstY == 0:
                            self.board[dstY][dstX] = 3
                        elif self.whoseMove == "red" and dstY == 7:
                            self.board[dstY][dstX] = 4
                        else:
                            self.board[dstY][dstX] = self.board[dstY][dstX]
                        return True
                    else:
                        return False

                self.board[ int( (srcY+dstY)/2 ) ][int( (srcX+dstX)/2 )] = 0
                if self.whoseMove == "white" and dstY == 0:
                    self.board[dstY][dstX] = 3
                elif self.whoseMove == "red" and dstY == 7:
                    self.board[dstY][dstX] = 4
                else:
                    self.board[dstY][dstX] = self.board[dstY][dstX]
            else:
                return False

        return True