#Creating Chess Pieces
pcdriftx={"rook": -56, "horse":-48, "bishop": -50, "queen": -48, "king":-48, "pawn":-45}
pcdrifty={"rook": -55, "horse":-40, "bishop": -47, "queen": -45, "king":-42, "pawn":-42}

tiltedcoord={"rook": (), "horse": (), "bishop": (), "queen": (), "king": (), "pawn": ()}
COORD={"rook": (), "horse": (), "bishop": (), "queen": (), "king": (), "pawn": ()}
pieces=("rook", "horse", "bishop", "queen", "king", "pawn")

tiltedcoord["rook"]=((96,83),(86,83),(78,69),(43,69),(40,75),(37,77),(20,77),(20,67),(28,67),(28,59),(17,59),(17,44),(28,44),(28,36),(20,36),(20,26),(37,26),(40,29),(43,34),(78,34),(86,20),(96,20))
tiltedcoord["horse"]=((82,63),(74,63),(67,55),(64,55),(48,39),(43,39),(40,40),(42,41),(47,49),(47,53),(53,59),(53,64),(50,70),(44,70),(32,61),(27,61),(22,58),(17,51),(11,51),(11,47),(17,42),(18,35),(21,28),(27,22),(34,17),(41,15),(55,15),(67,17),(75,11),(82,11))
tiltedcoord["bishop"]=((84,72),(75,72),(69,61),(66,63),(61,66),(56,68),(50,68),(45,67),(39,65),(34,62),(24,53),(20,54),(16,54),(11,50),(11,45),(16,41),(20,44),(25,47),(34,49),(45,50),(50,50),(50,43),(45,43),(34,41),(27,38),(34,32),(39,29),(45,27),(50,26),(56,26),(61,28),(66,31),(69,33),(75,21),(84,21))
tiltedcoord["queen"]=((82,70),(73,70),(67,63),(39,74),(37,78),(33,80),(29,79),(26,75),(26,71),(29,67),(33,66),(37,66),(46,58),(25,58),(22,61),(18,63),(14,62),(11,58),(10,55),(11,52),(14,49),(18,48),(21,49),(24,51),(42,44),(24,39),(21,41),(18,42),(15,41),(11,38),(10,35),(10,34),(11,31),(15,28),(19,27),(23,28),(25,31),(46,31),(37,23),(33,24),(30,23),(27,21),(25,17),(26,13),(29,11),(33,10),(37,11),(39,15),(67,26),(73,19),(82,19))
tiltedcoord["king"]=((80,68),(72,68),(66,61),(48,76),(44,77),(44,62),(54,54),(54,49),(41,49),(38,53),(38,59),(43,62),(43,77),(36,77),(25,65),(25,56),(27,47),(21,47),(21,53),(13,53),(13,47),(6,47),(6,38),(13,38),(13,32),(21,32),(21,37),(27,37),(25,29),(25,18),(36,8),(43,8),(43,22),(38,26),(38,32),(41,36),(54,36),(54,31),(44,22),(44,8),(48,9),(66,24),(72,16),(80,16))
tiltedcoord["pawn"]=((77,64),(69,64),(51,47),(46,47),(46,53),(43,55),(40,54),(36,48),(33,50),(31,51),(28,52),(23,52),(20,50),(17,47),(15,44),(15,37),(17,34),(20,31),(23,29),(28,29),(31,30),(33,31),(36,33),(40,27),(43,26),(46,28),(46,34),(51,34),(69,17),(77,17))

for i in pieces:
    for tup in tiltedcoord[i]:
        COORD[i]+=((tup[0]+pcdriftx[i], tup[1]+pcdrifty[i]),)


#Colour Selections
LIGHTSQUARECLR="#E8E8E8"
DARKSQUARECLR="#78A7B7"
CHECKSQUARECLR=(224, 111, 111)
SELECTEDLIGHTSQUARECLR="#D8D14D"
SELECTEDDARKSQUARECLR="#C3BC3B"
LEGALLIGHTSQUARECLR="#B0B0D6"
LEGALDARKSQUARECLR="#8888D7"
BLACKPIECECLR='#313339'
WHITEPIECECLR="white"
PAWNPROMOTIONWINDOWCLR="#CCD1D1" #"#E2C35C"

#Colours specific to GUI
DARKBGCLR = "#1F1F1F" #
LIGHTBGCLR = "#CCD1D1" #ACACAC
DARKBGTEXTCLR = "#FFFFFF" #C3C3C3
LIGHTBGTEXTCLR = "#000000"
ACTIVEBGCLR = "#FFFFFF"
ACTIVEFGCLR = "#000000"
PRIMARYCLR = "#CCD1D1"
SECONDARYCLR = "#8BC34A"
TERTIARYCLR = "#FFA726"
WINNERCLR = "#64E052"
DRAWCLR = "#AABABF"
LOSERCLR = "#F37561"


#Drift of white_view board in Double View
DRIFT_WV_BOARD = -300
DRIFT_BOARD_END_OF_GAME = -250

ABOUT_INFO = '''Pocket Chess Arena, a cross-platform desktop application, allows you to play casual chess games with your friends offline or online and also revisit past games. At the end of a game, the PGN (Portable Game Notation) is generated, using which, you can analyse your game on top chess platforms. The objective was to develop a pocket-sized application to help users quickly strike up a game with a friend in the midst of using another application.

It was built using tkinter, turtle and MySQL by 3 students of NPS Indiranagar, Bangalore as part of the Grade 11 and 12 Computer Science project. 

Please feel free to reach out with any questions, comments, or feedback.

Developers:
Sriram Srinivasan 
Subham Patra
Gurumurthy V

Email address: pocketchessarena@gmail.com'''
