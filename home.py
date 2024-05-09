#Import of Modules
import turtle
import time
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser
from tkinter import messagebox
import random
import requests
from threading import Thread
import clipboard
import ctypes
import os
from screeninfo import get_monitors

#Import of created files
import game
import logic
import replay
import constant
import database_functions
from utils import Tooltip, CustomButton, rgb_to_hex, ScrolledFrame, tfor, show_labels


def main_menu():
    global canvas_turtle, img_logo, img_history, img_play_offline, img_play_online, img_toggle_on, img_toggle_off, canvas_main_menu, mode_of_play
    
    def on_play_over_board():
        global mode_of_play
        mode_of_play = "offline"
        settings()
        
    def on_play_with_friends():
        global mode_of_play
        mode_of_play = "online"
        settings()
    
    def on_visit_past_games():
        global mode_of_play, canvas_main_menu
        mode_of_play = None
        destroy_all_widgets_in_canvas_main_menu()
        canvas_main_menu.destroy()
        if database_functions.check_connection()==False:
            #Opening Database function
            database_functions.open_connection()
        if database_functions.check_connection()==True:
            root_turtle.grid_columnconfigure((0,1,2,3), weight = 0)
            root_turtle.grid_rowconfigure((0,1,2,3), weight = 0)
            replay.games_played()
        else:
            messagebox.showerror("Error", "Check your internet connection and try again.")
    
    def on_about():
        about()

    def on_turtle_close():
        global program_running
        program_running = False
        root_turtle.destroy()
        database_functions.close_connection()

    root_turtle.protocol("WM_DELETE_WINDOW", on_turtle_close)
    
    #canvas_turtle has been placed at the location below temporarily. It will get replaced by canvas_left. If canvas_turtle is NOT placed anywhere on the screen, turtle will throw an error. So, we are actually fooling turtle.    
    canvas_turtle.grid(row = 0, column = 0)
    
    #Gridding root_turtle
    root_turtle.grid_columnconfigure((0,1,2,3), weight = 0)
    root_turtle.grid_rowconfigure((0,1,2,3), weight = 0)
    root_turtle.grid_rowconfigure(0, weight = 1)
    root_turtle.grid_columnconfigure(0, weight = 1)
    
    #Creating the main menu window
    canvas_main_menu = Canvas(root_turtle, bg = constant.DARKBGCLR, bd = 0, highlightthickness = 0)
    canvas_main_menu.grid(row = 0, column = 0, sticky = NSEW, ipadx = 5, ipady = 5)
 
    #Gridding canvas_main_menu
    canvas_main_menu.grid_columnconfigure((0,1), weight = 1)
    canvas_main_menu.grid_rowconfigure((0,1,2), weight = 1)

    
    #Adding the pocket chess arena logo 
    img_logo = PhotoImage(file = "./Icons/pocket_chess_arena_logo.png").subsample(3, 3) 
    label_logo = Label(canvas_main_menu, image = img_logo, text = "POCKET\nCHESS  ARENA", compound = TOP, font = ('Algerian', 32, 'bold'), fg = constant.LIGHTBGTEXTCLR, bg = constant.LIGHTBGCLR, bd = 2, highlightthickness = 2, justify = CENTER)
    label_logo.grid(row = 0, column = 0, rowspan = 4, sticky = NSEW, ipadx = 10, ipady = 10)
    
    #Creating the icons for the buttons/toggles
    img_history = PhotoImage(file = "./Icons/history.png").subsample(6,6)
    img_play_offline = PhotoImage(file = "./Icons/play_offline.png").subsample(6,6)
    img_play_online = PhotoImage(file = "./Icons/play_online.png").subsample(6,6)
    img_toggle_on = PhotoImage(file = "./Icons/on.png")
    img_toggle_off = PhotoImage(file = "./Icons/off.png")

    #Creating all the buttons inside
    button_play_offline = CustomButton(canvas_main_menu, text = "    PLAY OVER THE BOARD", image = img_play_offline, compound = TOP, font = ('Algerian', 20, 'bold'), bg = constant.PRIMARYCLR, fg = constant.LIGHTBGTEXTCLR, relief = "ridge", justify = "center", command = on_play_over_board)
    button_play_online = CustomButton(canvas_main_menu, text = "    PLAY A FRIEND ONLINE", image = img_play_online, compound = TOP,font = ('Algerian', 20, 'bold'), bg = constant.PRIMARYCLR, fg = constant.LIGHTBGTEXTCLR, relief = "ridge", justify = "center", command = on_play_with_friends)
    button_visit_past_games = CustomButton(canvas_main_menu, text = "    VISIT PAST GAMES    ", image = img_history, compound = TOP, font = ('Algerian', 20, 'bold'), bg = constant.PRIMARYCLR, fg = constant.LIGHTBGTEXTCLR, relief = "ridge", justify = "center", command = on_visit_past_games)
    button_about = CustomButton(canvas_main_menu, text = "ABOUT", font = ('Algerian', 18, 'bold'), bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, bd = 0, highlightthickness = 0, relief = "ridge", command = on_about)
    

    #Gridding all the buttons
    button_play_offline.grid(row = 0, column = 1, sticky = NSEW, ipadx = 10, ipady = 10, padx = 40, pady = (30, 20))
    button_play_online.grid(row = 1, column = 1, sticky = NSEW, ipadx = 10, ipady = 10, padx = 40, pady = 20)
    button_visit_past_games.grid(row = 2, column = 1, sticky = NSEW, ipadx = 10, ipady = 10, padx = 40, pady = 20)
    button_about.grid(row = 3, column = 1, sticky = EW, ipadx = 5, ipady = 5, padx = 40, pady = 5)
    

def destroy_all_widgets_in_canvas_main_menu():
    global canvas_main_menu
    for widget in canvas_main_menu.winfo_children():
        try:
            for child_widget in widget.winfo_children():
                child_widget.destroy()
        except:
            pass
        widget.destroy()


def send_challenge_request(code): #Challenger
    global url, oppname, received , oppside, black_name , white_name

    info = {
        'code': code, 
        'name': player_name, 
        'side': player_side, 
        'mintime': min_time, 
        'inc': increment, 
        'tm' : touch_move,
        'status':'waiting'
    }
    r = requests.post(geturl('rooms'), data = info)

    while True:
        try:
            r = requests.get(geturl('rooms') , params={'code':code})
            r = r.json()
            if r['status'] == 'running':
                received = True
                break
        except Exception as e:
            pass
        time.sleep(0.2)

    oppname = r['name']
    oppside = 'white' if player_side == 'black' else 'black'
    if player_side == 'white':
        white_name = player_name
        black_name = oppname
        root_turtle.title(f'{code}: {player_name} vs {oppname}')
    else:
        white_name = oppname
        black_name = player_name
        root_turtle.title(f'{code}: {oppname} vs {player_name}')


def accept_challenge_request(code): #Joinee
    global accepted, oppname, oppside, touch_move, min_time, increment, player_side, black_name, white_name
    info = {
        'code': code, 
        'name': player_name,                 
        'status': 'running'
    }

    while 1:
        try:
            r = requests.get(geturl('rooms') , params={'code' : code})
            r = r.json()
            if r is None:
                messagebox.showerror("Error" , f"Invalid room code {code}")
                return False
            if r['status'] == 'waiting':
                accepted = True
                requests.post(geturl('rooms'), data=info)
                break
        except KeyError:
            messagebox.showerror("Error" , f"Invalid room code {code}")
            return False
        except Exception  as e:
            pass
        time.sleep(0.2)

    oppinfo = r
    oppname = oppinfo['name']
    oppside = oppinfo['side']
    player_side = 'white' if oppside == 'black' else 'black'
    touch_move = (oppinfo['tm'].lower() == 'true')
    min_time = oppinfo['mintime']
    increment = int(oppinfo['inc']) if oppinfo['inc'] else 0
    if player_side == 'white':
        white_name = player_name
        black_name = oppname
        root_turtle.title(f'{code}: {player_name} vs {oppname}')
    else:
        white_name = oppname
        black_name = player_name
        root_turtle.title(f'{code}: {oppname} vs {player_name}')
    return True


#For the timers and stuff (pre game page)
def settings():
    global canvas_turtle, var_min_time, var_increment, mode_of_play, canvas_main_menu, img_play_offline, img_play_online, img_history, img_back, img_join_game, img_create_game, button_touch_move, touch_move, challenger, joinee_code, var_white_name, var_black_name
    
    possible_min_times=["Unlimited", '1', '2', '3', '5', '10', '15', '20', '30', '45', '60', '90']
    possible_increments=['0','3','5','10','30','60']


    def select_min_time(e):
        global combo_increment
        min_time_ = var_min_time.get()
        if min_time_ == "Unlimited":
            var_increment.set('')
            combo_increment['state'] = DISABLED
        elif min_time_ != "Unlimited" and str(combo_increment['state']) == str(DISABLED):
            combo_increment['state'] = 'readonly'
    

    def on_start_game():
        global canvas_turtle, canvas_main_menu, var_white_name, var_black_name, var_min_time, var_increment, white_name, black_name, min_time, increment

        white_name = var_white_name.get().strip().strip('*')
        black_name = var_black_name.get().strip().strip('*')
        min_time = var_min_time.get()
        increment = var_increment.get()       

        if not(white_name and black_name and ((min_time and increment) or min_time.lower() == "unlimited")):
            return

        #print(white_name, black_name, min_time, increment)

        destroy_all_widgets_in_canvas_main_menu()
        canvas_main_menu.destroy()
        setup_game()


    def on_touch_move_toggle():
        global touch_move, button_touch_move
        if touch_move == True:
            touch_move = False
            button_touch_move.configure(image = img_toggle_off)
        elif touch_move == False:
            touch_move = True
            button_touch_move.configure(image = img_toggle_on)
        pass

    
    def on_back():
        global canvas_main_menu
        destroy_all_widgets_in_canvas_main_menu()
        canvas_main_menu.destroy()
        main_menu()


    def on_choice_create_game():
        global canvas_main_menu, frame_self_details, label_player_side, label_player_name, challenger, var_player_side, var_player_name



        def on_create_game(): #Online
            global received, canvas_turtle, canvas_main_menu, var_player_side, var_player_name, player_side, player_name, min_time, increment, code, started

            player_side = var_player_side.get().lower().strip('*')
            player_name = var_player_name.get().strip().strip('*')
            min_time = var_min_time.get()
            increment = var_increment.get()

            if not(player_side and player_name and ((min_time and increment) or min_time.lower() == "unlimited")):
                return 
            
            if player_side == "random":
                player_side = random.choice(("white", "black"))

            received = False
            code = requests.get(geturl('connect')).text
            Thread(target=send_challenge_request,args=[code]).start()
            
            destroy_all_widgets_in_canvas_main_menu()
            canvas_main_menu.destroy()
            
            setup_game()

        #The player is a challenger
        challenger = True

        #Creating a frame and adding entry boxes to input name and side chosen by the player
        frame_self_details = Frame(canvas_main_menu, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
        frame_self_details.grid(row = 1, column = 1, sticky = EW, padx = 30, pady = (0,10), ipadx = 10, ipady = 10)
    
        #Gridding frame_names
        frame_self_details.grid_columnconfigure((0,1), weight = 1)
        frame_self_details.grid_rowconfigure((0,1), weight = 1)

        label_player_side = Label(frame_self_details, text = "Your side", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), bd = 0, highlightthickness=0)
        label_player_name = Label(frame_self_details, text = "Your name", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), bd = 0, highlightthickness=0)

        var_player_side = StringVar()
        combo_player_side = ttk.Combobox(frame_self_details, textvariable = var_player_side, justify = CENTER, font = ("Consolas", 20), state = 'readonly')
        combo_player_side['values'] = ('White', 'Black', 'Random')
        combo_player_side.current()

        var_player_name = StringVar()
        entry_player_name = Entry(frame_self_details, textvariable = var_player_name, font = ('Consolas', 20), justify = CENTER)

        #Gridding all the contents of frame_self_details
        label_player_side.grid(row = 0, column = 0, sticky = NSEW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        combo_player_side.grid(row = 0, column = 1, sticky = EW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        label_player_name.grid(row = 1, column = 0, sticky = NSEW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        entry_player_name.grid(row = 1, column = 1, sticky = EW, padx = 5, pady = 10, ipadx = 10, ipady = 2)

        #Creating the button to create game
        button_create_game = CustomButton(canvas_main_menu, text = "CREATE GAME", font = ('Algerian', 22, 'bold'), bg = constant.SECONDARYCLR, fg = constant.DARKBGTEXTCLR, relief = "ridge", justify = "center", command = on_create_game)
        button_create_game.grid(row = 4, column = 1, sticky = EW, padx = 30, pady = (5, 20), ipadx = 10, ipady = 10)

        #Taking out focus
        label_player_side.bind("<Button-1>", lambda e: label_player_side.focus_set())
        label_player_name.bind("<Button-1>", lambda e: label_player_name.focus_set())

        offline_or_challenger()


    def on_choice_join_game():
        global challenger, canvas_main_menu, frame_joinee_code, label_player_name, label_joinee_code, var_joinee_code, var_player_name



        def on_join_game(): #Online
            global canvas_turtle, canvas_main_menu, var_player_name, player_name, var_joinee_code, joinee_code, player_side, min_time, increment, touch_move, code, accepted 

            player_name = var_player_name.get().strip().strip('*')
            joinee_code = var_joinee_code.get().strip().strip('*')
            code = joinee_code

            if not (player_name and joinee_code):
                return 

            #Check if valid game code and get player_side, min_time, increment and touch_move
            accepted = False
            success = accept_challenge_request(joinee_code)
            if success:
                    destroy_all_widgets_in_canvas_main_menu()
                    canvas_main_menu.destroy()
                
                    setup_game()
        
        #The player is a joinee
        challenger = False

        #Creating a frame and adding entry boxes to input name and side chosen by the player
        frame_names = Frame(canvas_main_menu, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
        frame_names.grid(row = 1, column = 1, sticky = EW, padx = 30, pady = 10, ipadx = 5, ipady = 5)

        #Gridding frame_names
        frame_names.grid_rowconfigure(0, weight = 1)
        frame_names.grid_columnconfigure((0,1), weight = 1)

        label_player_name = Label(frame_names, text = "Your name", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), bd = 0, highlightthickness=0)
        label_player_name.grid(row = 0, column = 0, sticky = EW, padx = 5, pady = 5, ipadx = 10, ipady = 2)

        var_player_name = StringVar()
        entry_player_name = Entry(frame_names, textvariable = var_player_name, font = ('Consolas', 20), justify = CENTER)
        entry_player_name.grid(row = 0, column = 1, sticky = EW, padx = 5, pady = 5, ipadx = 10, ipady = 2)

        frame_joinee_code = Frame(canvas_main_menu, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
        frame_joinee_code.grid(row = 2, column = 1, sticky = EW, padx = 30, pady = 10, ipadx = 5, ipady = 5)

        #Gridding frame_joinee_code
        frame_joinee_code.grid_rowconfigure(0, weight = 1)
        frame_joinee_code.grid_columnconfigure((0,1), weight = 1)

        label_joinee_code = Label(frame_joinee_code, text = "Game code", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), bd = 0, highlightthickness=0)
        label_joinee_code.grid(row = 0, column = 0, sticky = EW, padx = 5, pady = 5, ipadx = 10, ipady = 2)

        var_joinee_code = StringVar()        
        entry_joinee_code = Entry(frame_joinee_code, textvariable = var_joinee_code, font = ('Consolas', 20), justify = CENTER)
        entry_joinee_code.grid(row = 0, column = 1, sticky = EW, padx = 5, pady = 5, ipadx = 10, ipady = 2)

        #Creating the button to join game
        button_join_game = CustomButton(canvas_main_menu, text = "JOIN GAME", font = ('Algerian', 22, 'bold'), bg = constant.SECONDARYCLR, fg = constant.DARKBGTEXTCLR, relief = "ridge", justify = "center", command = on_join_game)
        button_join_game.grid(row = 3, column = 1, sticky = EW, padx = 30, pady = (5, 20), ipadx = 10, ipady = 10)

        #Taking out focus
        canvas_main_menu.bind("<Button-1>", lambda e: canvas_main_menu.focus_set()) 
        frame_names.bind("<Button-1>", lambda e: frame_names.focus_set()) 
        frame_joinee_code.bind("<Button-1>", lambda e: frame_joinee_code.focus_set())   
        label_joinee_code.bind("<Button-1>", lambda e: label_joinee_code.focus_set())
        label_player_name.bind("<Button-1>", lambda e: label_player_name.focus_set())


    def offline_or_challenger():
        global canvas_main_menu, touch_move, var_min_time, var_increment, button_touch_move, combo_increment
        
        #Creating a frame for the timer initialisation and then creating the timers
        frame_timers = Frame(canvas_main_menu, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
        frame_timers.grid(row = 2, column = 1, sticky = EW, padx = 30, pady = 10, ipadx = 10, ipady = 10)

        #Gridding frame_timers
        frame_timers.grid_columnconfigure((0,1), weight = 1)
        frame_timers.grid_rowconfigure((0,1), weight = 1)

        #Creating the title labels for the content in frame_timers
        label_min_time = Label(frame_timers, text = "Min time (min)", font = ("Consolas", 20, 'bold'), bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, bd = 0, highlightthickness=0)
        label_increment = Label(frame_timers, text = "Increment (sec)", font = ("Consolas", 20, 'bold'), bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, bd = 0, highlightthickness=0)

        #Creating the comboboxes for receiving their choices for the min time and increment
        var_min_time = StringVar()
        combo_min_time= ttk.Combobox(frame_timers, textvariable = var_min_time, justify = CENTER, font = ("Consolas", 20), state = 'readonly')
        
        var_increment = StringVar()
        combo_increment = ttk.Combobox(frame_timers, textvariable = var_increment, justify = CENTER, font = ("Consolas", 20), state = 'readonly')

        combo_min_time['values'] = tuple(possible_min_times)
        combo_increment['values'] = tuple(possible_increments)
        
        combo_min_time.current()
        combo_increment.current()

        combo_min_time.bind('<<ComboboxSelected>>', select_min_time)

        #Packing all the contents of frame_timers
        label_min_time.grid(row = 0, column = 0, sticky = NSEW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        combo_min_time.grid(row = 0, column = 1, sticky = EW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        label_increment.grid(row = 1, column = 0, sticky = NSEW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        combo_increment.grid(row = 1, column = 1, sticky = EW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        
        #Creating a frame and then adding touchpiece toggle
        touch_move = False
        frame_touch_move = Frame(canvas_main_menu, bg = constant.DARKBGCLR, bd = 0, highlightthickness = 0)
        frame_touch_move.grid(row = 3, column = 1, sticky = EW, padx = 30, pady = 10, ipadx = 10, ipady = 10)

        #Gridding frame_touch_move
        frame_touch_move.grid_columnconfigure((0,1), weight = 1)
        frame_touch_move.grid_rowconfigure(0, weight = 1)
        label_touch_move = Label(frame_touch_move, text = "Enable touch move", font = ("Consolas", 20, 'bold'), bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, bd = 0, highlightthickness=0)
        
        button_touch_move = Button(frame_touch_move, image = img_toggle_off, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, activebackground = constant.DARKBGCLR, activeforeground = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), command = on_touch_move_toggle, bd = 0, highlightthickness = 0)
        
        label_touch_move.grid(row = 0, column = 0, sticky = E, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        button_touch_move.grid(row = 0, column = 1, sticky = W, padx = 5, pady = 10, ipadx = 10, ipady = 2)


        #Taking out focus
        canvas_main_menu.bind("<Button-1>", lambda e: canvas_main_menu.focus_set())   
        frame_timers.bind("<Button-1>", lambda e: frame_timers.focus_set())  
        label_min_time.bind("<Button-1>", lambda e: label_min_time.focus_set())  
        label_increment.bind("<Button-1>", lambda e: label_increment.focus_set())  
        label_touch_move.bind("<Button-1>", lambda e: label_touch_move.focus_set())  
        
    challenger = None #Undecided
    destroy_all_widgets_in_canvas_main_menu()

    #Regridding canvas_main_menu
    canvas_main_menu.grid_columnconfigure((0,1), weight = 1)
    canvas_main_menu.grid_rowconfigure(0, weight = 0)
    canvas_main_menu.grid_rowconfigure((1,2,3,4), weight = 1)
    
    #Adding a back button
    img_back = PhotoImage(file = "./Icons/back.png").subsample(2,2)
    button_back = Button(canvas_main_menu, image = img_back, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, activebackground = constant.DARKBGCLR, activeforeground = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), command = on_back, bd = 0, highlightthickness = 0)
    button_back.grid(row = 0, column = 1, sticky = W, padx = 10)
    
    if mode_of_play == "offline":
        #Displaying the choice (online/offline) on the left half of the screen
        img_play_offline = PhotoImage(file = "./Icons/play_offline.png").subsample(2,2)
        label_play_offline = Label(canvas_main_menu, text = "PLAY OVER THE\nBOARD", image = img_play_offline, compound = TOP, font = ('Algerian', 25, 'bold'), bg = constant.PRIMARYCLR, fg = constant.LIGHTBGTEXTCLR, justify = 'center')
        label_play_offline.grid(row = 0, column = 0, rowspan = 5, sticky = NSEW, ipadx = 30, ipady = 20)

        #Creating a frame and adding the entry boxes in it to input the name of the players
        frame_names = Frame(canvas_main_menu, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
        frame_names.grid(row = 1, column = 1, sticky = EW, padx = 30, pady = (0,10), ipadx = 10, ipady = 10)
        
        #Gridding frame_names
        frame_names.grid_columnconfigure((0,1), weight = 1)
        frame_names.grid_rowconfigure((0,1), weight = 1)

        label_white_name = Label(frame_names, text = "White name", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), bd = 0, highlightthickness=0)
        var_white_name = StringVar()
        entry_white_name = Entry(frame_names, textvariable = var_white_name, font = ('Consolas', 20), justify = CENTER)

        label_black_name = Label(frame_names, text = "Black name", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), bd = 0, highlightthickness=0)
        var_black_name = StringVar()
        entry_black_name = Entry(frame_names, textvariable = var_black_name, font = ('Consolas', 20), justify = CENTER)

        label_white_name.grid(row = 0, column = 0, sticky = NSEW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        entry_white_name.grid(row = 0, column = 1, sticky = EW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        label_black_name.grid(row = 1, column = 0, sticky = NSEW, padx = 5, pady = 10, ipadx = 10, ipady = 2)
        entry_black_name.grid(row = 1, column = 1, sticky = EW, padx = 5, pady = 10, ipadx = 10, ipady = 2)

        #Creating the button to start game
        button_start_game = CustomButton(canvas_main_menu, text = "START GAME", font = ('Algerian', 22, 'bold'), bg = constant.SECONDARYCLR, fg = constant.DARKBGTEXTCLR, relief = "ridge", justify = "center", command = on_start_game)
        button_start_game.grid(row = 4, column = 1, sticky = EW, padx = 30, pady =  (5, 20), ipadx = 10, ipady = 10)

        #Taking out focus
        label_play_offline.bind("<Button-1>", lambda e: label_play_offline.focus_set())   
        frame_names.bind("<Button-1>", lambda e: frame_names.focus_set())   
        label_white_name.bind("<Button-1>", lambda e: label_white_name.focus_set())  
        label_black_name.bind("<Button-1>", lambda e: label_black_name.focus_set())

        offline_or_challenger()
 
    elif mode_of_play == "online":

        #Displaying the choice (online/offline) on the left half of the screen
        img_play_online = PhotoImage(file = "./Icons/play_online.png").subsample(3,3)
        label_play_online = Label(canvas_main_menu, text = "PLAY A FRIEND\nONLINE", image = img_play_online, compound = TOP, font = ('Algerian', 32, 'bold'), bg = constant.PRIMARYCLR, fg = constant.LIGHTBGTEXTCLR, justify = 'center')
        label_play_online.grid(row = 0, column = 0, rowspan = 5, sticky = NSEW, ipadx = 30, ipady = 20)

        #Creating the images for create game and join game
        img_create_game = PhotoImage(file = "./Icons/plus.png")
        img_join_game = PhotoImage(file = "./Icons/enter.png")

        #Adding the buttons to know whether the user wants to join a game or create a game
        button_choice_create_game = CustomButton(canvas_main_menu, text = "CREATE GAME", image = img_create_game, compound = TOP,  font = ('Algerian', 20, 'bold'), bg = constant.PRIMARYCLR, fg = constant.LIGHTBGTEXTCLR, relief = "ridge", justify = "center", command = lambda : (button_choice_create_game.destroy(), button_choice_join_game.destroy(), on_choice_create_game()))
        button_choice_create_game.grid(row = 1, column = 1, sticky = EW, ipadx = 50, ipady = 30, padx = 40, pady = (0,30))
        
        button_choice_join_game = CustomButton(canvas_main_menu, text = "JOIN GAME", image = img_join_game, compound = TOP,  font = ('Algerian', 20, 'bold'), bg = constant.PRIMARYCLR, fg = constant.LIGHTBGTEXTCLR, relief = "ridge", justify = "center", command = lambda : (button_choice_join_game.destroy(), button_choice_create_game.destroy(), on_choice_join_game()))
        button_choice_join_game.grid(row = 2, column = 1, sticky = EW, ipadx = 50, ipady = 30, padx = 40, pady = (30, 60))

        #Taking out focus
        label_play_online.bind("<Button-1>", lambda e: label_play_online.focus_set())   


def disable_game_controls():
    global scale_board, button_color_chooser, button_volume_toggle, button_legal_moves, button_flip
    scale_board.configure(state = DISABLED)
    button_color_chooser.configure(state = DISABLED)
    button_volume_toggle.configure(state = DISABLED)
    button_legal_moves.configure(state = DISABLED)
    button_flip.configure(state = DISABLED)
    scale_board.unbind("<ButtonRelease-1>")


def enable_game_controls():
    global scale_board, button_color_chooser, button_volume_toggle, button_legal_moves, button_flip
    scale_board.configure(state = NORMAL)
    button_color_chooser.configure(state = NORMAL)
    button_volume_toggle.configure(state = NORMAL)
    button_legal_moves.configure(state = NORMAL)
    button_flip.configure(state = NORMAL)
    scale_board.bind("<ButtonRelease-1>", on_scale_board_release)


def on_scale_board_release(e):
    global scale_board, var_board_scaler
    
    length = (355 + max_board_size) / 2
    amplitude = max_board_size - length
    game.size = length + (var_board_scaler.get() - 50)/20 * amplitude
    game.sqsize = game.size / 8
    game.stretch_square=(game.size/8)/20
    if e is not None:
        game.configure_game() 

    size_canvas_turtle = int(game.size) + 15
    size_root_turtle = size_canvas_turtle + 35
    canvas_turtle.configure(width = size_canvas_turtle, height = size_canvas_turtle)
    canvas_turtle.update()
    width_root_turtle = size_root_turtle
    
    if button_extend_left['text'] == ">":
        frame_left.update_idletasks()
        width_root_turtle += frame_left.winfo_width()
    if button_extend_right['text'] == "<":
        frame_right.update_idletasks()
        width_root_turtle += frame_right.winfo_width()
    
    root_turtle.geometry(f"{width_root_turtle}x{size_root_turtle+95}")
    

def on_pin_toggle():
    global pinned, button_pin
    if pinned == True:
        pinned = False
        root_turtle.attributes('-topmost',False)
        button_pin.configure(image = img_pin_outline)

    elif pinned == False:
        pinned = True
        root_turtle.attributes('-topmost',True)
        button_pin.configure(image = img_pin_filled)


def on_extend_left():
    global button_extend_left, frame_left

    w = root_turtle.winfo_width()
    h = root_turtle.winfo_height()

    frame_left.update_idletasks()

    if button_extend_left['text'] == "<":
        frame_left.grid(row = 0, column = 0, rowspan = 3, sticky = NSEW)
        new_w = w + frame_left.winfo_width()
        button_extend_left.configure(text = ">")
    elif button_extend_left['text'] == ">":
        new_w = w - frame_left.winfo_width()
        frame_left.grid_forget()
        button_extend_left.configure(text = "<")

    root_turtle.geometry(f"{new_w}x{h}")


def on_extend_right():
    global button_extend_right, frame_right

    w = root_turtle.winfo_width()
    h = root_turtle.winfo_height()

    frame_right.update_idletasks()
    
    if button_extend_right['text'] == ">":
        frame_right.grid(row = 0, column = 2, rowspan = 3, sticky = NSEW)
        new_w = w + frame_right.winfo_width()
        button_extend_right.configure(text = "<")
    elif button_extend_right['text'] == "<":
        new_w = w - frame_right.winfo_width()
        frame_right.grid_forget()
        button_extend_right.configure(text = ">")
        
    root_turtle.geometry(f"{new_w}x{h}")


def on_color_chooser():
    try:
        clr_dark = colorchooser.askcolor(title ="Choose DARK square color", color = game.dark_square_clr)[0]
        if clr_dark is None:
            return
    except:
        return
        
    game.dark_square_clr = rgb_to_hex(clr_dark)
    game.configure_game()


def on_volume_toggle():
    global volume_toggle, button_volume_toggle
    if volume_toggle == True:
        volume_toggle = False
        button_volume_toggle.configure(image = img_volume_off)
    elif volume_toggle == False:
        volume_toggle = True
        button_volume_toggle.configure(image = img_volume_on)


def on_flip():
    global label_white_timer_top, label_white_timer_bottom, label_black_timer_top, label_black_timer_bottom
    
    if mode_of_play == "offline":
        global button_white_resign, button_black_resign
    
    if game.white == True:
        game.white = False
        game.black = True
        
        label_white_timer_bottom.grid_forget()
        label_white_timer_top.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)
        label_black_timer_top.grid_forget()
        label_black_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)

        if mode_of_play == "offline":
            button_white_resign.grid(row = 0, column = 0, sticky = NSEW)
            button_black_resign.grid(row = 2, column = 0, sticky = NSEW)
        
    elif game.black == True:
        game.black = False
        game.white = True

        label_white_timer_top.grid_forget()
        label_white_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)
        label_black_timer_bottom.grid_forget()
        label_black_timer_top.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)

        if mode_of_play == "offline":
            button_white_resign.grid(row = 2, column = 0, sticky = NSEW)
            button_black_resign.grid(row = 0, column = 0, sticky = NSEW)
        

    game.configure_game()


def on_game_over():

    #Emptying legal addresses list
    game.legaladd = []
    
    #Generating pgn
    game.generate_pgn()

    #Permanently removing extend left
    frame_left.grid_forget()
    button_extend_left.configure(text = "<")
    button_extend_left.grid_forget()
    on_scale_board_release(None)

    if mode_of_play == 'online':
        r = requests.get(geturl('connection') , params={'code':code}).json()['move durations']
        game.move_duration = r
        if challenger:
            requests.get(geturl('connection') , params={'code':code , 'clean':True})

    #Disabling mouse activity on the turtle canvas
    game.mouse_vacant = False
    wn.onclick(lambda x,y: None)
    canvas_turtle.unbind("<ButtonPress>")
    canvas_turtle.unbind("<B1-Motion>")
    canvas_turtle.unbind("<ButtonRelease-1>")
    
    #Displaying the result in the status bar
    if game.game_result == "W":
        root_turtle.title(f'*{white_name} vs {black_name}')
    elif game.game_result == "B":
        root_turtle.title(f'{white_name} vs *{black_name}')
    elif game.game_result == "D":
        root_turtle.title(f'*{white_name} vs *{black_name}')
        on_draw(False)
    elif game.game_result == "S":
        root_turtle.title(f'#{white_name} vs #{black_name}')

    #Pause the Timers


    #Adding game to database
    game.add_to_db(game.game_date, game.game_start_time, white_name, black_name, game.game_result, logic.List_of_Moves, game.move_duration , min_time,  increment)


def on_draw(confirm = True):
    global draw, draw_boundary, button_extend_left, frame_left, draw_offer
    if confirm:
        if mode_of_play == "offline":
            choice = messagebox.askyesno('Draw agreement', 'Do you both agree?')
            if not choice:
                return 
        elif mode_of_play == "online":
            requests.post(geturl('connection') , data= {'code':code, 'side':player_side, 'draw':player_side})
            while 1:
                try :
                    connectoption = True if (int(time.time())%30 == 0 and int(time.time()) != game.t0) else False
                    if connectoption:
                        game.t0 = int(time.time())

                    r = requests.get(geturl('connection') , params= {'side' : player_side , 'code' : code , 'connectop':connectoption})
                    time.sleep(0.2)
                    info = r.json()['offers']['draw offers']
                    if info in ('accepted' , 'rejected'):
                        break
                except:
                    pass
            requests.post(geturl('connection') , params = {'code' : code , 'reset':None})
            if info == 'rejected':
                return

        game.game_result = "D"

        on_game_over()

    #Display draw with a green border around the board
    try:
        draw_boundary.clear()
        wn.update()
    except:
        pass

    
    wn.tracer(0)
    draw_boundary=turtle.Turtle()
    draw_boundary.ht()
    draw_boundary.width(7)
    draw_boundary.color("green")
    draw_boundary.pu()
    draw_boundary.goto(-(game.size/2)+game.drift,(game.size/2))
    draw_boundary.pd()
    for _ in range(4):
        draw_boundary.fd(game.size)
        draw_boundary.rt(90)
    wn.tracer(1)

    def on_turtle_close():
        global program_running
        program_running = False
        root_turtle.after(500, lambda: root_turtle.destroy())
        database_functions.close_connection()
    
    root_turtle.protocol("WM_DELETE_WINDOW", on_turtle_close)


def on_white_resign():
    global button_extend_left, frame_left, move_duration
    
    if mode_of_play == "offline":
        choice = messagebox.askyesno('White resign', f'Are you ({white_name}) sure?')
        if not choice:
            return 
    elif mode_of_play == "online":
        if messagebox.askyesno('White resign' , f'Are you sure?'):
            requests.post(geturl('connection') , data = {'resign' : 'idk' ,'side' : 'white' ,'code' : code})
        else:
            return

    game.game_result = "B"

    on_game_over()


def on_black_resign():
    global button_extend_left, frame_left, move_duration, player_side, challenger

    if mode_of_play == "offline":
        choice = messagebox.askyesno('Black resign', f'Are you ({black_name}) sure?')
        if not choice:
            return 
    elif mode_of_play == "online":
        if messagebox.askyesno('Black resign', f'Are you sure?'):
            requests.post(geturl('connection') , data = {'resign' : 'idk' ,'side' : 'black' ,'code' : code})
        else:
            return 

    game.game_result = "W"

    on_game_over()


def on_legal_moves():
    global button_legal_moves, img_legal_moves_off, img_legal_moves_on
    if game.legalmoves == True:
        game.legalmoves = False
        button_legal_moves.configure(image = img_legal_moves_off)
    elif game.legalmoves == False:
        game.legalmoves = True
        button_legal_moves.configure(image = img_legal_moves_on)
    
    if game.legalmoves==True and game.move_stage==1:
        for m,n in game.legaladd:
            blm, bln=7-m, 7-n
            game.change_square_clr(m, n, blm, bln, constant.LEGALLIGHTSQUARECLR, constant.LEGALDARKSQUARECLR, update=False)
        wn.tracer(1)
    elif game.legalmoves==False and game.move_stage==1:
        for m,n in game.legaladd:
            blm, bln=7-m, 7-n
            game.change_square_clr(m, n, blm, bln, game.light_square_clr, game.dark_square_clr, update=False)
        wn.tracer(1)


def on_code_copy():
    global code
    if os.sys.platform.lower() == 'win32':
        clipboard.copy(code)

    else:
        os.system(f'echo -n "{code}" | xclip -selection clipboard')


def setup_game():
    global canvas_turtle, touch_move, var_board_scaler, scale_board, mode_of_play, pinned, img_pin_outline, img_pin_filled, button_pin, img_color_chooser, img_flip, img_draw, img_resign, volume_toggle, button_volume_toggle, img_volume_on, img_volume_off, button_extend_left, button_extend_right, frame_left, frame_right, label_white_timer_top, label_white_timer_bottom, label_black_timer_top, label_black_timer_bottom, img_legal_moves_on, img_legal_moves_off, button_legal_moves, img_touch_move_on, img_touch_move_off, button_color_chooser, button_flip, frame_moves, chess_not_row, button_white_resign, button_black_resign, button_resign, img_copy, frame_pgn
    
         
    #Configuring root_turtle
    root_turtle.configure(bg = constant.LIGHTBGCLR)

    #Reconfiguring minsize of the window
    root_turtle.minsize(0,0)
    root_turtle.resizable(width = False, height = False)
    root_turtle.overrideredirect(False)
    root_turtle.withdraw()
    root_turtle.deiconify()

    #Gridding root_turtle
    root_turtle.grid_rowconfigure(0, weight = 0)
    root_turtle.grid_columnconfigure(0, weight = 0)
    root_turtle.grid_rowconfigure(1, weight = 1)
    root_turtle.grid_columnconfigure(1, weight = 1)

    #Placing canvas_turtle inside root_turtle
    canvas_turtle.grid(row = 1, column = 1, sticky = NSEW)

    #Giving a background colour to wn
    wn.bgcolor("#000000")

    #Adding all the other elements present during the game (except timers)
    
    #Creating all the frames for the 4 sides
    frame_top = Frame(root_turtle, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    frame_bottom = Frame(root_turtle, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    frame_left = Frame(root_turtle, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    frame_right = Frame(root_turtle, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)

    #Adding all the frames to the screenready_to_play = True 
    frame_top.grid(row = 0, column = 1, sticky = NSEW)
    frame_bottom.grid(row = 2, column = 1, sticky = NSEW)

    #Gridding all the frames
    frame_top.grid_columnconfigure((2,3,4), weight = 1)
    frame_bottom.grid_columnconfigure((0,1,2), weight = 1)
    frame_left.grid_rowconfigure((0,1,2), weight = 1)
    frame_right.grid_rowconfigure(0, weight = 1)
    frame_right.grid_columnconfigure(0, weight = 1)

    button_extend_left = Button(frame_top, text = "<", font = ('consolas', 20, 'bold'), bg = constant.LIGHTBGCLR, fg = constant.LIGHTBGTEXTCLR, activebackground = constant.LIGHTBGCLR, activeforeground = constant.LIGHTBGTEXTCLR, command = on_extend_left, bd = 0, highlightthickness = 0)
    button_extend_left.grid(row = 0, column = 0, sticky = NSEW, padx = (0,1))

    button_extend_right = Button(frame_top, text = ">", font = ('consolas', 20, 'bold'), bg = constant.LIGHTBGCLR, fg = constant.LIGHTBGTEXTCLR, activebackground = constant.LIGHTBGCLR, activeforeground = constant.LIGHTBGTEXTCLR, command = on_extend_right, bd = 0, highlightthickness = 0)
    button_extend_right.grid(row = 0, column = 5, sticky = NSEW, padx = (1,0))

    #Adding frame_moves to frame_right
    frame_moves = ScrolledFrame(frame_right, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0, max_height = 1000)
    frame_moves.grid(row = 0, column = 0, sticky = NSEW, padx = 2, pady = 2, ipadx = 2, ipady = 2)
    
    #Gridding frame_moves.viewPort
    frame_moves.viewPort.grid_columnconfigure((1,2), weight = 1)

    #Adding frame_pgn for copying and downloading pgn of the game after it gets over
    frame_pgn = Frame(frame_right, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    frame_pgn.grid_columnconfigure(0, weight = 1)
    frame_pgn.grid(row = 1, column = 0, sticky = NSEW)
    
    #Initialising chess_not_row
    chess_not_row = 0

    #Adding the board scaler to frame_top
    var_board_scaler = IntVar()
    scale_board = ttk.Scale(frame_top, variable = var_board_scaler, from_ = 30, to = 70, orient = HORIZONTAL)
    var_board_scaler.set(50)

    scale_board.bind("<ButtonRelease-1>", on_scale_board_release)
    scale_board.grid(row = 0, column = 4, sticky = EW, padx = 5)
    
    #Adding the pin to frame_top
    img_pin_outline = PhotoImage(file = "./Icons/pin_outline.png").subsample(15,15)
    img_pin_filled = PhotoImage(file = "./Icons/pin_filled.png").subsample(15,15)

    button_pin = Button(frame_top, image = img_pin_outline, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_pin_toggle, bd = 0, highlightthickness = 0)
    pinned = False
    button_pin.grid(row = 0, column = 1, sticky = NSEW, padx = 2)

    #Creating frame_icons to contain all the icons
    frame_icons = Frame(frame_bottom, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    
    #Adding frame_icons to the screen
    frame_icons.grid(row = 0, column = 0, sticky = NSEW, padx = 5)
    
    #Gridding frame_icons
    frame_icons.grid_columnconfigure((0,1,2,3,4), weight = 1)

    #Adding the color chooser icon to frame_bottom
    img_color_chooser = PhotoImage(file = "./Icons/color_chooser.png").subsample(3,3)
    button_color_chooser = Button(frame_icons, image = img_color_chooser, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_color_chooser, bd = 0, highlightthickness = 0)

    #Adding volume toggle icon to frame_bottom
    img_volume_on = PhotoImage(file = "./Icons/volume_on.png").subsample(4,4)
    img_volume_off = PhotoImage(file = "./Icons/volume_off.png").subsample(4,4)
    volume_toggle = True
    button_volume_toggle = Button(frame_icons, image = img_volume_on, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_volume_toggle, bd = 0, highlightthickness = 0)
    

    #Adding flip icon to frame_bottom
    img_flip = PhotoImage(file = "./Icons/flip.png").subsample(3,3)
    button_flip = Button(frame_icons, image = img_flip, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_flip, bd = 0, highlightthickness = 0)
    
    #Adding the legal moves icon to frame_bottom
    img_legal_moves_on = PhotoImage(file = "./Icons/arrows_on.png")
    img_legal_moves_off = PhotoImage(file = "./Icons/arrows_off.png")
    button_legal_moves = Button(frame_icons, image = img_legal_moves_on, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_legal_moves, bd = 0, highlightthickness = 0)

    #Adding draw icon to frame_left
    img_draw = PhotoImage(file = "./Icons/draw.png").subsample(16, 16)
    button_draw = Button(frame_left, image = img_draw, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_draw, bd = 0, highlightthickness = 0)

    #Adding resign icon to frame_left
    img_resign = PhotoImage(file = "./Icons/flag.png").subsample(3,3)
    
    #Adding the info about if touch move is enabled or disabled
    img_touch_move_on = PhotoImage(file = "./Icons/touch_move_on.png")
    img_touch_move_off = PhotoImage(file = "./Icons/touch_move_off.png")
    
    label_touch_move = Label(frame_icons, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    
    #Adding the room code copy button only for challenger if online
    img_copy = PhotoImage(file = "./Icons/clipboard.png").subsample(3,3)
    if challenger:
        button_code_copy = Button(frame_icons, image = img_copy, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_code_copy, bd = 0, highlightthickness = 0)
        button_code_copy.grid(row = 0, column = 5, sticky = NSEW)
        Tooltip(button_code_copy, text = f"Copy room code: {code}")

    if touch_move:
        label_touch_move.configure(image = img_touch_move_on)
        Tooltip(label_touch_move, text = "Touch move enabled")
    elif not touch_move:
        label_touch_move.configure(image = img_touch_move_off)
        Tooltip(label_touch_move, text = "Touch move disabled")
        
    if mode_of_play == "online":
        button_resign = Button(frame_left, image = img_resign, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
        button_resign.grid(row = 0, column = 0, sticky = NSEW)
        if player_side == "white":
            button_resign.configure(command = on_white_resign)
        elif player_side == "black":
            button_resign.configure(command = on_black_resign)

        Tooltip(button_resign, text = "Resign")
    elif mode_of_play == "offline":
        button_white_resign = Button(frame_left, image = img_resign, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_white_resign, bd = 0, highlightthickness = 0)
        button_black_resign = Button(frame_left, image = img_resign, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_black_resign, bd = 0, highlightthickness = 0)
        button_white_resign.grid(row = 2, column = 0, sticky = NSEW)
        button_black_resign.grid(row = 0, column = 0, sticky = NSEW)
        Tooltip(button_white_resign, text = "White resign")
        Tooltip(button_black_resign, text = "Black resign")


    #Adding all the icons to frame_icons
    button_color_chooser.grid(row = 0, column = 0, sticky = NSEW)
    button_volume_toggle.grid(row = 0, column = 1, sticky = NSEW)
    button_flip.grid(row = 0, column = 2, sticky = NSEW)
    button_legal_moves.grid(row = 0, column = 3, sticky = NSEW)
    label_touch_move.grid(row = 0, column = 4, sticky = NSEW)
    
    #Adding button_draw to frame_left
    button_draw.grid(row = 1, column = 0, sticky = NSEW)

    #Adding the timer labels to frame_top and frame_bottom
    start_time = tfor(int(min_time)*60 if min_time.isdigit() else 0)[:-2]
    label_white_timer_top = Label(frame_top, text = start_time, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('consolas', 15, 'bold'), bd = 2)
    label_white_timer_bottom = Label(frame_bottom, text = start_time, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('consolas', 15, 'bold'), bd = 2)

    label_black_timer_top = Label(frame_top, text =  start_time, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('consolas', 15, 'bold'), bd = 2)
    label_black_timer_bottom = Label(frame_bottom, text = start_time, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('consolas', 15, 'bold'), bd = 2)

    if mode_of_play == "offline":
        label_white_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)
        label_black_timer_top.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)
    elif mode_of_play == "online":
        if player_side == "white":
            label_white_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)
            label_black_timer_top.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)
        elif player_side == "black":
            label_white_timer_top.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)
            label_black_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 2)

    #Adding tooltips for the required widgets
    Tooltip(button_flip, text = "Switch view")
    Tooltip(button_volume_toggle, text = "Toggle sound")
    Tooltip(button_color_chooser, text = "Change square colour")
    Tooltip(button_pin, text = "Toggle pin window")
    Tooltip(button_legal_moves, text = "Toggle legal moves")
    Tooltip(scale_board, text = "Scale board size")

    if mode_of_play == "offline":
        Tooltip(button_draw, text = "Draw")
    elif mode_of_play == "online":
        Tooltip(button_draw, text = "Offer draw")
    

    for _ in range(2):
        on_extend_left()
        on_extend_right()
    
    if challenger:
        if not received:
            if player_side == "white":
                root_turtle.title(f'{code}: {player_name} vs (waiting...) ') 
            elif player_side == "black":
                root_turtle.title(f'{code}: (waiting...) vs {player_name}')
    elif challenger is None: #Offline
        root_turtle.title(f'{white_name} vs {black_name}')


    game.game_main(touch_move)


def about():
    global img_back, frame_about, canvas_main_menu, text_about_info, bind_configure
    destroy_all_widgets_in_canvas_main_menu()

    def on_back():
        global canvas_main_menu, bind_configure, frame_about
        frame_about.unbind("<Configure>", bind_configure)
        frame_about.destroy()
        destroy_all_widgets_in_canvas_main_menu()
        canvas_main_menu.destroy()
        main_menu()
    
    def on_frame_about_configure(e):
        global text_about_info, frame_about
        frame_about.viewPort.update_idletasks()
        #text_about_info.configure(width = frame_about.viewPort.winfo_width() - 20)

    #Gridding canvas_main_menu
    canvas_main_menu.grid_rowconfigure((0,1,2), weight = 0)
    canvas_main_menu.grid_columnconfigure((0,1,2), weight = 0)
    canvas_main_menu.grid_rowconfigure(1, weight = 1)
    canvas_main_menu.grid_columnconfigure(1, weight = 1)

    #Creating, gridding and adding frame_about to canvas_main_menu
    frame_about = ScrolledFrame(canvas_main_menu, bg = constant.DARKBGCLR, bd = 0, highlightthickness = 0, max_height = 500)
    frame_about.grid(row = 1, column = 1, sticky = 'new', padx = (0,60), pady = (0, 60))
    frame_about.viewPort.grid_rowconfigure(0, weight = 1)
    frame_about.viewPort.grid_columnconfigure(0, weight = 1)
    frame_about.viewPort.update_idletasks()

    #Adding the title to the about page
    Label(canvas_main_menu, text = "ABOUT        ", font = ('Algerian', 30, 'bold'), bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, bd = 0, highlightthickness = 0).grid(row = 0, column = 1, sticky = NSEW)

    text_about_info = Text(frame_about.viewPort, font = ('Comic Sans', 18), bg = constant.LIGHTBGCLR, fg = constant.LIGHTBGTEXTCLR, bd = 0, highlightthickness = 20, highlightcolor = constant.LIGHTBGCLR, highlightbackground = constant.LIGHTBGCLR, wrap = WORD)
    text_about_info.insert(INSERT, constant.ABOUT_INFO)
    text_about_info.config(state = DISABLED)
    text_about_info.grid(row = 0, column = 0, sticky = NSEW, ipadx = 20, ipady = 20)
    bind_configure = frame_about.bind("<Configure>", on_frame_about_configure, add = "+")

    #Adding a back button
    img_back = PhotoImage(file = "./Icons/back.png").subsample(2,2)
    button_back = Button(canvas_main_menu, image = img_back, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, activebackground = constant.DARKBGCLR, activeforeground = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), command = on_back, bd = 0, highlightthickness = 0)
    button_back.grid(row = 0, column = 0, sticky = W, padx = 5)

    
#Called by main.py
def main():
    #Setting up the screen
    global geturl, wn, root_turtle, canvas_turtle, program_running, theme_bg, url, game_result, img_pocket_chess_arena_icon, draw_offer, max_board_size
    wn=turtle.Screen()
    wn.colormode(255)
    wn.bgcolor('black')
    wn.title("Pocket Chess Arena")
    wn.tracer(1)
    program_running = True
    
    ip = '10.0.5.70'
    port = 5001
    # url = f'http://{ip}:{port}/'
    url = 'https://srams.pythonanywhere.com/'
    
    geturl = lambda x : url + x
    draw_offer = None

    #Getting the canvas and top level window from wn
    canvas_turtle = wn.getcanvas() 
    canvas_turtle.configure(bd = 0, highlightthickness = 0)
    root_turtle = canvas_turtle.winfo_toplevel() 
    
    #Setting the minsize of root_turtle
    root_turtle.minsize(850, 550)
    
    #Setting the size of root_turtle
    root_turtle_width = 1050
    root_turtle_height = 650
    root_turtle.geometry(f'{root_turtle_width}x{root_turtle_height}')
    root_turtle.resizable(width = False, height = False)

    #Setting the title bar icon
    img_pocket_chess_arena_icon = PhotoImage(file = "./Icons/pocket_chess_arena_logo.png")
    root_turtle.iconphoto(False, img_pocket_chess_arena_icon)

    #Adjusting the resolution 
    if os.sys.platform == 'win32':
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    
    #Setting up scollbars for the turtle window
    #wn.screensize(root_turtle.winfo_width(), root_turtle.winfo_height())
    
    #Getting the max board size
    screen_height = get_monitors()[0].height
    max_board_size = screen_height - 300
    
    #Storing the shapes of all the pieces
    wn.register_shape("Pawn", constant.COORD["pawn"])
    wn.register_shape("Horse", constant.COORD["horse"])
    wn.register_shape("Bishop", constant.COORD["bishop"])
    wn.register_shape("Queen", constant.COORD["queen"])
    wn.register_shape("King", constant.COORD["king"])
    wn.register_shape("Rook", constant.COORD["rook"])

    #Changing the default font of combobox drop downs. This font size looks good only on the home page. It will be changed later for the other pages.
    font_combo_listbox = font.Font(family="Algerian", size = 17, weight = "normal")
    root_turtle.option_add("*TCombobox*Listbox*Font", font_combo_listbox)

    #Configuration Variables
    global touchpieceval, vocalval, whiteview, blackview, doubleview
    touchpieceval, vocalval, whiteview, blackview, doubleview=None,None,None,None,None
    
    #Timer Variables
    global timer_name, timer_cords , neutral_bound , active_bound , timer_bound ,active_bound_width , neutral_bound_width
    timer_name = []
    
    neutral_bound = '#ffe599'
    active_bound = '#2315D4'
    active_bound_width = 8
    neutral_bound_width = 4

    timer_cords = {
                    'doubleview':[(-365,-330),(220,-330)],
                    'whiteview':[(353,-142),(353,142)],
                    'blackview':[(353,142),(353,-142)]
            }

    timer_bound = {
                    'doubleview':{
                                    'black':[(207,-298),(360,-328)],
                                    'white':[(-376,-296),(-227,-327)]
                            },
                    'blackview':{
                                    'white':[(343,177),(482,142)],
                                    'black':[(343,-107),(482,-142)]
                            },
                    'whiteview':{
                                    'black':[(343,177),(482,142)],
                                    'white':[(343,-107),(482,-142)]
                            }
    }
    main_menu()
    turtle.mainloop()

