#The purpose of test_chess.py is to test multiple CHECKMATE configurations all at once using pytest.
import pytest
from logic import *
iemp=["", "", 0, 0]  

#The reason we use @pytest.fixture() is because we need to INITIALISE the 2dlist AND all the pieces every time we go to a new test case. In a new test case, we can't use the values of the 2dlist and the pieces which we finally arrived at in the previous testcase.
#Each test case is independent.
#NOTE: In this testing file, the variable names which we use for the 2-dimensional list and the pieces are different.


@pytest.fixture()
def il(): #Initialisng the 2d List
    iwhrook1=["rook", "*][", 7, 0] 
    iwhrook2=["rook", "*][", 7, 7] 
    iwhhor1=["horse", "*/>", 7, 1]
    iwhhor2=["horse", "*/>", 7, 6]
    iwhbish1=["bishop", "*A", 7, 2]
    iwhbish2=["bishop", "*A", 7, 5]
    iwhqueen=["queen", "*Q", 7, 3]
    iwhking=["king", "*$", 7, 4]
    iP1=["pawn", "*^", 6, 0]
    iP2=["pawn", "*^", 6, 1]
    iP3=["pawn", "*^", 6, 2]
    iP4=["pawn", "*^", 6, 3]
    iP5=["pawn", "*^", 6, 4]
    iP6=["pawn", "*^", 6, 5]
    iP7=["pawn", "*^", 6, 6]
    iP8=["pawn", "*^", 6, 7]

    #Creating Black pieces
    iblrook1=["rook", "][", 0, 0] 
    iblrook2=["rook", "][", 0, 7] 
    iblhor1=["horse", "/>", 0, 1]
    iblhor2=["horse", "/>", 0, 6]
    iblbish1=["bishop", "A", 0, 2]
    iblbish2=["bishop", "A", 0, 5]
    iblqueen=["queen", "Q", 0, 3]
    iblking=["king", "$", 0, 4]
    ip1=["pawn", "^", 1, 0]
    ip2=["pawn", "^", 1, 1]
    ip3=["pawn", "^", 1, 2]
    ip4=["pawn", "^", 1, 3]
    ip5=["pawn", "^", 1, 4]
    ip6=["pawn", "^", 1, 5]
    ip7=["pawn", "^", 1, 6]
    ip8=["pawn", "^", 1, 7]

    return [[iblrook1, iblhor1, iblbish1, iblqueen, iblking, iblbish2, iblhor2, iblrook2],[ip1, ip2, ip3, ip4, ip5, ip6, ip7, ip8],[iemp]*8,[iemp]*8,[iemp]*8,[iemp]*8,[iP1, iP2, iP3, iP4, iP5, iP6, iP7, iP8],[iwhrook1, iwhhor1, iwhbish1, iwhqueen, iwhking, iwhbish2, iwhhor2, iwhrook2]]

#By using this function, the value at the starting address will be changed to iemp. The value at the ending address will be changed to the piece which was originally at the starting address. And, the rownumber and the columnnumber of the piece which is moving is changed.
def tmove(tl, add1, add2):
    tl[add2[0]][add2[1]]=tl[add1[0]][add1[1]] #Ending address is filled
    tl[add1[0]][add1[1]]=iemp #Starting address is iemptied
    tl[add2[0]][add2[1]][2]=add2[0]
    tl[add2[0]][add2[1]][3]=add2[1]
    




###Sample Code for Testing
##def test_check_*(il):  #* should be filled with the name of the checkmate or if the checkmate has no name, give some numbers along with your name (i.e, Guru, Subham)
##    iemp=iemp=["", "", 0, 0]
##    tmove(il, * , *) #*-Starting address and ending address as a tuple, 
##    tmove(il, *, *)
##        .
##        .
##        .
##    
##    displaylist(il) #In case the test case is failed, this command will display the 2d list so that you can CROSSCHECK if the configuration is same as the reference configuration. 
##    add = *  #*-King's location as a tuple 
##    result=checkmate(add, il)
##    assert result==True


def test_check1(il):
    displaylist(il)
    add = (0,4)
    result = checkmate(add, il)
    assert result == False #I have given False because this configuration is actually not a checkmate


def test_check2(il):
    displaylist(il)
    tmove(il, (6,4), (4,4))
    tmove(il, (1,4), (3,4))
    tmove(il, (7,5), (4,2))
    tmove(il, (1,5), (2,5))
    tmove(il, (7,3), (3,7))
    tmove(il, (0,2), (5,5))
    tmove(il, (7,2), (4,1))
    tmove(il, (1,6), (3,6))

    displaylist(il)
    add = (0,4)
    result = checkmate(add, il)
    assert result == False


def test_check_foolsmate(il):
    tmove(il, (6,6), (4,6))
    tmove(il, (6,5), (5,5))
    tmove(il, (1,4), (3,4))
    tmove(il, (0,3), (4,7))
    displaylist(il)
    add=(7,4)
    result=checkmate(add, il)
    assert result==True


def test_check_scholarsmate(il):
    tmove(il,(6,4), (4,4))
    tmove(il,(1,4), (3,4))
    tmove(il,(7,3), (1,5))
    tmove(il, (0,6), (2,5))
    tmove(il, (7,5), (4,2))
    tmove(il, (0,5), (3,2))
    displaylist(il)
    add=(0,4)
    result=checkmate(add,il)
    assert result==True


def test_check_smotheredmate(il):
    iemp=["", "", 0, 0]
    tmove(il, (1,4), (3,4))
    tmove(il, (6,4), (4,4))
    tmove(il, (7,1), (5,2))
    tmove(il, (7,6), (6,4))
    tmove(il, (0,1), (5,5))
    tmove(il, (6,6), (5,6))
    displaylist(il)
    add=(7,4)
    result=checkmate(add, il)
    assert result==True


def test_check_hippopotamusmate(il):
    tmove(il, (1,4), (3,4))
    tmove(il, (6,4), (4,4))
    tmove(il, (7,1), (5,2))
    tmove(il, (7,6), (6,4))
    tmove(il, (0,1), (5,5))
    tmove(il, (0,3), (3,6))
    tmove(il, (7,2), (3,6))
    tmove(il, (6,6), (5,6))
    il[6][3]=iemp
    displaylist(il)
    add=(7,4)
    result=checkmate(add, il)
    assert result==True


def test_check_blackburneshillingmate(il):
    tmove(il, (7,5), (6,4))
    tmove(il, (7,6), (1,5))
    tmove(il, (7,7), (7,5))
    tmove(il, (0,3), (4,4))
    tmove(il, (0,1), (5,5))
    displaylist(il)
    il[1][4]=iemp
    il[6][6]=iemp
    add=(7,4)
    result=checkmate(add, il)
    assert result==True


def test_check_legallsmate(il):
    tmove(il, (1,6), (2,6))
    tmove(il, (7,1), (3,3))
    tmove(il, (7,6), (3,4))
    tmove(il,(6,4), (4,4))
    tmove(il, (0,2), (7,3))
    tmove(il, (1,3), (2,3))
    tmove(il, (0,4), (1,4))
    tmove(il, (7,5), (1,5))
    displaylist(il)
    add=(1,4)
    result=checkmate(add, il)
    assert result==True


def test_check_smotheredmatequeenspawn(il):
    tmove(il, (0,1), (2,2))
    tmove(il, (0,3), (1,4))
    tmove(il, (0,6), (5,3))
    il[0][5]=iemp
    tmove(il, (7,1), (6,3))
    tmove(il, (7,6), (5,5))
    tmove(il, (6,0), (4,1))
    tmove(il, (6,2), (4,2))
    tmove(il, (7,2), (4,5))

    displaylist(il)
    add=(7,4)
    result=checkmate(add, il)
    assert result==True


def test_check_seacadetmate(il):
    tmove(il, (1,3), (2,3))
    tmove(il, (7,1), (3,3))
    tmove(il, (7,6), (3,4))
    tmove(il, (0,4), (1,4))
    tmove(il, (7,5), (1,5))
    tmove(il, (7,4), (7,6))
    tmove(il, (7,7), (7,5))
    tmove(il, (0,2), (7,3))
    il[6][2]=iemp
    il[6][3]=iemp
    tmove(il, (6,4), (4,4))
    il[0][1]=iemp

    displaylist(il)
    add=(1,4)
    result=checkmate(add, il)
    assert result==True


def test_check_twopawnmate(il):
    il=[[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp] ]

    iblking=["king", "$", 0, 4]
    iwhking=["king", "*$", 2, 4]
    iP4=["pawn", "*^", 1, 3]
    iP5=["pawn", "*^", 1, 4]

    il[0][4] = iblking
    il[1][3] = iP4
    il[1][4] = iP5
    il[2][4] = iwhking
        
    displaylist(il)
    add = (0, 4)
    result = checkmate(add, il)
    assert result==True


def test_check_diagonalmate(il):
    il=[[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp] ]

    iblrook1=["rook", "][", 0, 0]
    iblrook2=["rook", "][", 0, 5]
    iblking=["king", "$", 0, 6]
    iwhqueen=["queen", "*Q", 1, 6]
    iwhking=["king", "*$", 7, 6]
    iP2=["pawn", "*^", 5, 1]
    iwhbish1=["bishop", "*A", 7, 0]
    iwhrook1=["rook", "*][", 7, 5]
    
    ip1=["pawn", "^", 1, 0]
    ip2=["pawn", "^", 1, 1]
    ip3=["pawn", "^", 1, 2]
    ip6=["pawn", "^", 1, 5]
    ip7=["pawn", "^", 1, 6]
    iP1=["pawn", "*^", 6, 0]
    iP6=["pawn", "*^", 6, 5]
    iP7=["pawn", "*^", 6, 6]
    iP8=["pawn", "*^", 6, 7]
    il[0][0] = iblrook1
    il[1][0] = ip1
    il[1][1] = ip2
    il[1][2] = ip3
    il[0][5] = iblrook2
    il[0][6] = iblking
    il[1][5] = ip6
    il[1][6] = ip7
    il[1][6] = iwhqueen
    il[6][0] = iP1    
    il[5][1] = iP2
    il[6][5] = iP6
    il[6][6] = iP7
    il[6][7] = iP8
    il[7][0] = iwhbish1
    il[7][5] = iwhrook1
    il[7][6] = iwhking

    displaylist(il)
    add = (0, 6)
    result = checkmate(add, il)
    assert result==True


def test_check_fianchettomate(il):
    tmove(il, (7,2), (2,5))
    tmove(il, (6,1), (5,1))
    tmove(il, (7,7), (7,5))
    tmove(il, (7,4), (7,6))
    tmove(il, (7,1), (2,7))
    tmove(il, (0,7), (0,5))
    tmove(il, (0,4), (0,6))
    tmove(il, (1,6), (2,6))

    il[0][1] = il[0][2] = il[0][3] = il[1][3] = il[1][4] = iemp
    il[6][2] = il[6][3] = il[6][4] = il[7][0] = il[7][3] = iemp

    displaylist(il)
    add = (0, 6)
    result = checkmate(add, il)
    assert result==True


def test_check_subhamsriramgame1(il):
    il=[[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp],[iemp,iemp, iemp, iemp, iemp, iemp, iemp, iemp] ]
    iwhking=["king", "*$", 7, 5, True]
    iblking=["king", "$", 1, 2]
    iblrook1=["rook", "][", 7,0]
    iblqueen=["queen", "Q", 6, 1]
    iblbish2=["bishop", "A", 3, 4]
    il[7][5]=iwhking
    il[1][2]=iblking
    il[7][0]=iblrook1
    il[6][1]=iblqueen
    il[3][4]=iblbish2

    displaylist(il)
    add = (7,5)
    print(checkmate(add, il))
    result = checkmate(add, il)
    assert result==True
