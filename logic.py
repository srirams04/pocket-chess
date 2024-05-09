import logmessage


def define_basic_global_variables():
    global blrook1, blhor1, blbish1, blqueen, blking, blbish2, blhor2, blrook2, p1, p2, p3, p4, p5, p6, p7, p8,emp,P1, P2, P3, P4, P5, P6, P7, P8, whrook1, whhor1, whbish1, whqueen, whking, whbish2, whhor2, whrook2, colour, list2d, List_of_Moves, chance, enpassant_possible, pawnnum
    
    #Creating White pieces
    whrook1=["rook", "*][", 7, 0, False] #Identity(no shortforms. Full name), Symbol(It will be modified based on the "piece" choice given by the user), Rownumber, Columnnumber, Moved?
    whrook2=["rook", "*][", 7, 7, False] #The numbers for rownumber and columnumber are based on 2D list indexing and not Usual Chess Address
    whhor1=["horse", "*/>", 7, 1]
    whhor2=["horse", "*/>", 7, 6]
    whbish1=["bishop", "*A", 7, 2]
    whbish2=["bishop", "*A", 7, 5]
    whqueen=["queen", "*Q", 7, 3]
    whking=["king", "*$", 7, 4, False]
    P1=["pawn", "*^", 6, 0, False] #False indicating that the pawn cannot be a victim of en passant capture. When it is susceptible, it will be changed to True.
    P2=["pawn", "*^", 6, 1, False]
    P3=["pawn", "*^", 6, 2, False]
    P4=["pawn", "*^", 6, 3, False]
    P5=["pawn", "*^", 6, 4, False]
    P6=["pawn", "*^", 6, 5, False]
    P7=["pawn", "*^", 6, 6, False]
    P8=["pawn", "*^", 6, 7, False]

    #Creating Black pieces
    blrook1=["rook", "][", 0, 0, False] #Identity(no shortforms. Full name), Symbol(It will be modified based on the "piece" choice given by the user), Rownumber, Columnnumber
    blrook2=["rook", "][", 0, 7, False] #The numbers for rownumber and columnumber are based on 2D list indexing and not Usual Chess Address
    blhor1=["horse", "/>", 0, 1]
    blhor2=["horse", "/>", 0, 6]
    blbish1=["bishop", "A", 0, 2]
    blbish2=["bishop", "A", 0, 5]
    blqueen=["queen", "Q", 0, 3]
    blking=["king", "$", 0, 4, False]
    p1=["pawn", "^", 1, 0, False]
    p2=["pawn", "^", 1, 1, False]
    p3=["pawn", "^", 1, 2, False]
    p4=["pawn", "^", 1, 3, False]
    p5=["pawn", "^", 1, 4, False]
    p6=["pawn", "^", 1, 5, False]
    p7=["pawn", "^", 1, 6, False]
    p8=["pawn", "^", 1, 7, False]

    emp=["", "", 0, 0] #Empty

    list2d=[[blrook1, blhor1, blbish1, blqueen, blking, blbish2, blhor2, blrook2],[p1, p2, p3, p4, p5, p6, p7, p8],[emp]*8,[emp]*8,[emp]*8,[emp]*8,[P1, P2, P3, P4, P5, P6, P7, P8],[whrook1, whhor1, whbish1, whqueen, whking, whbish2, whhor2, whrook2]]

    List_of_Moves=[]

    chance="white"
    
    enpassant_possible=False #Is an en passant capture possible in the next move?

    pawnnum=1 #A number used to identify the pieces which are formed after a pawnpromotion


def copy_of_init_list2d():
    #None of the below variables are global variables. ALL of them are LOCAL variables.
    #Creating White pieces
    whrook1=["rook", "*][", 7, 0, False] #Identity(no shortforms. Full name), Symbol(It will be modified based on the "piece" choice given by the user), Rownumber, Columnnumber, Moved?
    whrook2=["rook", "*][", 7, 7, False] #The numbers for rownumber and columnumber are based on 2D list indexing and not Usual Chess Address
    whhor1=["horse", "*/>", 7, 1]
    whhor2=["horse", "*/>", 7, 6]
    whbish1=["bishop", "*A", 7, 2]
    whbish2=["bishop", "*A", 7, 5]
    whqueen=["queen", "*Q", 7, 3]
    whking=["king", "*$", 7, 4, False]
    P1=["pawn", "*^", 6, 0, False] #False indicating that the pawn cannot be a victim of en passant capture. When it is susceptible, it will be changed to True.
    P2=["pawn", "*^", 6, 1, False]
    P3=["pawn", "*^", 6, 2, False]
    P4=["pawn", "*^", 6, 3, False]
    P5=["pawn", "*^", 6, 4, False]
    P6=["pawn", "*^", 6, 5, False]
    P7=["pawn", "*^", 6, 6, False]
    P8=["pawn", "*^", 6, 7, False]

    #Creating Black pieces
    blrook1=["rook", "][", 0, 0, False] #Identity(no shortforms. Full name), Symbol(It will be modified based on the "piece" choice given by the user), Rownumber, Columnnumber
    blrook2=["rook", "][", 0, 7, False] #The numbers for rownumber and columnumber are based on 2D list indexing and not Usual Chess Address
    blhor1=["horse", "/>", 0, 1]
    blhor2=["horse", "/>", 0, 6]
    blbish1=["bishop", "A", 0, 2]
    blbish2=["bishop", "A", 0, 5]
    blqueen=["queen", "Q", 0, 3]
    blking=["king", "$", 0, 4, False]
    p1=["pawn", "^", 1, 0, False]
    p2=["pawn", "^", 1, 1, False]
    p3=["pawn", "^", 1, 2, False]
    p4=["pawn", "^", 1, 3, False]
    p5=["pawn", "^", 1, 4, False]
    p6=["pawn", "^", 1, 5, False]
    p7=["pawn", "^", 1, 6, False]
    p8=["pawn", "^", 1, 7, False]

    emp=["", "", 0, 0] #Empty

    return [[blrook1, blhor1, blbish1, blqueen, blking, blbish2, blhor2, blrook2],[p1, p2, p3, p4, p5, p6, p7, p8],[emp]*8,[emp]*8,[emp]*8,[emp]*8,[P1, P2, P3, P4, P5, P6, P7, P8],[whrook1, whhor1, whbish1, whqueen, whking, whbish2, whhor2, whrook2]]


#generation of a requests link
def generate_code():
    return 1234


def encrypt(x):
    return x

    
#Aim: To display any list for debugging purposes
def displaylist(lst):
    colwd=25
    print("-"*(int(5*colwd)))
    for i in lst:
        for j in i:
            if colour(j)!="empty":
                clr=colour(j)
            else:
                clr=""
            print(clr+" "+j[0], end=" "*((colwd//2)-len(j[0]+" "+clr))+"|" + " "*(colwd//7))
        print()
        print("-"*(int(5*colwd)))


#Parameters: Starting address and the ending address as tuples
#Function: In list2d, the piece present in the starting address is moved to the ending address making 3 important changes
def move(add1, add2):
    global list2d
    list2d[add2[0]][add2[1]]=list2d[add1[0]][add1[1]]
    list2d[add1[0]][add1[1]]=emp
    list2d[add2[0]][add2[1]][2]=add2[0]
    list2d[add2[0]][add2[1]][3]=add2[1]


#Parameters: Starting address and the ending address as tuples, the list in which the move is to be made
#Function: In the list given as a parameter, the piece present in the starting address is moved to the ending address making 3 important changes
def validatemove(add1,add2,testf2d):
    testf2d[add2[0]][add2[1]]=testf2d[add1[0]][add1[1]]
    testf2d[add1[0]][add1[1]]=["", "", 0, 0]
    testf2d[add2[0]][add2[1]]=[testf2d[add2[0]][add2[1]][0], testf2d[add2[0]][add2[1]][1], add2[0], add2[1]]


#Aim: To get the colour of the piece
#Parameter: Piece
#Result: "black", "white" or "empty"
def colour(piece):
    if piece[1]=="":
        return "empty"
    elif piece[1][0]=="*":
        return "white"
    else:
        return "black"
    

#Given a color, the opposite colour is returned
def oppcolour(clr): #Opposite Colour
    if clr=="black":
        return "white"
    elif clr=="white":
        return "black"
    

#Aim: To check if two pieces belong to the same team
#Parameters: Example: whrook1, whbish2
#Return: True if they belong to the same team and False if they belong to different teams or if one of the pieces is ["", "", 0, 0]-->empty space
#Explanation: whrook1=["rook", "*...", rownumber, columnnumber], whbish2=["bishop", "*...", rownumber, columnnumber]. If the zeroth index of the 1st index of each of the two pieces is equal to *, both are white. If both do not contain *, they are both black. If only one of them contain, they are opposite teams. whrook1 and whbish2 belong to the same team.
def sameteam(pc1, pc2):
    if pc1[1]!="" and pc2[1]!="":
        if pc1[1][0]=="*" and pc2[1][0]=="*":
            return True
        elif pc1[1][0]!="*" and pc2[1][0]!="*":
            return True
        else:
            return False
    else:
        return False


#Aim: (To detect a CHECK, To check if a move will be intercepted by a piece) Given a starting address(based on 2D list indexing) and an ending address(same indexing), finding out all the pieces in between the two addresses on the CHESSBOARD STARTING from the starting address and moving to the ending address. 
#Parameters: starting address[given as a tuple], ending address[given as a tuple], a 2 dimensional list
#Note: If the starting address and the ending address lie in the same row, same column or same diagonal, the operation can be done. Otherwise, it cannot be done.
#Return: if pieces present in between return the Pieces in a tuple; if no pieces present, return empty tuple; if operation cannot be carried out, return "Invalid" 
#Example: parameters --> (0,1), (7,1), list2d  ;  output --> (value of p2, value of P2, value of whhor1)   ==> Output is a tuple not a list AND the element/piece present in the starting address is NOT given in the output  
#Explanation: [Refer to the chessboard on google docs] Between the two addresses given, p2, P2, whhor1 are present. blhor1 is NOT included.
def piecesbetween(add1, add2, f2d):
    if add1==add2:
        return ()

    if add1[0]==add2[0] or add1[1]==add2[1] or abs(add1[0] - add2[0])==abs(add1[1]- add2[1]):
        path=()
        
        if add1[0]==add2[0]:
            stepr=0
        else:
            stepr=(add2[0]-add1[0])//abs(add2[0]-add1[0])

        if add1[1]==add2[1]:
            stepc=0
        else:
            stepc=(add2[1]-add1[1])//abs(add2[1]-add1[1])

        curadd=(add1[0]+stepr, add1[1]+stepc) #Current address at which we are present and checking for pieces
        complete=False
        while complete==False:
            if curadd==add2:
                complete=True
                
            if f2d[curadd[0]][curadd[1]] ==["", "", 0, 0]:
                pass
            else:
                path+=(f2d[curadd[0]][curadd[1]],)
            curadd=(curadd[0]+stepr, curadd[1]+stepc) #Changing the value of the current address to the next address which we should check
            
    
        return path
    else:
        return "Invalid"
    

#Returns the rowstepcount and columnstepcount between the starting address and the ending address (NOT in a tuple)
#Possible return values are: 0,1 ; 0,-1 ; 1,0 ; -1,0 ; 1,1 ; 1,-1 ; -1,1 ; -1,-1 
def stepcount(add1, add2):
    if add1[0]==add2[0]:
        stepr=0
    else:
        stepr=(add2[0]-add1[0])//abs(add2[0]-add1[0])

    if add1[1]==add2[1]:
        stepc=0
    else:
        stepc=(add2[1]-add1[1])//abs(add2[1]-add1[1])

    return stepr, stepc


#Aim: to check if a move given by the user is valid
#Parameters: Starting address(2D Indexing)(tuple), Ending Address(2D Indexing)(tuple), 2 dimensional list 
#Return: True if the move is valid and False if the move is invalid.

def rookmove(add1, add2, f2d):  
    level=0
    #1st Level
    if add1[0]==add2[0]: #row numbers
        level+=1
    elif add1[1]==add2[1]: #Column Numbers
        level+=1
    else:
        return False

    #2nd Level
    pathpieces=piecesbetween(add1, add2, f2d)
    
    if pathpieces ==():
        level+=1
    elif len(pathpieces)==1 and (pathpieces[0][2], pathpieces[0][3])==add2 and sameteam(pathpieces[0], f2d[add1[0]][add1[1]])==False:
        level+=1

    if level==2:
        return True
    else:
        return False


#For a horse, we need not worry about whether there is a piece in between or not.
def hormove(add1, add2, f2d): 
    level=0
    #1st Level
    if (add1[0]==add2[0]+1 or add1[0]==add2[0]-1) and (add1[1]==add2[1]+2 or add1[1]==add2[1]-2):
        level+=1
    elif (add1[0]==add2[0]+2 or add1[0]==add2[0]-2) and (add1[1]==add2[1]+1 or add1[1]==add2[1]-1):
        level+=1
    else:
        return False
    
    #2nd Level
    if sameteam(f2d[add2[0]][add2[1]], f2d[add1[0]][add1[1]])==False:
        level+=1
    if level==2:
        return True
    else:
        return False


def bishmove(add1, add2, f2d):
    level=0
    #1st Level
    if abs(add1[0]-add2[0])==abs(add1[1]-add2[1]):
        level+=1
    else:
        return False

    #2nd Level
    pathpieces=piecesbetween(add1, add2, f2d)
    if pathpieces ==():
        level+=1
    elif len(pathpieces)==1 and (pathpieces[0][2], pathpieces[0][3])==add2 and sameteam(pathpieces[0], f2d[add1[0]][add1[1]])==False:
        level+=1

    if level==2:
        return True
    else:
        return False


def queenmove(add1, add2, f2d):
    level=0
    #1st Level
    if add1[0]==add2[0] or add1[1]==add2[1]:
        level+=1
    elif abs(add1[0]-add2[0])==abs(add1[1]-add2[1]):
        level+=1
    else:
        return False


    #2nd Level
    pathpieces=piecesbetween(add1, add2, f2d)
    if pathpieces ==():
        level+=1
    elif len(pathpieces)==1 and (pathpieces[0][2], pathpieces[0][3])==add2 and sameteam(pathpieces[0], f2d[add1[0]][add1[1]])==False:
        level+=1

    if level==2:
        return True
    else:
        return False


def kingmove(add1, add2, f2d):
    level=0
    #1st Level
    #(add1[0]==add2[0]+1 or add1[0]==add2[0]-1 or add1[0]==add2[0]) and (add1[1]==add2[1] or add1[1]==add2[1]-1 or add1[1]==add2[1]+1)
    if (add1[0]-add2[0])**2 + (add1[1]-add2[1])**2<=2:
        level+=1
    else :
        return False

    #2nd Level
    pathpieces=piecesbetween(add1, add2, f2d)
    if pathpieces ==():
        level+=1
    elif len(pathpieces)==1 and (pathpieces[0][2], pathpieces[0][3])==add2 and sameteam(pathpieces[0], f2d[add1[0]][add1[1]])==False:
        level+=1


    if level==2:
        return True
    else:
        return False


#Parameters: Two addresses are given as tuples, 2 dimensional list
#Will return True if castling is possible, False if not possible            
def castle(add1, add2, f2d):    
    if not(0<=add1[0]<=7 and 0<=add1[1]<=7 and 0<=add2[0]<=7 and 0<=add2[1]<=7):
        return (False, ((0,0), (0,0)), ((0,0), (0,0)))
    

    #Converting add2 to possible add of rook
    if add2[1] > add1[1]:
        add2 = (add2[0], add2[1] + 1)
    elif add2[1] < add1[1]:
        add2 = (add2[0], add2[1] - 2)
    
    #Getting the relevant pieces
    pc1=f2d[add1[0]][add1[1]]
    pc2=f2d[add2[0]][add2[1]]

    caslevel1=False
    if pc1[0]=="king" and pc2[0]=="rook":
        caslevel1=True
    
    logmessage.log("       Caslevel1: (King has been moved correctly for a castle) ", caslevel1)

    caslevel1_1=False
    if caslevel1==True:
        if abs(add1[1]-add2[1])==3:
            if f2d[add1[0]][pc2[3]-1]==["", "", 0, 0] and f2d[add1[0]][pc2[3]-2]==["", "", 0, 0]:
                caslevel1_1=True
        elif abs(add1[1]-add2[1])==4:
            if f2d[add1[0]][pc2[3]+1]==["", "", 0, 0] and f2d[add1[0]][pc2[3]+2]==["", "", 0, 0] and f2d[add1[0]][pc2[3]+3]==["", "", 0, 0] :
                caslevel1_1=True
    if caslevel1==True:
        logmessage.log("       Caslevel1_1: (Squares in between are empty) ", caslevel1_1)
    
    caslevel2=False
    if caslevel1_1==True and check((pc1[2], pc1[3]), f2d)[0]==False:
        caslevel2=True
    if caslevel1_1==True:
        logmessage.log("       Caslevel2: (Castling king is not facing a check) ", caslevel2)
    
    caslevel3=False
    if caslevel2==True and sameteam(pc1, pc2)==True and pc1[4]==False and pc2[4]==False and len(piecesbetween(add1, add2, f2d))==1:
        caslevel3=True
    if caslevel2==True:
        logmessage.log("       Caslevel3: (Both the pieces belong to the same team) ", caslevel3)
    
    caslevel4=False
    if caslevel3==True:

        clist2d=[]
        for i in f2d:
            temp=[]
            for j in i:
                temp.append(j.copy())
            clist2d.append(temp)
    
    
        if abs(add1[1]-add2[1])==3:
            validatemove((pc1[2], pc1[3]), (pc1[2], pc1[3]+1), clist2d)
            if check((pc1[2], pc1[3]+1), clist2d)[0]==False:
                caslevel4=True
                newkingadd=(pc1[2], pc1[3]+2)
                newrookadd=(pc2[2], pc2[3]-2)

        elif abs(add1[1]-add2[1])==4:
            validatemove((pc1[2], pc1[3]), (pc1[2], pc1[3]-1), clist2d)
            if check((pc1[2], pc1[3]-1), clist2d)[0]==False:
                caslevel4=True
                newkingadd=(pc1[2], pc1[3]-2)
                newrookadd=(pc2[2], pc2[3]+3)

    if caslevel4==True:
        castleinfo=(True, ((pc1[2], pc1[3]), newkingadd), ((pc2[2], pc2[3]), newrookadd))
        return (True, ((pc1[2], pc1[3]), newkingadd), ((pc2[2], pc2[3]), newrookadd)) #Castle is possible or not?, King's starting and ending add, rook's S and E add
    elif caslevel4==False:
        return (False, ((0,0), (0,0)), ((0,0), (0,0)))
        
                       
#Movement of the pawn is slightly complicated. Depending on whether it is black or white, it can only move in ONE direction. It can move CROSS only if something can be attacked.
#Parameters: Starting address[2D indexing], ending address[2D indexing], 2 dimensional list
#Return: if the move is straight and there is 'NO piece in the ending address' return True; if the move is cross there is a piece of the OPPOSITE team in the ending address return True
#Incorporated starting double move and En Passant also
#The returned tuple consists of 3 boolean values and 1 tuple: Is the move possible?, Is the moving pawn a possible en passant victim in the next move?, Is the moving pawn killing another pawn by en passant?, The address of the pawn which has to be killed.
def pawnmove(add1, add2, f2d):
    if f2d[add1[0]][add1[1]][1]=="*^": #White Checking
        if  add2[0]-add1[0]==-1: #For white, row should decrease.
            if add1[1]==add2[1]: #Checking if the column is the same
                if f2d[add2[0]][add2[1]][1]=="": #Checking if the ending address is empty
                    return (True, False, False, None)
                else:
                    return (False, False,False, None)
            elif abs(add2[1]-add1[1])==1: #Checking if the pawn has moved cross
                if sameteam(f2d[add1[0]][add1[1]], f2d[add2[0]][add2[1]])==False and f2d[add2[0]][add2[1]]!=["", "", 0, 0]: #Checking if the ending address is occupied by a black piece
                    return (True, False,False, None)
                elif f2d[add2[0]][add2[1]]==["", "", 0, 0] and f2d[add1[0]][add2[1]][0]=="pawn" and f2d[add1[0]][add2[1]][4]==True:
                    return (True, False, True, (add1[0],add2[1]))
                else:
                    return (False, False,False, None)

        elif add2[0]-add1[0]==-2 and add1[0]==6:
            if add1[1]==add2[1]: #Checking if the column is the same
                if f2d[add2[0]][add2[1]][1]=="": #Checking if the ending address is empty
                    return (True, True,False, None)
                else:
                    return (False, False,False, None)
            
        else:
            return (False, False, False, None)

    elif f2d[add1[0]][add1[1]][1]=="^": #Black Checking
        if  add2[0]-add1[0]==1: #For black, row should increase.
            if add1[1]==add2[1]: #Checking if the column is the same
                if f2d[add2[0]][add2[1]][1]=="": #Checking if the ending address is empty
                    return (True, False,False, None)
                else:
                    return (False, False,False, None)
            elif abs(add2[1]-add1[1])==1: #Checking if the pawn has moved cross
                if sameteam(f2d[add1[0]][add1[1]], f2d[add2[0]][add2[1]])==False and f2d[add2[0]][add2[1]]!=["", "", 0, 0]: #Checking if the ending address is occupied by a white piece
                    return (True, False,False, None)
                elif f2d[add2[0]][add2[1]]==["", "", 0, 0] and f2d[add1[0]][add2[1]][0]=="pawn" and f2d[add1[0]][add2[1]][4]==True:
                    return (True, False, True,(add1[0],add2[1]))
                else:
                    return (False, False,False, None)
        elif add2[0]-add1[0]==2 and add1[0]==1:
            if add1[1]==add2[1]: #Checking if the column is the same
                if f2d[add2[0]][add2[1]][1]=="": #Checking if the ending address is empty
                    return (True, True,False, None)
                else:
                    return (False, False,False, None)
        else:
            return (False, False,False, None)
    
    return (None, None,False, None)


#Parameters: First address, Second address, 2 dimensional list
#Function: Given that a piece CAN MOVE from the first address to the second address, extend return the addresses (tuples) of all the squares following the first address along the line(first add, second add) that are either free or occupied by a piece opposite to the piece present in the starting address.
#In short, it gives the reach of the piece present in the first address given that it can move from the first address to the second address.
def extend(add1, add2, f2d):
    r,c=add1[0], add1[1]
    if colour(f2d[r][c])=="white":
        for m in f2d:
            for n in m:
                if n[1]=="*$":
                    extendking=n #King of the piece which is being moved. We need to see if the king of the piece which is moving suffers a check or not
    elif colour(f2d[r][c])=="black":
        for m in f2d:
            for n in m:
                if n[1]=="$":
                    extendking=n
    stepr, stepc=stepcount(add1, add2)
    piece=f2d[add1[0]][add1[1]]
    rowcounter, colcounter=add2[0], add2[1]
    tup=()
    while True:
        if 0<=rowcounter<=7 and 0<=colcounter<=7:
            if sameteam(piece, f2d[rowcounter][colcounter])==False:
                templist2d=[]
                for l in f2d:
                    temp=[]
                    for k in l:
                        temp.append(k.copy())
                    templist2d.append(temp)
                validatemove((r,c), (rowcounter,colcounter), templist2d)
                if check((extendking[2], extendking[3]), templist2d)[0]==False:
                    tup+=((rowcounter, colcounter),)
                if colour(f2d[rowcounter][colcounter])=="white" or colour(f2d[rowcounter][colcounter])=="black":
                    break
            else:
                break
            rowcounter+=stepr
            colcounter+=stepc
        else:
            break  
    return tup


#Given an address and a 2 dimensional list, it returns the addresses of all the squares that the piece present in the starting address can go to as a TUPLE.
def legal(add,f2d):
    if colour(f2d[add[0]][add[1]])=="empty":
        return (False, ())
    
    global legaladdresses
    legaladdresses=()

    r,c=add[0], add[1]
    
    if colour(f2d[r][c])=="white":
        for m in f2d:
            for n in m:
                if n[1]=="*$":
                    king=n #King of the piece which is being moved. We need to see if the king of the piece which is moving suffers a check or not
    elif colour(f2d[r][c])=="black":
        for m in f2d:
            for n in m:
                if n[1]=="$":
                    king=n
    
    def aroundcheck(add, f2d, a1, a2, a3, a4, a5, a6, a7, a8):
        global legaladdresses
        r,c=add[0], add[1]
        pc=f2d[r][c][0]
        ru=cl=8
        if r>=1:
            ru=r-1
        if c>=1:
            cl=c-1
        
        around=[a1,a2,a3,a4,a5,a6,a7,a8]
        addresses=[(r, c+1), (ru, c+1), (ru, c), (ru, cl), (r, cl), (r+1, cl), (r+1, c), (r+1, c+1)]
        
        for i in range(8):
            if around[i]==False:
                addresses[i]=(None, None)

        
        for i,j in addresses:
            try:
                if i!=None:
                    templist2d=[]
                    for l in f2d:
                        temp=[]
                        for k in l:
                            temp.append(k.copy())
                        templist2d.append(temp)
                        
                    if pc=="pawn":
                        level1=pawnmove((r,c), (i,j), templist2d)[0] #Pawn attacking and moving has different rules.
                    else:
                        level1=not(sameteam(f2d[r][c], f2d[i][j])) #All other pieces have the same rules of attacking and moving

                    if level1!=True:
                        continue

                    validatemove((r,c), (i,j), templist2d)
                    
                    if colour(f2d[r][c])=="white":
                        for m in templist2d:
                            for n in m:
                                if n[1]=="*$":
                                    teamking=n #King of the piece which is being moved. We need to see if the king of the piece which is moving suffers a check or not
                    elif colour(f2d[r][c])=="black":
                        for m in templist2d:
                            for n in m:
                                if n[1]=="$":
                                    teamking=n

                    if check((teamking[2], teamking[3]), templist2d)[0]==False:
                        if pc=="king" or pc=="horse" or pc=="pawn":
                            legaladdresses+=((i,j),)
                        elif pc=="queen" or pc=="bishop" or pc=="rook":
                            if colour(f2d[i][j])=="empty":
                                for k in extend(add, (i,j), f2d):
                                    legaladdresses+=(k,)
                            else:
                                legaladdresses+=((i,j),)
                    
                    if pc=="pawn" and colour(f2d[i][j])=="empty":
                        stepr=i-r
                        nextr=i+stepr
                        templist2d=[]
                        for l in f2d:
                            temp=[]
                            for k in l:
                                temp.append(k.copy())
                            templist2d.append(temp)
                        validatemove((r,c), (nextr, j), templist2d)
                        
                        if pawnmove((r,c), (nextr, j), f2d)[0]==True:
                            if check((teamking[2], teamking[3]), templist2d)[0]==False:
                                legaladdresses+=((nextr, j),)
            except IndexError:
                pass

        if legaladdresses==():
            return (False, legaladdresses)
        else:
            return (True, legaladdresses)

    def aroundhorsecheck(add, f2d):
        global legaladdresses
        r=add[0]
        c=add[1]
        
        rowu=rowuu=coll=colll=8 #rowup, rowupup, columnleft, columnleftleft
        if r-1>=0:
            rowu=r-1 
        if r-2>=0:
            rowuu=r-2
        if c-1>=0:
            coll=c-1
        if c-2>=0:
            colll=c-2

        addresses=((rowu, c+2),(r+1, c+2),(rowuu, c+1),(r+2, c+1),(rowu, colll),(r+1, colll),(rowuu, coll),(r+2, coll))
        for i, j in addresses:
            try:               
                    
                templist2d=[]
                for l in f2d:
                    temp=[]
                    for k in l:
                        temp.append(k.copy())
                    templist2d.append(temp)

                level1=not(sameteam(f2d[r][c], f2d[i][j]))
                if level1!=True:
                        continue
                    
                validatemove((r,c), (i,j), templist2d)
                if colour(f2d[r][c])=="white":
                    for m in templist2d:
                        for n in m:
                            if n[1]=="*$":
                                teamking=n #King of the piece which is being moved. We need to see if the king of the piece which is moving suffers a check or not
                elif colour(f2d[r][c])=="black":
                    for m in templist2d:
                        for n in m:
                            if n[1]=="$":
                                teamking=n
                       
                if check((teamking[2], teamking[3]), templist2d)[0]==False:
                    legaladdresses+=((i,j),)
                                            
            except IndexError:
                pass
        
        if legaladdresses==():
            return (False, legaladdresses)
        else:
            return (True, legaladdresses)
        
    if check((king[2], king[3]), f2d)[0]==True and (f2d[r][c][0]=="rook" or f2d[r][c][0]=="bishop" or f2d[r][c][0]=="queen"):
        attpcs=check((king[2], king[3]), f2d)[1] #Attacking Pieces
        logmessage.log("Legal: Check=True: attpcs ", attpcs)
        
        for indattpc in attpcs: #Individual Attacking Piece
            rowf=indattpc[2] #Row number of the attacking piece
            colf=indattpc[3] #Column number of the attacking piece
            rowstep, colstep=stepcount((king[2], king[3]), (rowf, colf)) #Gives us the rowstep value and the colstep value to gradually move from the king's address to the attackers's address
            rowcounter=king[2]+rowstep
            colcounter=king[3]+colstep

            locations=()
            if indattpc[0]=="horse":
                locations+=(indattpc,)
            else:
                while True:
                    if rowcounter==rowf and colcounter==colf:
                        locations+=(indattpc,)
                        break
                    bwsquare=["", "", rowcounter, colcounter] #Between square
                    locations+=(bwsquare,)
                    rowcounter+=rowstep
                    colcounter+=colstep

            for indsquares in locations: #Individual squares in between the king and the attacking species
                templist2d=[]
                for l in f2d:
                    temp=[]
                    for k in l:
                        temp.append(k.copy())
                    templist2d.append(temp)

                checklevel1=False
                if f2d[r][c][0]=="rook":
                    if rookmove((r,c), (indsquares[2], indsquares[3]), templist2d)==True:
                        validatemove((r,c), (indsquares[2], indsquares[3]), templist2d)
                        checklevel1=True
                elif f2d[r][c][0]=="bishop":
                    if bishmove((r,c), (indsquares[2], indsquares[3]), templist2d)==True:
                        validatemove((r,c), (indsquares[2], indsquares[3]), templist2d)
                        checklevel1=True
                elif f2d[r][c][0]=="queen":
                    if queenmove((r,c), (indsquares[2], indsquares[3]), templist2d)==True:
                        validatemove((r,c), (indsquares[2], indsquares[3]), templist2d)
                        checklevel1=True

                if checklevel1==True:
                    if colour(f2d[r][c])=="white":
                        for m in templist2d:
                            for n in m:
                                if n[1]=="*$":
                                    teamking=n #King of the piece which is being moved. We need to see if the king of the piece which is moving suffers a check or not
                    elif colour(f2d[r][c])=="black":
                        for m in templist2d:
                            for n in m:
                                if n[1]=="$":
                                    teamking=n

                    if check((teamking[2], teamking[3]), templist2d)[0]==False:
                        legaladdresses+=((indsquares[2], indsquares[3]),)
    else:
        if f2d[r][c][0]=="king":
            return aroundcheck((r,c), f2d, True, True, True, True, True, True, True, True)
            
        elif f2d[r][c][0]=="queen":
            return aroundcheck((r,c), f2d, True, True, True, True, True, True, True, True)
                            
        elif f2d[r][c][0]=="rook":
            return aroundcheck((r,c), f2d, True, False, True, False, True, False, True, False)
            
        elif f2d[r][c][0]=="bishop":
            return aroundcheck((r,c), f2d, False, True, False, True, False, True, False, True)
            
        elif f2d[r][c][0]=="pawn":
            return aroundcheck((r,c), f2d, False, True, True, True,False,True,True,True)            
                
        elif f2d[r][c][0]=="horse":
            return aroundhorsecheck((r,c), f2d)    
    
    if legaladdresses==():
        return (False, legaladdresses)
    else:
        return (True, legaladdresses)


#Aim: Detection of a Check
#Parameters: king's position as a tuple, 2 dimensional list
#Result: if a check is possible, return (True, all the attacking pieces in a tuple). If not return (False, ())
def check(add,f2d):
    attack=()
    #Checking all pieces except Horse
    leftadd=(add[0], 0)
    left=piecesbetween(add, leftadd, f2d)

    rightadd=(add[0], 7)
    right=piecesbetween(add, rightadd, f2d)

    topadd=(0, add[1])
    top=piecesbetween(add, topadd, f2d)

    bottomadd=(7, add[1])
    bottom=piecesbetween(add, bottomadd, f2d)

    neadd=(add[0]-min(abs(add[0]-0), abs(7-add[1])),add[1]+min(abs(add[0]-0), abs(7-add[1])))  #North east - ne
    ne=piecesbetween(add, neadd, f2d)

    nwadd=(add[0]-min(abs(add[0]-0), abs(0-add[1])),add[1]-min(abs(add[0]-0), abs(0-add[1]))) #North west - nw
    nw=piecesbetween(add, nwadd, f2d)

    swadd=(add[0]+min(abs(add[0]-7), abs(0-add[1])),add[1]-min(abs(add[0]-7), abs(0-add[1]))) #South west - sw
    sw=piecesbetween(add, swadd, f2d)

    seadd=(add[0]+min(abs(add[0]-7), abs(7-add[1])),add[1]+min(abs(add[0]-7), abs(7-add[1]))) #South east - se
    se=piecesbetween(add, seadd, f2d)

    alldir=[left, right, top, bottom, ne, nw, se, sw]
    
    count=0
    for i in alldir:
        if i==():
            pass
        else:
            if i[0][0]=="horse":
                pass
            else:
                if sameteam(i[0], f2d[add[0]][add[1]])==False:
                    if (i[0][0]=="rook" or i[0][0]=="queen") and count in range(4):
                        attack+=(i[0],)
                        
                    elif (i[0][0]=="bishop" or i[0][0]=="queen") and count in (4,5,6,7):
                        attack+=(i[0],)
                    
                    elif i[0][0]=="pawn" and ((add[0]-i[0][2])**2 + (add[1]-i[0][3])**2)==2:
            
                        if i[0][1][0]=="*" and count in (6,7):
                            attack+=(i[0],)
                        
                        elif i[0][1][0]!="*" and count in (4,5):
                            attack+=(i[0],)
                    elif i[0][0]=="king" and (i[0][2]-add[0])**2 + (i[0][3]-add[1])**2<=2:
                        return (True, (i[0],))
        count+=1
        
    #Checking Horse   
    r=add[0]
    c=add[1]
    
    rowu=rowuu=coll=colll=8 #rowup, rowupup, columnleft, columnleftleft
    if r-1>=0:
        rowu=r-1 
    if r-2>=0:
        rowuu=r-2
    if c-1>=0:
        coll=c-1
    if c-2>=0:
        colll=c-2

    addresses=((rowu, c+2),(r+1, c+2),(rowuu, c+1),(r+2, c+1),(rowu, colll),(r+1, colll),(rowuu, coll),(r+2, coll))
    for tup in addresses:
        try:
            if f2d[tup[0]][tup[1]][0]=="horse" and sameteam(f2d[tup[0]][tup[1]], f2d[r][c])==False:
                attack+=(f2d[tup[0]][tup[1]],)
        except IndexError:
            pass
          
     
    if attack==():
        return (False, attack)
    else:
        return (True, attack)
        

#Aim: [Underlying aim is to detect a checkmate] Given an address and its status(empty or non-empty), being able to detect whether any piece of the SPECIFIED colour can enter the address either by just occupying or attacking
#Parameters: address(tuple), empty=True or False, clr=what is the colour of the piece you are looking for to occupy the given address, 2 dimensional list
#Note: Either of the kings cannot be considered for moving into the required square. 
#Return: if some piece satisfying the GIVEN conditions is present, return (True, pieces in a tuple), If ot, return (False, ())
def capture(add, empty, clr, f2d):
    attack=()
    leftadd=(add[0], 0)
    left=piecesbetween(add, leftadd, f2d)

    rightadd=(add[0], 7)
    right=piecesbetween(add, rightadd, f2d)

    topadd=(0, add[1])
    top=piecesbetween(add, topadd, f2d)

    bottomadd=(7, add[1])
    bottom=piecesbetween(add, bottomadd, f2d)

    neadd=(add[0]-min(abs(add[0]-0), abs(7-add[1])),add[1]+min(abs(add[0]-0), abs(7-add[1])))  #North east - ne
    ne=piecesbetween(add, neadd, f2d)

    nwadd=(add[0]-min(abs(add[0]-0), abs(0-add[1])),add[1]-min(abs(add[0]-0), abs(0-add[1]))) #North west - nw
    nw=piecesbetween(add, nwadd, f2d)

    swadd=(add[0]+min(abs(add[0]-7), abs(0-add[1])),add[1]-min(abs(add[0]-7), abs(0-add[1]))) #South west - sw
    sw=piecesbetween(add, swadd, f2d)

    seadd=(add[0]+min(abs(add[0]-7), abs(7-add[1])),add[1]+min(abs(add[0]-7), abs(7-add[1]))) #South east - se
    se=piecesbetween(add, seadd, f2d)

    alldir=[left, right, top, bottom, ne, nw, se, sw]
    
    count=0
    for i in alldir:
        if i==():
            pass
        else:
            if i[0][0]=="horse":
                pass
            else:
                if colour(i[0])==clr:
                    if (i[0][0]=="rook" or i[0][0]=="queen") and count in range(4):
                        attack+=(i[0],)
                        
                    elif (i[0][0]=="bishop" or i[0][0]=="queen") and count in (4,5,6,7):
                        attack+=(i[0],)
                    
                    elif i[0][0]=="pawn":
                        if empty==True and count in (2,3):
                            if clr=="black" and (add[0]-i[0][2]==1 or (add[0]-i[0][2]==2 and i[0][2]==1)):
                                attack+=(i[0],)
                            elif clr=="white" and (add[0]-i[0][2]==-1 or (add[0]-i[0][2]==-2 and i[0][2]==6)):
                                attack+=(i[0],)    
                        elif empty==False:
                            if clr=="black" and count in (4,5) and ((add[0]-i[0][2])**2 + (add[1]-i[0][3])**2 ==2):
                                attack+=(i[0],)
                            elif clr=="white" and count in (6,7) and ((add[0]-i[0][2])**2 + (add[1]-i[0][3])**2 ==2):
                                attack+=(i[0],)
                            
        count+=1
        
    #Checking Horse   
    r=add[0]
    c=add[1]
    
    rowu=rowuu=coll=colll=8 #rowup, rowupup, columnleft, columnleftleft
    if r-1>=0:
        rowu=r-1 
    if r-2>=0:
        rowuu=r-2
    if c-1>=0:
        coll=c-1
    if c-2>=0:
        colll=c-2


    addresses=((rowu, c+2),(r+1, c+2),(rowuu, c+1),(r+2, c+1),(rowu, colll),(r+1, colll),(rowuu, coll),(r+2, coll))
    for tup in addresses:
        try:
            if f2d[tup[0]][tup[1]][0]=="horse" and colour(f2d[tup[0]][tup[1]])==clr:
                attack+=(f2d[tup[0]][tup[1]],)
        except IndexError:
            pass
    
    if attack==():
        return (False, attack)
    else:
        return (True, attack)


#Aim: Detecting a Checkmate
#Parameters: Address of the king for whom you would like to validate for checkmate(tuple), 2 dimensional list
#Return: True if it is a checkmate and return False if it is not a checkmate.
def checkmate(add, f2d):
    attack=check(add,f2d)[1]
    if attack==():
        return False
    
    logmessage.log("\nCHECK!")
    logmessage.log("Pieces attacking the king:", attack)
    oppclr=oppcolour(colour(f2d[add[0]][add[1]]))  #The colour opposite to the king's colour which the king can attack
    kingclr=colour(f2d[add[0]][add[1]])
    logmessage.log("Attacked King colour: ", kingclr)
    logmessage.log("Opposite King Colour: ", oppclr)
    #Checking whether the king can move to a SAFE square around it either by just moving or by attacking another piece
    r,c=add[0], add[1]
    ru=8
    cl=8
    if r-1>=0:
        ru=r-1
    if c-1>=0:
        cl=c-1

    addresses=((r,c+1), (ru, c+1) ,(ru, c) ,(ru, cl) ,(r, cl) ,(r+1, cl) ,(r+1, c) ,(r+1, c+1))
    logmessage.log(addresses)
    for tup in addresses:
        
        testf2d=[]
        for i in f2d:
            temp=[]
            for j in i:
                temp.append(j.copy())
            testf2d.append(temp)
        
        try:
            if colour(testf2d[tup[0]][tup[1]])=="empty" or colour(testf2d[tup[0]][tup[1]])==oppclr:
                validatemove((r,c), tup, testf2d)
                logmessage.log("Pieces which can capture the king if it moves to the given adjacent square: ", tup, capture((tup[0], tup[1]), False, oppclr, testf2d))
                capturecheck=True
                if kingclr=="white":
                    #rok and cok-row of opposite king and column of opposite king
                    for i in testf2d:
                        for j in i:
                            if j[1]=="$":
                                rok, cok=j[2], j[3]
                    
                    if (rok-tup[0])**2 + (cok-tup[1])**2<=2:
                        capturecheck=False
                        
                elif kingclr=="black":
                    #rok and cok-row of opposite king and column of opposite king
                    for i in testf2d:
                        for j in i:
                            if j[1]=="*$":
                                rok, cok=j[2], j[3]
                    
                    if (rok-tup[0])**2 + (cok-tup[1])**2<=2:
                        capturecheck=False
                        
                if capturecheck==True and capture((tup[0], tup[1]), False, oppclr, testf2d)[0]==False:
                    return False
        
        except IndexError:
            pass
    

    if len(attack)>=2:
        #If there are multiple pieces attacking the king, the king has no option but to move simply or by attacking a piece.(This has already been validated in the beginning of this function)
        pass
    else:
        if attack[0][0]=="horse":
            #If there is a horse attacking a king, the king has no option but to move simply or by attacking a piece. Or the horse which is attacking can be killed.(This has already been validated in the beginning of this function)
            if capture((attack[0][2], attack[0][3]), False, kingclr,f2d)[0]==True:
                for i in capture((attack[0][2], attack[0][3]), False, kingclr,f2d)[1]:

                    #duplicate f2
                    dupf2d=[]
                    for k in f2d:
                        temp=[]
                        for j in k:
                            temp.append(j.copy())
                        dupf2d.append(temp)
                    
                            
                    validatemove((i[2], i[3]),(attack[0][2],attack[0][3]), dupf2d)
                    if check((r,c), dupf2d)[0]==False:
                        return False
        else:
            #If only one piece is attacking a king, the king can move, attack or some piece from the king's team can come in between and block OR some piece of the king's team can kill the piece giving a check
            rowf=attack[0][2] #Row number of the attacking piece
            colf=attack[0][3] #Column number of the attacking piece
            rowstep, colstep=stepcount((r,c), (rowf, colf)) #Gives us the rowstep value and the colstep value to gradually move from the king's address to the attackers's address
            rowcounter=r+rowstep
            colcounter=c+colstep
            success=False
            while success==False:
                if rowcounter==rowf and colcounter==colf:
                    success=True
                    if capture((rowcounter, colcounter), False, kingclr, f2d)[0]==True:
                        logmessage.log("Pieces which can attack the attacking piece: ",(rowcounter, colcounter), capture((rowcounter, colcounter), False, kingclr, f2d))
                        for i in capture((rowcounter, colcounter), False, kingclr, f2d)[1]:

                            #duplicate f2d
                            dupf2d=[]
                            for k in f2d:
                                temp=[]
                                for j in k:
                                    temp.append(j.copy())
                                dupf2d.append(temp)
                                
                            validatemove((i[2], i[3]),(rowf,colf), dupf2d)
                            if check((r,c), dupf2d)[0]==False:
                                return False
                else:
                    if capture((rowcounter, colcounter), True, kingclr, f2d)[0]==True:
                        logmessage.log("Pieces which can block the attacking piece: ",(rowcounter, colcounter) ,capture((rowcounter, colcounter), True, kingclr, f2d))
                        for i in capture((rowcounter, colcounter), True, kingclr, f2d)[1]:

                            #duplicate f2d
                            dupf2d=[]
                            for k in f2d:
                                temp=[]
                                for j in k:
                                    temp.append(j.copy())
                                dupf2d.append(temp)
                            validatemove((i[2], i[3]),(rowcounter,colcounter), dupf2d)
                            if check((r,c), dupf2d)[0]==False:
                                return False

                rowcounter+=rowstep
                colcounter+=colstep     
                           
    return True


#Aim: Detecting a Stalemate
#Parameters: 2 dimensional list, Is any king under check?
#Return: True if it is a stalemate and return False if it is not a stalemate.
def stalemate(f2d, checkval):
    #Stalemate Checking
    if checkval==True:
        return False
    
    for i in f2d:
        for j in i:
            if chance==colour(j) and legal((j[2], j[3]), f2d)[0]==True:
                return False

    return True


#The main function which is called by the display subsection of the program. This functions unifies all the functions present in Logic.py
#Return a long tuple containing all the information which the display subsection of the program would need.
#Returns: (Validity of Move, starting address, ending address, is it a check?, is it a checkmate?, is pawnpromotion possible? , Is castling possible?, are any legal moves possible for the piece present in the starting address? ,Possible legal addresses as a tuple)
def gameprocessing(add1, add2, update=False): #Starting address, Ending address
    #list2d ==> Live Board
    #newlist2d ==> To be used for checks and checkmates
    global chance, list2d, list2d_start_of_current_move, enpassant_possible, enpassant_possiblevictim
    
    enpassantcapture=False #WIll be changed to True if a pawn is en passant capturing another pawn in this move. False is a default value
    enpassant_killedpawn_add=None

    if add2==(None, None):
        return (False, add1, add2, False, False, False, False, legal(add1, list2d)[0],legal(add1, list2d)[1], False, None, False)
    
    if add1==add2:
        return (False, add1, add2, False, False, False, False, legal(add1, list2d)[0],legal(add1, list2d)[1], False, None, False)
    
    newlist2d=[]
    for i in list2d:
        temp=[]
        for j in i:
            temp.append(j.copy())
        newlist2d.append(temp)
    
    list2d_start_of_current_move = []
    for i in list2d:
        temp=[]
        for j in i:
            temp.append(j.copy())
        list2d_start_of_current_move.append(temp)
                    
                
    pc=list2d[add1[0]][add1[1]] #piece - pc
    logmessage.log("")
    logmessage.log("Chance: ", chance)

    level1=False
    if colour(pc)==chance:
        level1=True

    logmessage.log("Level1: (The correct player is playing) ", level1)

    level2=False
    if level1==True:
        if pc[0]=="rook" and rookmove(add1, add2, list2d)==True:
            level2=True
        elif pc[0]=="horse" and hormove(add1, add2, list2d)==True:
            level2=True
        elif pc[0]=="bishop" and bishmove(add1, add2, list2d)==True:
            level2=True
        elif pc[0]=="queen" and queenmove(add1, add2, list2d)==True:
            level2=True
        elif pc[0]=="king" and kingmove(add1, add2, list2d)==True:
            level2=True
        elif pc[0]=="pawn" and pawnmove(add1, add2, list2d)[0]==True:
            enpassantcapture=pawnmove(add1, add2, list2d)[2]
            enpassant_killedpawn_add=pawnmove(add1, add2, list2d)[3]
            level2=True
    if level1==True:
        logmessage.log("Level2: (The selected piece is CAPABLE of moving to the specified location) ", level2)
    
    level2alter=False #Alternate level2 incorporating castling
    if level1==True:
        if level2 == False:
            try:
                castleinfo=castle(add1, add2, list2d)
                if castleinfo[0]==True:
                    level2alter=True
            except:
                pass
    if level2==True:
        logmessage.log("Level2alter: (Alternate Level2) (Castling is Possible) ", level2alter)

    #Changing newlist2d to use it for check and checkmate
    if level2==True:            
        validatemove(add1, add2, newlist2d)
    elif level2alter==True:
        #Converting the end row, col click to rook square row, col
        if add2[1] > add1[1]:
            add2 = (add2[0], add2[1] + 1)
        elif add2[1] < add1[1]:
            add2 = (add2[0], add2[1] - 2)

        validatemove(castleinfo[1][0], castleinfo[1][1], newlist2d)
        validatemove(castleinfo[2][0], castleinfo[2][1], newlist2d)
        
    for i in newlist2d:
        for j in i:
            if j[1]=="*$":
                newwhking=j
            elif j[1]=="$":
                newblking=j
                        
    level3=False
    if level2==True or level2alter==True:
        if chance=="white":
            if check((newwhking[2], newwhking[3]),newlist2d)[0]==False:
                level3=True

        if chance=="black":
            if check((newblking[2], newblking[3]), newlist2d)[0]==False:
                level3=True
    if level2alter==True:
        logmessage.log("Level3: (Player's king is safe after the move) ", level3)
    
    level4=False
    if level3==True:                    
        if ((newwhking[2]-newblking[2])**2 + (newwhking[3]-newblking[3])**2 >2):
            level4=True
    if level3==True:
        logmessage.log("Level4: (Kings are NOT too close) ", level4)
    
    
    if level4==True:
        #Incorporating En Passant: Making changes to the pawn's detail list and changing the value of enpassant_possible
        if enpassant_possible==True: #This statement can be passed only if pawnmove(add1, add2, list2d)[1] was passed in the previous move
            enpassant_possible=False
            enpassant_possiblevictim[4]=False 
            enpassant_possiblevictim=[None, None]
            del enpassant_possiblevictim
        if pawnmove(add1, add2, list2d)[1]==True:
            pc[4]=True
            enpassant_possiblevictim=pc #The pawn which is susceptible to an enpassant capture in the next move
            enpassant_possible=True #An en passant capture is possible in the next move
        

        if level2==True:
            if pc[0]=="king": #Indicating that the king has started moving
                pc[4]=True
            elif pc[0]=="rook":# Indicating that the rook has started moving
                pc[4]=True
            piece_at_endinglocation=list2d[add2[0]][add2[1]]
            move(add1, add2) 
            if enpassantcapture==True:
                piece_at_victimlocation = list2d[enpassant_killedpawn_add[0]][enpassant_killedpawn_add[1]]
                list2d[enpassant_killedpawn_add[0]][enpassant_killedpawn_add[1]]=emp
                
        elif level2alter==True:
            list2d[add1[0]][add1[1]][4]=True
            list2d[add2[0]][add2[1]][4]=True
            move(castleinfo[1][0], castleinfo[1][1])
            move(castleinfo[2][0], castleinfo[2][1])
        

        #Checking for Pawn Promotion: The move has already been validated
        if chance=="white":
            pawnprom=False
            if pc[0]=="pawn" and pc[2]==0:
                pawnprom=True
        if chance=="black":
            pawnprom=False
            if pc[0]=="pawn" and pc[2]==7:
                pawnprom=True
    

        if chance=="white":
            checkval=check((blking[2], blking[3]), list2d)[0]
            checkmateval=checkmate((blking[2], blking[3]), list2d)
            chance="black"
            
        elif chance=="black":
            checkval=check((whking[2], whking[3]), list2d)[0]
            checkmateval=checkmate((whking[2], whking[3]), list2d)
            chance="white"


        logmessage.log("\n")
        logmessage.log(list2d, "\n")
        if logmessage.DEBUG==True:
            displaylist(list2d)
            for i in list2d:
                for j in i:
                    print(j, end=" ")
                print("\n\n")
        
        stalemateval = stalemate(list2d, checkval)
        
        #Adding the move made to "List_of_Moves"
        if level2alter==True: #Castling
            List_of_Moves.append(("Castling", castleinfo[1], castleinfo[2]))
        elif enpassantcapture==True: #Enpassant capture
            List_of_Moves.append(("Enpassant", add1, add2, enpassant_killedpawn_add, piece_at_victimlocation))
        else:
            List_of_Moves.append((add1, add2, piece_at_endinglocation))
    
        #print('in logic: ',List_of_Moves , '\n')
        if level2alter==True:#Level2alter is for castling
            return (True, castleinfo[1], castleinfo[2], checkval, checkmateval, pawnprom, castleinfo[0], legal(add1, list2d)[0],legal(add1, list2d)[1], False, None, stalemateval)
        elif level2==True:
            return (True, add1, add2, checkval, checkmateval, pawnprom, False, legal(add1, list2d)[0],legal(add1, list2d)[1], enpassantcapture, enpassant_killedpawn_add, stalemateval)
    
    elif level4==False:
        return(False, add1, add2, False, False, False, False, legal(add1, list2d)[0], legal(add1, list2d)[1], False, None, False)


#Given the address where the pawn is present and the identity of the piece to which it has to be converted to, the required changes in list2d are made. 
def pawnpromotion(add, identity):#Address of the pawn as a tuple, identity-what should the pawn be changed to? (queen, rook, horse, bishop)

    global list2d
    pc=list2d[add[0]][add[1]]
    if identity==None:
        return None
    
    if colour(pc)=="white":
        if identity=="queen":
            sym="*Q"
        elif identity=="bishop":
            sym="*A"
        elif identity=="horse":
            sym="*/>"
        elif identity=="rook":
            sym="*]["
    elif colour(pc)=="black":
        if identity=="queen":
            sym="Q"
        elif identity=="bishop":
            sym="A"
        elif identity=="horse":
            sym="/>"
        elif identity=="rook":
            sym="]["
    if identity=="rook":
        globals()['{clr[0:2]}{identity}pp{pawnnum}']=[identity, sym, pc[2], pc[3], True]
        List_of_Moves.append(("Pawnpromotion", add, [identity, sym, pc[2], pc[3], True])) 
    else:   
        globals()['{clr[0:2]}{identity}pp{pawnnum}']=[identity, sym, pc[2], pc[3]]
        List_of_Moves.append(("Pawnpromotion", add, [identity, sym, pc[2], pc[3]]))
    list2d[add[0]][add[1]]=globals()['{clr[0:2]}{identity}pp{pawnnum}']


#Parameter: Possible winner
#Return: 0 or 1
def winner_on_flag(clr):
    alive_pieces = []
    for row in list2d:
        for piece in row:
            if colour(piece) == clr:
                alive_pieces.append(piece[0])
    
    if len(alive_pieces) == 1 and alive_pieces == ['king']:
        return 0
    elif len(alive_pieces) == 2:
        alive_pieces.remove('king')
        if alive_pieces[0] in ('bishop', 'horse'):
            return 0
        else:
            return 1
    else:
        return 1


def get_game_situation(f2d):
    checkv, checkmatev, stalematev = False, False, False
    for row in f2d:
        for piece in row:
            if piece[1]=="*$":
                whkadd = tuple(piece[2:4])
                checkv = check(whkadd, f2d)[0]
                if checkv:
                    checkmatev = checkmate(whkadd, f2d)
                    if not checkv:
                        stalematev = stalemate(f2d, False)
                    return checkv , checkmatev , stalematev
            elif piece[1]=="$":
                blkadd = tuple(piece[2:4])
                checkv = check(blkadd, f2d)[0]
                if checkv:
                    checkmatev = checkmate(blkadd, f2d)
                    if not checkv:
                        stalematev = stalemate(f2d, False)
                    return checkv , checkmatev , stalematev
    
    return checkv, checkmatev, stalematev

