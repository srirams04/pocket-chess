#Import of Modules
import turtle
import time
import datetime
from tkinter import *
from tkinter import messagebox
import requests
from playsound import playsound
from threading import Thread
import clipboard
import os


#Import of created files
import home
import logic 
import database_functions
import constant
import logmessage #To help in debugging

#Import of supporting game file
from utils import *


def define_basic_global_variables(touch_move_):
    global size, sqsize, stretch_square, drift, white, black, name, legalmoves, touch_move, turn, move_stage, DRIFT, wh_list_piece_numbers, bl_list_piece_numbers, wh_piece_count, bl_piece_count, legaladd, code, light_square_clr, dark_square_clr, active_piece, move_duration, game_result, pgn, movenumber, last_sec
    
    #Initialising a size for the chess board and a corresponding size for root_turtle
    length = (355 + home.max_board_size) / 2

    size_canvas_turtle = int(length) + 15
    size_root_turtle = size_canvas_turtle + 35
    home.canvas_turtle.configure(width = size_canvas_turtle, height = size_canvas_turtle)
    home.canvas_turtle.update()
    home.root_turtle.geometry(f"{size_root_turtle}x{size_root_turtle+95}")
    
    #Making the size of the board a global variable which can be accessed everywhere
    size = length

    #Size of 1 UNIT square in the chess board
    sqsize = size/8 
    
    #The value by which each unit square should be stretched.
    stretch_square = (size/8)/20

    #Initialsing game_result [None, 'W', 'B', 'D', 'S']
    game_result = None

    #Initialising the view 
    if home.mode_of_play == "online":
        if home.player_side == "white":
            white = True
            black = False
        elif home.player_side == "black":
            white = False
            black = True
    else:
        white = True
        black = False


    #Initialsing active_piece as None because no piece has been dragged yet
    active_piece = None

    #Making the drift of the white board a global variable...which implies that drift of the black view board can as also be accessed as it is negative of the drift of the white view board
    
    if white == True and black == True:
        drift = constant.DRIFT_WV_BOARD
    else:
        drift = 0

    #white view list of piece numbers
    wh_list_piece_numbers = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    wh_piece_count = 0

    #black view list of piece numbers
    bl_list_piece_numbers = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    bl_piece_count=0


    name = {'pawn' : 'pawn',
        'rook' : 'rook',
        'horse' : 'knight',
        'bishop' : 'bishop',
        'queen' : 'queen',
        'king' : 'king'}
    

    #Drawing a boundary around the 'legal moves' button on the screen
    legalmoves=True
    
    home.wn.colormode(255)

    #Touchpiece
    touch_move = touch_move_

    #defining the colours of lightsquare colour and dark square colour
    light_square_clr = constant.LIGHTSQUARECLR
    dark_square_clr = constant.DARKSQUARECLR

    #0 = Waiting for Starting Address, 1 = waiting for Ending Address 
    move_stage = 0

    #Who's turn is it?
    turn="white"

    #List of all the possible legal squares
    legaladd = []

    #Initialising move_duration for the timers
    move_duration = []

    #Initialising movenumber
    movenumber = 0

    #Initialising pgn - portable game notation
    pgn = []

    #last seconds
    last_sec = 20 


#Displays A,B,C, ...H and 1,2,3...8 on the side of the board for whiteview and blackview taking into account the value of boardview
def display_labels():

    #Deletes the OLD labels
    try:
        show_labels(None, None, None, None, False, True)
    except:
        pass
    try:
        show_labels(None, None, None, None, True, True)
    except:
        pass
    

    #Creates the NEW labels
    distance=17
    startdistance=(sqsize/2)+8
    if white==True: 
        show_labels(-(size/2)+drift-distance,(-size/2)-distance, sqsize, startdistance, False)
    if black == True:
        show_labels(-(size/2)-drift-distance,(-size/2)-distance, sqsize,startdistance, True)


#Can be used to create a SINGLE piece at the desired board location (UNLIKE pieces_setup in game.py which creates ALL the pieces in the BASE configuration)
def create_chess_piece(row, col, identity, colour, view):
    global wh_piece_count, bl_piece_count, wh_list_piece_numbers, bl_list_piece_numbers

    #row, col --> wrt white view / list2d 
    if view == "white":
        wh_piece_count+=1
        wh_list_piece_numbers[row][col] = wh_piece_count
        piece_count = wh_piece_count
    elif view == "black":
        bl_piece_count+=1
        blrow = 7- row
        blcol = 7 - col
        bl_list_piece_numbers[blrow][blcol] = bl_piece_count
        piece_count = bl_piece_count
    
        
    globals()[f'{view[:2]}{piece_count}']=turtle.Turtle(visible=False)
    globals()[f'{view[:2]}{piece_count}'].ht()
    globals()[f'{view[:2]}{piece_count}'].pu()
    globals()[f'{view[:2]}{piece_count}'].shape(identity.title())
    stretch_piece = stretch_square * 0.2
    border_width = int(stretch_piece * 4)
    globals()[f'{view[:2]}{piece_count}'].shapesize(stretch_piece, stretch_piece, border_width)
    globals()[f'{view[:2]}{piece_count}'].speed(5) 
    
    if colour == "white":
        globals()[f'{view[:2]}{piece_count}'].color(constant.WHITEPIECECLR)
        globals()[f'{view[:2]}{piece_count}'].pencolor("black")
    elif colour == "black":
        globals()[f'{view[:2]}{piece_count}'].color(constant.BLACKPIECECLR)
        globals()[f'{view[:2]}{piece_count}'].pencolor("black")
    
    
    globals()[f'{view[:2]}{piece_count}'].goto(coord_from_add(row, col, view))
    globals()[f'{view[:2]}{piece_count}'].st()


#Return: Central pixel coordinates as a tuple (IMP: Using the global variable boardview, it also acknowledges the changes in BOARD VIEW and returns the coordinates accordingly)
def coord_from_add(row, col, view):
    step=size/8
    if view == "white":    
        return ((col*step) - (4*step) + (step/2) + drift, (4*step) - (row*step) - (step/2))
    elif view == "black":
        return ( -1 * ((col*step) - (4*step) + (step/2)) - drift, -1 * ((4*step) - (row*step) - (step/2)))


#Deletes all the existing turtle chess pieces on the board, creates new turtle chess pieces for the current configuration. Updates/Resets wh_list_of_piece_numbers, bl_list_of_piece_numbers, wh_piece_count, bl_piece_count.
def configure_pieces():
    global wh_list_piece_numbers, bl_list_piece_numbers, wh_piece_count, bl_piece_count
 

    #Initialisation of some variables

    try:
        del wh_list_piece_numbers, bl_list_piece_numbers, wh_piece_count, bl_piece_count
    except:
        pass
    

    wh_list_piece_numbers = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    bl_list_piece_numbers = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    
    wh_piece_count = 0
    bl_piece_count = 0
    
    if white == True:
        for i in range(8):
            for j in range(8):
                if logic.list2d[i][j] != logic.emp:
                    create_chess_piece(i, j, logic.list2d[i][j][0], logic.colour(logic.list2d[i][j]), "white")
    if black == True:
        for i in range(8):
            for j in range(8):
                if logic.list2d[i][j] != logic.emp:
                    create_chess_piece(i, j, logic.list2d[i][j][0], logic.colour(logic.list2d[i][j]), "black")   


def configure_board():
    #For the individual square turtles, identification is first row number and then column number in the variable name.
      
    #White's View
    if white==True:
        for x in range(len(wh_list_piece_numbers)):
            for y in range(len(wh_list_piece_numbers[x])):
                globals()[f't{x}{y}'] = turtle.Turtle()
                globals()[f't{x}{y}'].shape('square')
                globals()[f't{x}{y}'].shapesize(stretch_square,stretch_square)
                globals()[f't{x}{y}'].up()
                if (x+y)%2==0:
                    globals()[f't{x}{y}'].color(light_square_clr)
                elif (x+y)%2==1:
                    globals()[f't{x}{y}'].color(dark_square_clr)
                globals()[f't{x}{y}'].goto((sqsize/2) + sqsize*(y-4)+drift , -(sqsize/2) + sqsize*(4-x)) 

    if black==True:
        #Black's View
        for x in range(len(bl_list_piece_numbers)):
            for y in range(len(bl_list_piece_numbers[x])):
                globals()[f'tb{x}{y}'] = turtle.Turtle()
                globals()[f'tb{x}{y}'].shape('square')
                globals()[f'tb{x}{y}'].shapesize(stretch_square,stretch_square)
                globals()[f'tb{x}{y}'].up()
                if (x+y)%2==0:
                    globals()[f'tb{x}{y}'].color(light_square_clr)
                elif (x+y)%2==1:
                    globals()[f'tb{x}{y}'].color(dark_square_clr)
                globals()[f'tb{x}{y}'].goto((sqsize/2) + sqsize*(y-4)-drift , -(sqsize/2) + sqsize*(4-x)) 

    display_labels()


def configure_game():
    global whsrow, whscol, blsrow, blscol
    home.wn.tracer(0)
    
    #Hiding and Deleting all the pieces on the screen
    for j, k in zip((wh_piece_count, bl_piece_count), ('wh', 'bl')):
        for i in range(1,j+1):
            try:
                globals()[f'{k}{i}'].ht()
                globals()[f'{k}{i}'].clear()
                del globals()[f'{k}{i}']
            except:
                pass
    
    #Hiding and Deleting all the board turtles on the screen
    for x in range(len(wh_list_piece_numbers)):
        for y in range(len(wh_list_piece_numbers[x])):
            try:
                globals()[f't{x}{y}'].ht()
                globals()[f't{x}{y}'].clear()
                del globals()[f't{x}{y}']
            except:
                pass
    
    for x in range(len(bl_list_piece_numbers)):
        for y in range(len(bl_list_piece_numbers[x])):
            try:
                globals()[f'tb{x}{y}'].ht()
                globals()[f'tb{x}{y}'].clear()
                del globals()[f'tb{x}{y}']
            except:
                pass
    
    configure_board()
    configure_pieces()
    
    try:
        if legalmoves == True:
            show_legal_squares(True)
        
        try:
            pwhsrow, pwhscol, pwherow, pwhecol = prev_move_add
            for row,col in ((pwhsrow, pwhscol), (pwherow, pwhecol)):
                change_square_clr(row, col, 7-row, 7-col, constant.SELECTEDLIGHTSQUARECLR, constant.SELECTEDDARKSQUARECLR)    
        except:
            pass

        change_square_clr(whsrow, whscol, blsrow, blscol, constant.SELECTEDLIGHTSQUARECLR, constant.SELECTEDDARKSQUARECLR)
        change_square_clr(wherow, whecol, blerow, blecol, constant.SELECTEDLIGHTSQUARECLR, constant.SELECTEDDARKSQUARECLR)
    except:
        pass

    display_check_and_checkmate(logic.list2d, constant.CHECKSQUARECLR, True, False)
    display_stalemate(logic.list2d, False)
    if game_result == "D":
        home.on_draw(False)
    home.wn.tracer(1)


#Parameters: WV-row num, WV-col num, BV-row num, BV-col num, light clr, dark clr, should the change be updated on the screen using update or tracer?
def change_square_clr(whsrow, whscol, blsrow, blscol, light, dark, update=True):
    add="filled"
    if wh_list_piece_numbers[whsrow][whscol] == 0:
        add="empty"
    home.wn.tracer(0)
    if (whsrow+whscol)%2==0: #Lighter Squares
        if white==True:
            globals()[f't{whsrow}{whscol}'].color(light)
            if add!="empty":
                globals()[f'wh{wh_list_piece_numbers[whsrow][whscol]}'].st()
        if black==True:
            globals()[f'tb{blsrow}{blscol}'].color(light)
            if add!="empty":
                globals()[f'bl{bl_list_piece_numbers[blsrow][blscol]}'].st()
    elif (whsrow+whscol)%2==1: #Darker Squares
        if white==True:
            globals()[f't{whsrow}{whscol}'].color(dark)
            if add!="empty":
                globals()[f'wh{wh_list_piece_numbers[whsrow][whscol]}'].st()
        if black==True:
            globals()[f'tb{blsrow}{blscol}'].color(dark)
            if add!="empty":
                globals()[f'bl{bl_list_piece_numbers[blsrow][blscol]}'].st()
    if update==True:
        home.wn.tracer(1)


def show_legal_squares(show):
    global legaladd
    
    for m,n in legaladd:
        blm, bln=7-m, 7-n
        if show == True:
            change_square_clr(m, n, blm, bln, constant.LEGALLIGHTSQUARECLR, constant.LEGALDARKSQUARECLR, update=False)
        elif show == False:
            change_square_clr(m, n, blm, bln, light_square_clr, dark_square_clr, update=False)

        
#Parameters: 2 dimensional list, hexadecimal code for the king's square colour when there is a check, if there is a checkmate should it be declared?
def display_check_and_checkmate(f2d, pink, declare, animate = True):
    global mouse_vacant, drift, game_result
    toggleDEBUG=False
    if logmessage.DEBUG==True:
        logmessage.DEBUG=False #No debug info to be PRINTED on the screen until the display_check_and_checkmate function gets over
        toggleDEBUG=True #Debug will be changed back to True at the end of this function


    change=False
    roww, colw=logic.whking[2], logic.whking[3]
    rowb, colb=logic.blking[2], logic.blking[3]
    for i, j in ((roww, colw), (rowb, colb)):
        home.wn.tracer(0)  
    
        if logic.check((i,j), f2d)[0]==True:
            if white==True:
                if globals()[f't{i}{j}'].color()!=(pink,pink):
                    globals()[f't{i}{j}'].color(pink)
                    globals()[f'wh{wh_list_piece_numbers[i][j]}'].st()
                    change=True
            if black==True:
                if globals()[f'tb{7-i}{7-j}'].color()!=(pink,pink):
                    globals()[f'tb{7-i}{7-j}'].color(pink)
                    globals()[f'bl{bl_list_piece_numbers[7-i][7-j]}'].st()
                    change=True

        elif logic.check((i,j), f2d)[0]==False:               
            if white==True:
                if globals()[f't{i}{j}'].color()==(pink,pink):
                    change=True
                    if (i+j)%2==0: 
                        globals()[f't{i}{j}'].color(light_square_clr)
                        globals()[f'wh{wh_list_piece_numbers[i][j]}'].st()
                    elif (i+j)%2==1:
                        globals()[f't{i}{j}'].color(dark_square_clr)
                        globals()[f'wh{wh_list_piece_numbers[i][j]}'].st()
            if black==True:
                if globals()[f'tb{7-i}{7-j}'].color()==(pink,pink):
                    change=True
                    if (i+j)%2==0: 
                        globals()[f'tb{7-i}{7-j}'].color(light_square_clr)
                        globals()[f'bl{bl_list_piece_numbers[7-i][7-j]}'].st()
                    elif (i+j)%2==1:
                        globals()[f'tb{7-i}{7-j}'].color(dark_square_clr)
                        globals()[f'bl{bl_list_piece_numbers[7-i][7-j]}'].st()

        home.wn.tracer(1)

        if logic.checkmate((i,j), f2d)==True and declare==True and animate == False:
            if white==True:
                globals()[f't{i}{j}'].color("red")
                globals()[f'wh{wh_list_piece_numbers[i][j]}'].st()
            if black==True:
                globals()[f'tb{7-i}{7-j}'].color("red")
                globals()[f'bl{bl_list_piece_numbers[7-i][7-j]}'].st()
            home.wn.update()
        elif logic.checkmate((i,j), f2d)==True and declare==True and animate == True:
            if home.volume_toggle == True:
                #Sound for checkmate
                playsound("./Sounds/checkmate.mp3", False)
                        
            home.wn.tracer(0)
            for _ in range(2):
                time.sleep(0.75)
                if (i+j)%2==0:
                    if white==True:
                        globals()[f't{i}{j}'].color(light_square_clr)
                        globals()[f'wh{wh_list_piece_numbers[i][j]}'].st()
                    if black==True:
                        globals()[f'tb{7-i}{7-j}'].color(light_square_clr)
                        globals()[f'bl{bl_list_piece_numbers[7-i][7-j]}'].st()
                    home.wn.update()
                elif (i+j)%2==1:
                    if white==True:
                        globals()[f't{i}{j}'].color(dark_square_clr)
                        globals()[f'wh{wh_list_piece_numbers[i][j]}'].st()
                    if black==True:
                        globals()[f'tb{7-i}{7-j}'].color(dark_square_clr)
                        globals()[f'bl{bl_list_piece_numbers[7-i][7-j]}'].st()
                    home.wn.update()
                        
                time.sleep(0.75)

                if _==1:
                    if white==True:
                        globals()[f't{i}{j}'].color("red")
                        globals()[f'wh{wh_list_piece_numbers[i][j]}'].st()
                    if black==True:
                        globals()[f'tb{7-i}{7-j}'].color("red")
                        globals()[f'bl{bl_list_piece_numbers[7-i][7-j]}'].st()
                    home.wn.update()
                else:
                    if white==True:
                        globals()[f't{i}{j}'].color(pink)
                        globals()[f'wh{wh_list_piece_numbers[i][j]}'].st()
                    if black==True:
                        globals()[f'tb{7-i}{7-j}'].color(pink)
                        globals()[f'bl{bl_list_piece_numbers[7-i][7-j]}'].st()
                    home.wn.update()


            if turn=="white":
                game_result = "W"
            elif turn=="black":
                game_result = "B"
            
            home.on_game_over()

            #The required information about database storage has been taken from the user. Now on clicking the close button, the program can directly close without any pass statements
            def on_turtle_close():
                home.program_running = False
                home.root_turtle.after(500, lambda: home.root_turtle.destroy())
                database_functions.close_connection()
                
            
            home.root_turtle.protocol("WM_DELETE_WINDOW", on_turtle_close)

                     
    if toggleDEBUG==True:
        logmessage.DEBUG=True
    return change


#Parameters: 2 dimensional list
def display_stalemate(f2d, animate = True):
    global mouse_vacant, move_duration, stalemate_boundary, game_result

    #If either of the kings are under check, definitely, it cannot be a stalemate.
    if logic.get_game_situation(logic.list2d)[0]:
        return 
    
    if logic.stalemate(logic.list2d, False)==True:
        if home.volume_toggle == True and animate:
            #Sound of stalemate
            playsound("./Sounds/stalemate.mp3")

            game_result = "S"

            home.on_game_over()

        if turn=="black":
            move_duration += [1]
            #print(move_duration)
        elif turn=="white":
            move_duration += [1]
            #print(move_duration)
        
        home.wn.tracer(0)

        try:
            stalemate_boundary.clear()
        except:
            pass
        home.wn.update()

        stalemate_boundary=turtle.Turtle()
        stalemate_boundary.ht()
        
        stalemate_boundary.width(7)
        stalemate_boundary.color("red")
        for sign in (1,-1):
            stalemate_boundary.pu()
            stalemate_boundary.goto(-(size/2)+sign*drift,(size/2))
            stalemate_boundary.pd()
            for _ in range(4):
                stalemate_boundary.fd(size)
                stalemate_boundary.rt(90)
            if white==True and black==True:
                pass
            else:
                break
        home.wn.tracer(1)                
        

        def on_turtle_close():
            home.program_running = False
            home.root_turtle.after(500, lambda: home.root_turtle.destroy())
            database_functions.close_connection()
        
        home.root_turtle.protocol("WM_DELETE_WINDOW", on_turtle_close)
            

#Aim: Displaying the board in a more readible form on the COMMAND line
#Parameters: 2 dimensional list
def display(board):
    return
    for y in range(len(board)):
        for x in range(len(board[y])):
            print(board[y][x] , end = ' ')
        print()
    

#Aim: Create a tkinter window and ask the users if they want to store the game details to the database. Also take care of network failure exceptions. If users agree, the game details to be uploaded to the database.
def add_to_db(date, start_time, name_white, name_black, result, moves:list, times:list, min_time = 0, increment = 0):  
    if home.mode_of_play == 'online':
        if not home.challenger:
            return 

    min_time = int(min_time)*60 if 1/min_time else 0
    if min_time:
        increment = int(increment)
    else:
        increment = 0

    end_time=datetime.datetime.now().strftime("%H:%M:%S")
    FMT = '%H:%M:%S'
    duration = datetime.datetime.strptime(end_time, FMT) - datetime.datetime.strptime(start_time, FMT)
    times = [tfor(times[r]).replace(' ','') for r in range(len(times))]

    while True:
        value = messagebox.askquestion("Store Game", "Save Game to Database?\nRequires Network Connection")
    
        if value=="yes" and database_functions.check_connection()==False:
            database_functions.open_connection()
    
        if value=="yes" and database_functions.check_connection()==True: 
            database_functions.update_game_details(date, start_time, end_time, duration, name_white, name_black, result, moves, times, min_time, increment)                      
            #After all the details have been uploaded to the database, displaying a message to the user.
            messagebox.showinfo("Status", "Successfully uploaded to database")
            break
        elif value=="no":
            break
        elif value=="yes" and database_functions.check_connection()==False:
            messagebox.showinfo("Error", "No Internet Connection")
    

def get_turtle_coord(x,y):
    home.canvas_turtle.update()
    width = home.canvas_turtle.winfo_width()    
    height = home.canvas_turtle.winfo_height()
    return x - (width/2), (height/2) - y


def get_tkinter_coord(x,y):
    home.canvas_turtle.update()
    width = home.canvas_turtle.winfo_width()    
    height = home.canvas_turtle.winfo_height()
    return x + (width/2), (height/2) - y


def main_updater_offline():
    global old, whitetime, blacktime , move_duration, winner, game_result
    old = time.time()
    while home.program_running and (game_result is None):
        if 1/home.min_time != 0 and timer_start:
            if turn == 'white':
                whitetime -= (time.time() - old)
                old = time.time()
                if whitetime < last_sec:
                    time_left = tfor(whitetime)
                else:
                    time_left = tfor(int(whitetime))[:-2]
                home.label_white_timer_bottom.configure(text = time_left)
                home.label_white_timer_top.configure(text = time_left)
                if whitetime < 0:
                    game_result = 'B' if logic.winner_on_flag('black') else 'D'
                    home.on_game_over()

            elif turn == 'black':
                blacktime -= (time.time() - old)
                old = time.time()
                if blacktime < last_sec:
                    time_left = tfor(blacktime)
                else:
                    time_left = tfor(int(blacktime))[:-2]
                home.label_black_timer_bottom.configure(text = time_left)
                home.label_black_timer_top.configure(text = time_left)
                if blacktime < 0:
                    game_result = 'W' if logic.winner_on_flag('white') else 'D'
                    home.on_game_over()
                    

        home.wn.tracer(0)
        home.wn.update()


def main_updater_online():
    global ready_to_play, turn, game_date , game_start_time
    while home.mode_of_play == "online" and game_result is None:
        if (home.challenger and home.received) or ((not home.challenger) and home.accepted):
            ready_to_play = True 

            while turn != home.player_side:
                res = requests.get(home.geturl('rooms') , params={'code':home.code})
                out = process_response(res)
                time.sleep(0.2)
                home.wn.update()

        home.wn.tracer(0)
        home.wn.update()


def process_response(response):
    global mouse_vacant, game_result, turn, o, whsrow, whscol, blsrow, blscol, srow, scol, whecol, wherow, blecol, blerow, division, started, oldtime, timer_start
    try:
        r = response.json()#[str(home.code)]
        if 'side' in r:
            if r['side'] != home.player_side:
                sr,sc,er,ec = [int(t) for t in tuple(r['move'])]
                process_move((sr,sc),(er,ec),r['pppiece'])
                timer_start = True
            return False
        return r

    except Exception as e:
        return e


def connection():
    global timer_start, game_result, t0
    t0 = int(time.time())
    while game_result is None:
        try:
            if ((not home.challenger) and home.accepted) or (home.challenger and home.received):#or ((not home.challenger) and home.accepted):
                connectoption = True if (int(time.time())%30 == 0 and int(time.time()) != t0) else False
                #print(f'{tfor(int(time.time()))[:-2]} : connection made')
                if connectoption:
                    t0 = int(time.time())
                payload = {'code' : home.code , 'side' : home.player_side , 'connectop' : connectoption}
                res = requests.get(home.geturl('connection') , params=payload)
                data = res.json()

                if data['offers']['status'] == 'gameover':
                    game_result = data['offers']['game result']

                    if data['offers']['resignations'] == home.oppside:
                        messagebox.showinfo('Game Over' , 'You Won on Resignation')
                        game_result = home.player_side[0].upper()
                        home.on_game_over()

                    elif data['offers']['flagged']:
                        if data['offers']['flagged'] == 'white':
                            game_result = 'W' if logic.winner_on_flag('white') else 'D'
                            home.on_game_over()
                        else :
                            game_result = 'B' if logic.winner_on_flag('black') else 'D'
                            home.on_game_over()

                    elif data['offers']['lost connection'] == home.oppside:
                        messagebox.showinfo('Game Over' , 'Game Abandoned\nYou Won')
                        game_result = home.player_side[0].upper()
                        home.on_game_over()
                    break

                if data['offers']['draw offers'] == home.oppside:
                    if messagebox.askyesno('Draw Offer' , 'Your opponent has offered a draw, accept?'):
                        requests.post(home.geturl('connection') , data={'code':home.code , 'side':home.player_side , 'draw':'accepted'})
                        game_result = "D"
                        home.on_game_over()
                        break
                    else:
                        requests.post(home.geturl('connection') , data={'code':home.code , 'side':home.player_side , 'draw':'rejected'})
            
                if 1/home.min_time:
                    wt,bt = data['timers']['white'][0] , data['timers']['black'][0]
                    if bt < last_sec:
                        home.label_black_timer_bottom.configure(text=tfor(bt))
                        home.label_black_timer_top.configure(text=tfor(bt))
                    else:
                        home.label_black_timer_bottom.configure(text=tfor(bt)[:-2])
                        home.label_black_timer_top.configure(text=tfor(bt)[:-2])
                        
                    if wt < last_sec:
                        home.label_white_timer_bottom.configure(text=tfor(wt))
                        home.label_white_timer_top.configure(text=tfor(wt))
                    else:
                        home.label_white_timer_bottom.configure(text=tfor(int(wt))[:-2])
                        home.label_white_timer_top.configure(text=tfor(int(wt))[:-2])

                    if bt > last_sec and wt > last_sec:
                        time.sleep(0.4)

                else:
                    time.sleep(0.4)
        except Exception as e:
            continue 


def generate_pgn():
    global pgn, img_copy, button_pgn_copy

    def on_pgn_copy():
        global button_pgn_copy
        if os.sys.platform.lower()=='win32':
            clipboard.copy(pgn_str)
        else:
            os.system(f'echo -n \'{pgn_str}\'| xclip -selection clipboard')
        button_pgn_copy.configure(text = " PGN copied!")
        home.root_turtle.after(5000, lambda : button_pgn_copy.configure(text = " Copy PGN to clipboard"))


    #Adding some additional details to pgn
    pgn_str = ' '.join(pgn)    
    pgn_result = '*'
    if game_result == "W":
        pgn_result = "1-0"
    elif game_result == "B":
        pgn_result = "0-1"
    elif game_result in ('D', 'S'):
        pgn_result = "1/2-1/2"
    
    pgn_str = f'''
[Site "Pocket Chess Arena"]
[White "{home.white_name}"]
[Black "{home.black_name}"]
[Result "{pgn_result}"]
[Date "{game_date.strftime("%Y.%m.%d")}"]

''' + pgn_str + " " + pgn_result

    img_copy = PhotoImage(file = "./Icons/clipboard.png").subsample(3,3)
    button_pgn_copy = Button(home.frame_pgn, image = img_copy, text = "Copy PGN to clipboard", compound = LEFT, font = ('Comic Sans', 13), bg = constant.LIGHTBGCLR, fg = constant.LIGHTBGTEXTCLR, activebackground = constant.LIGHTBGCLR, command = on_pgn_copy, bd = 0, highlightthickness = 0)
    button_pgn_copy.grid(row = 0, column = 0, sticky = NSEW)


#Main function of game.py which is called by home.py to handle the actual game (settings, instructions NOT included)
#Parameters: size-Size of the chess board, drift-Drift of the white's view board, white-white view==>True/False, black-black view==>True/False, Speech=True/False, Touchpiece=True/False
def game_main(touch_move_): 
    global process_move
    #Handling the close of the main turtle window
    def on_turtle_close():        
        
        if game_result is not None:
            home.program_running = False
            home.root_turtle.after(500, lambda: home.root_turtle.destroy())
            database_functions.close_connection()
            return 
        
        if home.mode_of_play == 'offline': 
            abort = messagebox.askyesno('Abort Game', 'Are you sure?')
        else:
            abort = messagebox.askyesno('Abandon', 'Do you wish to quit?')
        if abort:
            home.program_running = False
            home.root_turtle.after(500, lambda: home.root_turtle.destroy())
            database_functions.close_connection()

    #Move a piece from the Start address to the End address (S to E)
    def make_move(whsrow, whscol, blsrow, blscol, wherow, whecol, blerow, blecol, unitmovement):
        #print(whsrow, whscol, blsrow, blscol, wherow, whecol, blerow, blecol)
 
        if white==True:
            whendx, whendy = sqsize/2 + sqsize*(whecol-4) + drift, -(sqsize/2) + sqsize*(4-wherow)
            #Changes in White's View
            globals()[f'wh{wh_list_piece_numbers[whsrow][whscol]}'].goto(whendx, whendy)
            
        
        if black==True:
            blendx, blendy = sqsize/2 + sqsize*(blecol-4) - drift, -(sqsize/2) + sqsize*(4-blerow)
            #Changes in Black' View
            globals()[f'bl{bl_list_piece_numbers[blsrow][blscol]}'].goto(blendx, blendy) 
            
        home.wn.update()
        home.wn.tracer(1)


    #Hiding all the DEAD pieces on the board
    def hide_dead_pieces(enpassant, enpassant_killpawn_add, wherow, whecol, blerow, blecol):
        if enpassant==True:
            if white==True:
                globals()[f'wh{wh_list_piece_numbers[enpassant_killpawn_add[0]][enpassant_killpawn_add[1]]}'].ht()

            if black==True:
                globals()[f'bl{bl_list_piece_numbers[7-enpassant_killpawn_add[0]][7-enpassant_killpawn_add[1]]}'].ht()

        #If the below condition is satisfied, there was a piece in the ending address and a capture took place
        if logic.list2d_start_of_current_move[wherow][whecol] != logic.emp: 
            if white==True:
                globals()[f'wh{wh_list_piece_numbers[wherow][whecol]}'].ht()
            if black==True:
                globals()[f'bl{bl_list_piece_numbers[blerow][blecol]}'].ht()


    def promote_pawn(wherow, whecol, blerow, blecol):
        global pawnboardturtle, pc, mouse_vacant, movestr
        
        turn_pawnreachedend = turn
        
        pawnboardturtle=turtle.Turtle(visible=False)
        pawnboardturtle.color("black", constant.PAWNPROMOTIONWINDOWCLR)
        pawnboardturtle.shape("square")
        pawnboardturtle.st()
        
        scale_ppboard = int(size * 13/560)
        for i in range(1,scale_ppboard):
            pawnboardturtle.shapesize(i,i)
        
        pccolor={"white": ("black", "white"), "black": ("black", constant.BLACKPIECECLR)}
        pcname=["Horse", "Rook", "Bishop", "Queen"]
        pcsign=((1, 1), (-1, 1), (-1,-1), (1,-1))
        pc={}
        
        def pcchanger(x,y):
            global move_duration, wh_piece_count, bl_piece_count
            inactive_square_size = size * 90/560
            if -inactive_square_size<x<inactive_square_size and -inactive_square_size<y<inactive_square_size:
                pass
            else:
                return None
        
            
            for i in range(4):
                if x/pcsign[i][0]>30 and y/pcsign[i][1]>25:
                    global pawnboardturtle, pc
                    for k in pc:
                        pc[k].ht()
                    for k in range(scale_ppboard,0,-1):
                        pawnboardturtle.shapesize(k,k)    
                    pawnboardturtle.ht()
                    
                    logic.pawnpromotion((wherow, whecol), pcname[i].lower())

                    home.wn.tracer(0)
                    
                    if white==True:
                        globals()[f'wh{wh_list_piece_numbers[wherow][whecol]}'].shape(pcname[i])
                    if black==True:
                        globals()[f'bl{bl_list_piece_numbers[blerow][blecol]}'].shape(pcname[i])    
            
                    home.wn.tracer(1)

                    if home.mode_of_play == 'online':
                        requests.post(
                            home.geturl('rooms'),
                            data = {
                                'code':home.code,
                                'side':home.player_side,
                                'move':movestr,
                                'pppiece':pcname[i].lower()
                            }
                        )
                    else:
                        move_duration += [-1]
                    toggle_turns(False, pcname[i])
                    
                    home.wn.onclick(None)
                    home.canvas_turtle.bind("<ButtonPress>", lambda e: get_move(e.x, e.y, "press"))
                    home.enable_game_controls()

                    display_check_and_checkmate(logic.list2d, (224, 111, 111), True)
                    display_stalemate(logic.list2d)
            
        pawnpcdistance=size * 60 / 560
        for i in range(4):
            home.wn.tracer(0)
            pc[f'pawnpromotion{pcname[i]}'] =turtle.Turtle(visible = False)
            pc[f'pawnpromotion{pcname[i]}'].pu()
            stretch_piece = stretch_square * 0.2
            border_width = int(stretch_piece * 4)
            pc[f'pawnpromotion{pcname[i]}'].shapesize(stretch_piece, stretch_piece, border_width)
            pc[f'pawnpromotion{pcname[i]}'].color(pccolor[turn_pawnreachedend][0], pccolor[turn_pawnreachedend][1])
            pc[f'pawnpromotion{pcname[i]}'].shape(pcname[i])
            pc[f'pawnpromotion{pcname[i]}'].st()

        
        
        fractions = 10
        for j in range(fractions):
            home.wn.tracer(0)
            for i in range(4):
                pc[f'pawnpromotion{pcname[i]}'].goto((j/fractions)*pcsign[i][0]*pawnpcdistance, (j/fractions)*pcsign[i][1]*pawnpcdistance)
            home.wn.tracer(1)
        
        mouse_vacant = False
        home.canvas_turtle.unbind("<ButtonPress>")
        home.wn.onclick(pcchanger)
        home.disable_game_controls()


    #Parameters: Pawn promotion?, checkmate?, stalemate?
    def toggle_turns(pawnv, pppiece = ''): 
        global turn, move_duration, castlev, old, whitetime, blacktime, movenumber
        
        checkv_, checkmatev_, stalematev_ = logic.get_game_situation(logic.list2d)
        
        chess_not = get_chess_notation(logic.list2d_start_of_current_move, whsrow, whscol, wherow, whecol, (checkv_, checkmatev_), castlev, pppiece)
        label_chess_not = Label(home.frame_moves.viewPort, text = chess_not, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Comic Sans', 15, 'bold'), bd = 2, highlightthickness = 2, highlightbackground = constant.LIGHTBGTEXTCLR)

        if turn=="white":
            movenumber += 1
            Label(home.frame_moves.viewPort, text = home.chess_not_row + 1, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Comic Sans', 15, 'bold'), bd = 2, highlightthickness = 2, highlightbackground = constant.LIGHTBGTEXTCLR).grid(row = home.chess_not_row, column = 0, sticky = NSEW, padx = 1, pady = 1, ipadx = 5, ipady = 5)
            label_chess_not.grid(row = home.chess_not_row, column = 1, sticky = NSEW, padx = 1, pady = 1, ipady = 5)
            
            #Updating pgn
            pgn.append(str(home.chess_not_row + 1) + '.')
            pgn.append(chess_not)

            if checkmatev_!=True and pawnv!=True and stalematev_!=True:
                turn="black"

            #Make necessary changes to the timers
            if home.mode_of_play == 'offline' and not pawnv:
                if 1/whitetime:
                    if not (checkmatev_ or stalematev_): 
                        whitetime += home.increment
                    move_duration += [(home.min_time*60 - whitetime  + movenumber*home.increment- sum([x for x in move_duration[:-1:2] if x <= 0]))]
                    if whitetime < last_sec:
                        home.label_white_timer_top.configure(text = tfor(whitetime))
                        home.label_white_timer_bottom.configure(text = tfor(whitetime))
                    else:
                        home.label_white_timer_top.configure(text = tfor(int(whitetime))[:-2])
                        home.label_white_timer_bottom.configure(text = tfor(int(whitetime))[:-2])
                elif not(checkmatev_ or stalematev_):
                    move_duration += [0]

        elif turn=="black":
            label_chess_not.grid(row = home.chess_not_row, column = 2, sticky = NSEW, padx = 1, pady = 1, ipady = 5)

            #Updating pgn
            pgn.append(chess_not)

            home.chess_not_row += 1

            if checkmatev_!=True and pawnv!=True and stalematev_!=True:
                turn="white"

            #Make necessary changes to the timers
            if home.mode_of_play == 'offline' and not pawnv:
                if 1/blacktime:
                    if not(checkmatev_ or stalematev_):
                        blacktime += home.increment
                    move_duration += [(home.min_time*60 - blacktime  + movenumber*home.increment- sum([x for x in move_duration[1:-1:2] if x <= 0]))]
                    if blacktime < last_sec:
                        home.label_black_timer_top.configure(text = tfor(blacktime))
                        home.label_black_timer_bottom.configure(text = tfor(blacktime))
                    else:
                        home.label_black_timer_top.configure(text = tfor(int(blacktime))[:-2])
                        home.label_black_timer_bottom.configure(text = tfor(int(blacktime))[:-2])
                elif not(checkmatev_ or stalematev_):
                    move_duration += [0]

        home.frame_moves.canvas.yview_moveto('1.0')
        home.frame_moves.update()


    def reset_move():
        global legaladd
        
        home.wn.tracer(0)
        #Reverting the colour of the starting square if the user clicks on it again
        if legalmoves==True:
            show_legal_squares(False)
            legaladd = []
        if display_check_and_checkmate(logic.list2d, (224, 111, 111), False) == False:
            change_square_clr(whsrow, whscol, blsrow, blscol, light_square_clr, dark_square_clr)

        #Displaying the squares of the previous in case they are changed due to show_legal_squares(False)
        try:
            pwhsrow, pwhscol, pwherow, pwhecol = prev_move_add
            for row,col in ((pwhsrow, pwhscol), (pwherow, pwhecol)):
                change_square_clr(row, col, 7-row, 7-col, constant.SELECTEDLIGHTSQUARECLR, constant.SELECTEDDARKSQUARECLR)    
        except:
            pass
        home.wn.tracer(1)
        

    #type: "press", "motion", "release"
    def get_move(x, y, mode): 
        global move_stage, blscol, blsrow, whscol, whsrow, turn, legaladd, mouse_vacant, move_duration, active_piece, movestr, timer_start, old
 
        # scol-start address col num(RAW data as seen directly from the board on which the user clicks. For the numbering, the boards are considered to be matrices)
        # srow-start address row num('Same as above')
        # whscol-start address col num(white view list of piece numbers)
        # whsrow-start address row num(white PB)
        # blscol-start address col num(black PB)
        # blsrow-start address row num(black PB)
        # whecol-end address col num(white PB)
        # wherow-end address row num(white PB)
        # blecol-end address col num(black PB)
        # blerow-end address row num(black PB)

        #Irrespective of white and black view, srow and scol are the rownumber and the columnnumber considering both the boards to be MATRICES.

        #Irrespective of white and black view, erow and ecol are the rownumber and the columnnumber considering both the boards to be MATRICES

        x,y = get_turtle_coord(x,y)

        if ready_to_play==False:
            return 
        if home.mode_of_play == 'online':
            if home.player_side != turn:
                return 

        mouse_vacant = True 
    
        x = shift_to_centre(x)

        if move_stage==0 and mode == "press":
            #print("New press/piece")
            srow,scol = get(x,y) 
            
            whsrow, whscol, blsrow, blscol = whiteview_blackview_equivalents(srow,scol)

            #Checking if it is a valid piece
            if  0<=whsrow<=7 and 0<=whscol<=7 and logic.list2d[whsrow][whscol] != logic.emp :
                if turn=="white" and logic.list2d[whsrow][whscol][1][0] != "*":
                    return 
                elif turn=="black" and logic.list2d[whsrow][whscol][1][0] == "*":
                    return
            else:
                return

            move_stage = 1

            #Getting the active piece [currently moving piece]
            if white == True:
                active_piece = globals()[f'wh{wh_list_piece_numbers[whsrow][whscol]}']
            elif black == True:
                active_piece = globals()[f'bl{bl_list_piece_numbers[blsrow][blscol]}']

            #Changing the colour of the starting square
            change_square_clr(whsrow, whscol, blsrow, blscol, constant.SELECTEDLIGHTSQUARECLR, constant.SELECTEDDARKSQUARECLR)

            #Displaying the legal moves
            legaladd = logic.gameprocessing((whsrow, whscol), (None, None))[8]
            if legalmoves==True:
                show_legal_squares(True)
                home.wn.tracer(1)

            #Logging some values
            logmessage.log()
            logmessage.log("Selected Address (ChessNaming) (list2d Numbering): ", info(whsrow, whscol)," ", (whsrow, whscol))
            logmessage.log("Possible Legal Squares: ", legaladd)
            

            home.canvas_turtle.unbind("<ButtonPress>")
            home.canvas_turtle.bind("<B1-Motion>", lambda e: get_move(e.x, e.y, "motion"))
            home.canvas_turtle.bind("<ButtonRelease-1>", lambda e: get_move(e.x, e.y, "release"))  


        elif move_stage == 1 and mode == "motion":
            #print("Motion phase")
            active_piece.goto(x,y)
                 
        elif move_stage == 1 and mode == "release":
            erow,ecol=get(x,y)
            wherow, whecol = whiteview_blackview_equivalents(erow,ecol)[0:2]
            

            def return_piece():
                home.wn.tracer(0)
                if white:
                    sx, sy = antiget(whsrow, whscol)
                elif black:
                    sx, sy = antiget(blsrow, blscol)
                active_piece.goto(sx, sy)
                home.wn.tracer(1)

            #print("All event bindings removed temporarily")
            home.canvas_turtle.unbind("<ButtonPress>")
            home.canvas_turtle.unbind("<B1-Motion>")
            home.canvas_turtle.unbind("<ButtonRelease-1>")
            
            success, pawnv = process_move((whsrow, whscol), (wherow, whecol))
            
            if success:
                timer_start = True
                old = time.time()
                movestr = f'{whsrow}{whscol}{wherow}{whecol}'
                if home.mode_of_play == 'online' and not pawnv:
                    payload = {
                        'code':home.code,
                        'side':home.player_side,
                        'move':movestr,
                        'pppiece':''
                    }
                    requests.post(home.geturl('rooms'),data=payload)

                move_stage = 0
            elif not success:
                home.root_turtle.after(10, return_piece)
                
                #print("Returning the piece to its original position")

            #print("ButtonPress has got back control")
            home.canvas_turtle.bind("<ButtonPress>", lambda e: get_move(e.x, e.y, "press"))
            


        elif move_stage == 1 and mode == "press":
            #print("Second Press")
            row,col = get(x,y)
            if not(0<=row<=7 and 0<=col<=7):
                return
            press_x, press_y = x, y
            whrow, whcol = whiteview_blackview_equivalents(row,col)[0:2]
            

            def on_point_release(x,y):
                global move_stage, legaladd
                x,y = get_turtle_coord(x,y)
                
                if (x,y) == (press_x, press_y) and (touch_move==False or (touch_move==True and legaladd == ())):
                    reset_move()
                    move_stage = 0
                    home.canvas_turtle.unbind("<B1-Motion>")
                    home.canvas_turtle.unbind("<ButtonRelease-1>")
                    home.canvas_turtle.bind("<ButtonPress>", lambda e: get_move(e.x, e.y, "press"))
            
            if (whrow, whcol) == (whsrow, whscol):
                home.canvas_turtle.bind("<B1-Motion>", lambda e: get_move(e.x, e.y, "motion"))
                home.canvas_turtle.bind("<ButtonRelease-1>", lambda e: on_point_release(e.x, e.y))

            else:
                if logic.sameteam(logic.list2d[whrow][whcol], logic.list2d[whsrow][whscol]) and (touch_move==False or (touch_move==True and legaladd == ())):
                    reset_move()
                    x,y = get_tkinter_coord(x,y)
                    move_stage = 0
                    get_move(x, y, 'press')
                    return

            home.canvas_turtle.bind("<ButtonRelease-1>", lambda e: get_move(e.x, e.y, "release"), '+')  
            

    #Returns: success, pawnv
    def process_move(add1, add2, pppiece=''):
        global legaladd, move_stage, prev_move_add, wherow, whecol, blerow, blecol, movestr, checkv, castlev, movestr, whsrow, whscol, blsrow, blscol

        #scord, ecord - always white view
        sr,sc = add1
        er,ec = add2
        whsrow,whscol,blsrow,blscol = sr,sc,7-sr,7-sc
        wherow,whecol,blerow,blecol = er,ec,7-er,7-ec
        
        success = False
        if 0<=wherow<=7 and 0<=whecol<=7:
            success, fadd, ladd, checkv, checkmatev, pawnv, castlev, legalv, legaltuple, enpassant, enpassant_killpawn_add, stalematev=logic.gameprocessing((whsrow, whscol),(wherow, whecol))
        
        if not success:
            return False, False

        movestr = f'{whsrow}{whscol}{wherow}{whecol}'

        #Hiding the legal moves after the user clicks on the ending square
        if  0<=wherow<=7 and 0<=whecol<=7 and (whsrow, whscol) != (wherow, whecol) and success==True:
            if legalmoves==True:
                show_legal_squares(False)
                legaladd = []
                home.wn.tracer(1)

        #Reverting the colour of the squares of the previous move 
        try:
            pwhsrow, pwhscol, pwherow, pwhecol = prev_move_add
            for row,col in ((pwhsrow, pwhscol), (pwherow, pwhecol)):
                change_square_clr(row, col, 7-row, 7-col, light_square_clr, dark_square_clr)    
        except:
            pass

        #Changing the colour of the square clicked(Only ending square)    
        if  0<=wherow<=7 and 0<=whecol<=7 and logic.list2d[wherow][whecol] != logic.emp :
            change_square_clr(wherow, whecol, blerow, blecol, constant.SELECTEDLIGHTSQUARECLR, constant.SELECTEDDARKSQUARECLR)


        prev_move_add = (whsrow, whscol, wherow, whecol)

        if not castlev:

            if home.volume_toggle == True:
                sounds(wherow, whecol, enpassant, False, checkv, checkmatev, stalematev)
            make_move(whsrow, whscol, blsrow, blscol, wherow, whecol, blerow, blecol, 20)
            hide_dead_pieces(enpassant, enpassant_killpawn_add, wherow, whecol, blerow, blecol)
            
            display_check_and_checkmate(logic.list2d, (224, 111, 111), False)  
            

            #Changes in white view list of piece numbers
            wh_list_piece_numbers[wherow][whecol] , wh_list_piece_numbers[whsrow][whscol] = wh_list_piece_numbers[whsrow][whscol] , 0  
         
            #Changes in black view list of piece numbers
            bl_list_piece_numbers[blerow][blecol] , bl_list_piece_numbers[blsrow][blscol] = bl_list_piece_numbers[blsrow][blscol] , 0
                
            if enpassant==True:
                #Changes in white view list of piece numbers
                wh_list_piece_numbers[enpassant_killpawn_add[0]][enpassant_killpawn_add[1]] = 0

                #Changes in black view list of piece numbers
                bl_list_piece_numbers[7-enpassant_killpawn_add[0]][7-enpassant_killpawn_add[1]] = 0

            #if home.volume_toggle == True:
            #    sounds(None, None, False, False, checkv, checkmatev, stalematev)

            if pppiece and pawnv: #Using the choice of promoted piece from the online opponent
                logic.pawnpromotion((wherow, whecol), pppiece)
                home.wn.tracer(0)
                    
                if white==True:
                    globals()[f'wh{wh_list_piece_numbers[wherow][whecol]}'].shape(pppiece.title())
                if black==True:
                    globals()[f'bl{bl_list_piece_numbers[blerow][blecol]}'].shape(pppiece.title())    
                
                display_check_and_checkmate(logic.list2d, (224, 111, 111), False)
                display_stalemate(logic.list2d)  
                toggle_turns(False, pppiece)
                #print('toggled turns')
                home.wn.tracer(1)
            elif pawnv and not pppiece: 
                promote_pawn(wherow, whecol, blerow, blecol)
                return success , True

            toggle_turns(pawnv)
            #print('toggled turns')
        
        elif castlev:

            
            if home.volume_toggle == True:
                sounds(None, None, False, True, checkv, checkmatev, stalematev)

            #King Movement
            whksrow, whkscol=fadd[0][0], fadd[0][1]
            whkerow, whkecol=fadd[1][0], fadd[1][1]
            
            blksrow, blkscol=(7-fadd[0][0]), (7-fadd[0][1])
            blkerow, blkecol=(7-fadd[1][0]), (7-fadd[1][1])
            
            #Rook Movement
            whrsrow, whrscol=ladd[0][0], ladd[0][1]
            whrerow, whrecol=ladd[1][0], ladd[1][1]
            
            blrsrow, blrscol=(7-ladd[0][0]), (7-ladd[0][1])
            blrerow, blrecol=(7-ladd[1][0]), (7-ladd[1][1])
            
            
            #Moving the king
            make_move(whksrow, whkscol, blksrow, blkscol, whkerow, whkecol, blkerow, blkecol, 50) 
            
            #Moving the rook
            make_move(whrsrow, whrscol, blrsrow, blrscol, whrerow, whrecol, blrerow, blrecol, 50)  
            
            display_check_and_checkmate(logic.list2d, (224, 111, 111), False)
            

            #Changes in white view list of piece numbers
            wh_list_piece_numbers[whkerow][whkecol] , wh_list_piece_numbers[whksrow][whkscol] = wh_list_piece_numbers[whksrow][whkscol] , 0
            wh_list_piece_numbers[whrerow][whrecol] , wh_list_piece_numbers[whrsrow][whrscol] = wh_list_piece_numbers[whrsrow][whrscol] , 0
                
            #Changes in black view list of piece numbers
            bl_list_piece_numbers[blkerow][blkecol] , bl_list_piece_numbers[blksrow][blkscol] = bl_list_piece_numbers[blksrow][blkscol] , 0
            bl_list_piece_numbers[blrerow][blrecol] , bl_list_piece_numbers[blrsrow][blrscol] = bl_list_piece_numbers[blrsrow][blrscol] , 0
    
            toggle_turns(False)
            #print('toggled turns')
        
        try:
            pwhsrow, pwhscol, pwherow, pwhecol = prev_move_add
            for row,col in ((pwhsrow, pwhscol), (pwherow, pwhecol)):
                change_square_clr(row, col, 7-row, 7-col, constant.SELECTEDLIGHTSQUARECLR, constant.SELECTEDDARKSQUARECLR)    
        except:
            pass

        display_check_and_checkmate(logic.list2d, (224, 111, 111), True)
        display_stalemate(logic.list2d)

        return success, False


    global timer_start, whitetime , blacktime, firstmove, oldtime, ready_to_play, game_date, game_start_time

    home.root_turtle.protocol("WM_DELETE_WINDOW", on_turtle_close)
    logic.define_basic_global_variables()
    define_basic_global_variables(touch_move_)
    configure_game()
    
    home.wn.tracer(1)
    home.wn.listen()
    
    if home.mode_of_play == "offline":
        ready_to_play = True
        game_date = datetime.date.today() 
        game_start_time = datetime.datetime.now().strftime("%H:%M:%S")
    else:
        ready_to_play = False

    #Add game_date line for online after getting from Subham
    
    home.canvas_turtle.bind("<ButtonPress>", lambda e: get_move(e.x, e.y, "press"))
    
    #Timer Variables
    home.min_time = int(home.min_time) if home.min_time.isdigit() else float('inf')
    home.increment = int(home.increment) if home.increment else 0

    timer_start = False
    whitetime = home.min_time*60
    blacktime = home.min_time*60

    game_start_time = datetime.datetime.now().strftime("%H:%M:%S")
    game_date = datetime.date.today() 

    home.canvas_turtle.bind("<ButtonPress>", lambda e: get_move(e.x, e.y, "press"))
    #Thread(target=gettime).start()

    if home.mode_of_play == "offline":
        main_updater_offline()
    elif home.mode_of_play == 'online':
        Thread(target=connection).start()
        main_updater_online()

    home.wn.tracer(1)  
    