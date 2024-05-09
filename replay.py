#Import of Modules
import datetime
import turtle
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from functools import partial
from playsound import playsound
from tkinter import colorchooser
from utils import Tooltip, lighten_color, rgb_to_hex, ScrolledFrame, get_chess_notation, tfor, show_labels
import clipboard
import os

#Import of created files
import home
import constant
import database_functions
import logic
  
def save_configuration(replay_match_number, config_no):
    global active_save_configuration_number, root_saved_configurations, root_save_configuration
    try:   
        if config_no == active_save_configuration_number:
            return None
        else:
            root_save_configuration.destroy()
    except:
        pass        

    active_save_configuration_number = config_no
    
    root_save_configuration=Tk()
    root_save_configuration.title("Save Current Configuration")
    #root_save_configuration.iconphoto(False, home.img_pocket_chess_arena_icon)
    
    size=(450, 500)
    xoffset = int(3/5.6 * home.root_turtle.winfo_screenwidth())
    yoffset = int(1/7 * home.root_turtle.winfo_screenheight())
    root_save_configuration.geometry(f"{size[0]}x{size[1]}+{xoffset}+{yoffset}")
    root_save_configuration.resizable(width=False, height=False)

    
    def on_closing():
        global active_save_configuration_number
        active_save_configuration_number = None
        root_save_configuration.destroy()
    
    root_save_configuration.protocol("WM_DELETE_WINDOW", on_closing)

    top_frame = Frame(root_save_configuration)
    top_frame.pack(side=TOP, fill='x')
    top_frame.columnconfigure((0,1,2,3,4), weight=1)
    title_text=StringVar(top_frame)
    title_text.set("TITLE")
    title_entry = Entry(top_frame, font=("Comic Sans", 18, 'bold'), textvariable = title_text, relief="groove", bd=3)
    title_entry.grid(row=0, column=1, columnspan=3, sticky="WE")
    
    def onSaveButtonClick():
        global active_save_configuration_number
        
        #Title Validation
        if len(title_entry.get().rstrip()) > 150:
            messagebox.showerror('Error', 'Max Chars Allowed:\n150')
            return None

        for i in range(len(title_entry.get().rstrip())):
            if title_entry.get().rstrip()[i] in ("\"", ",", "(", ")"):
                messagebox.showerror('Error', 'Invalid Chars-\nRound Brackets ( )\nComma ,\nDouble Quotes "')
                return None

        #Notes Validation
        if len(notes_entry.get(1.0, "end-1c").rstrip()) > 1500:
            messagebox.showerror('Error', 'Max Chars Allowed:\n1500')
            return None

        for i in range(len(notes_entry.get(1.0, "end-1c").rstrip())):
            if notes_entry.get(1.0, "end-1c").rstrip()[i] in ("\"", ",", "(", ")"):
                messagebox.showerror('Error', 'Round Brackets\nComma\nDouble Quotes')
                return None
        
        if database_functions.check_connection()==False:
            database_functions.open_connection()
        if database_functions.check_connection()==True:
            database_functions.update_configuration_saved(replay_match_number, config_no, title_entry.get().rstrip(), notes_entry.get(1.0, "end-1c").rstrip())
        else:
            messagebox.showerror("Error", "Check your internet connection and try again.")
            return None
                    
        active_save_configuration_number = None
        root_save_configuration.destroy()

        try:
            root_saved_configurations.destroy()
            show_saved_configurations(replay_match_number)
        except:
            pass

    ttk.Button(top_frame, text="SAVE",command=onSaveButtonClick).grid(row=0, column=4)

    main_frame = Frame(root_save_configuration, relief="ridge", bd=3)
    main_frame.pack(side=TOP, fill='both', expand=True)

    scrollbar = Scrollbar(main_frame, orient ="vertical")
    scrollbar.pack(side="right", fill="y")
    
    notes_entry = Text(main_frame, font=("Consolas", 15, 'normal'), wrap = 'word', height = main_frame.winfo_height(), yscrollcommand=scrollbar.set)
    notes_entry.pack(fill="both", expand=True)

    saved_configuration_numbers=()
    for i in database_functions.receive_configurations_saved(replay_match_number):
        saved_configuration_numbers+=(i[1],)
    
    if config_no in saved_configuration_numbers:
        for i in database_functions.receive_configurations_saved(replay_match_number):
            if i[1]==config_no:
                title_text.set(i[2])
                title_entry.configure(textvariable=title_text)
                notes_entry.insert(INSERT, i[3])
    else:
        notes_entry.insert(INSERT, "NOTES")

    scrollbar.config(command = notes_entry.yview)


def show_saved_configurations(replay_match_number):
    global root_saved_configurations
    
    try:
        root_saved_configurations.destroy()
    except:
        pass

    root_saved_configurations = Tk()
    root_saved_configurations.title("Saved Configurations")
    #root_saved_configurations.iconphoto(False, home.img_pocket_chess_arena_icon)
    
    size=(500, 600)
    xoffset = int(3/5.6 * home.root_turtle.winfo_screenwidth())
    yoffset = int(1/15 * home.root_turtle.winfo_screenheight())
    root_saved_configurations.geometry(f"{size[0]}x{size[1]}+{xoffset}+{yoffset}")
    root_saved_configurations.resizable(width=False, height=True)
    

    configs=()
    titles=()
    notes=()
    for i in database_functions.receive_configurations_saved(replay_match_number):
        configs+=(i[1],)
        titles+=(i[2],)
        notes+=(i[3],)
    
    #Creating main_frame in which all the contents of saved_configuration will be present
    main_frame = ScrolledFrame(root_saved_configurations, max_height = size[1])
    main_frame.pack(fill = 'both', expand = True)

    
    for i in range(len(titles)):
        frame=Frame(main_frame.viewPort, height=300, relief="raised", bd=5)
        frame.pack(fill='x')
        title_text=scrolledtext.ScrolledText(frame, font=('Consolas', 16, 'bold'), relief='sunken', bd=3, height=0.5, wrap = 'word')
        title_text.pack(fill=X)
        notes_text=scrolledtext.ScrolledText(frame, font=('Consolas', 13,'normal'), height=7, wrap = 'word')
        notes_text.pack(fill=X)

        notes_text.insert(INSERT, notes[i].rstrip())
        title_text.insert(INSERT, titles[i].rstrip())

        title_text.configure(state='disabled')
        notes_text.configure(state='disabled')

        #Button_no are separately numbered for the show, edit and delete buttons. Button_no starts from 0 just like i.
        def onShowButtonClick(button_no):
            configure_pieces(configs[button_no])
            home.wn.tracer(1)
            root_saved_configurations.lift()
            root_saved_configurations.attributes("-topmost", True)

        def onEditButtonClick(button_no):
            save_configuration(replay_match_number, configs[button_no])
            root_saved_configurations.attributes("-topmost", False)

        def onDeleteButtonClick(button_no):
            database_functions.delete_configuration(replay_match_number, configs[button_no])
            root_saved_configurations.destroy()
            show_saved_configurations(replay_match_number)
    

        button_frame=Frame(frame)
        show_button = ttk.Button(button_frame, text='SHOW', command = partial(onShowButtonClick, i))
        edit_button = ttk.Button(button_frame, text='EDIT', command = partial(onEditButtonClick, i))
        delete_button = ttk.Button(button_frame, text='DELETE', command = partial(onDeleteButtonClick, i))
        
        show_button.grid(row=0, column=0, sticky='WE')
        edit_button.grid(row=0, column=1, sticky='WE')
        delete_button.grid(row=0, column=2, sticky='WE')
        button_frame.pack()
        
        Label(main_frame, text="      ").pack(side=TOP, fill='x')

    
def games_played():
    global main_frame, label_title, entry_frame, button_back, frame_top

    def onButtonClick():
        global error_alert, main_frame, label_title, entry_frame, button_back, frame_top
        try:
            desired_match_number = int(match_number_replay.get())
        except:
            desired_match_number = match_number_replay.get()

        if desired_match_number in possible_match_numbers:
            global root_internet_problem
            try:
                error_alert.grid_forget()
            except:
                pass
            
            try:
                root_internet_problem.destroy()
            except:
                pass

            if database_functions.check_connection()==False:
                database_functions.open_connection()
            if database_functions.check_connection()==True:
                val = match_number_replay.get()
                label_title.destroy()
                frame_top.destroy()
                main_frame.destroy()
                entry_frame.destroy()
                button_back.destroy()
                home.root_turtle.grid_columnconfigure((0,1,2,3), weight = 0)
                home.root_turtle.grid_rowconfigure((0,1,2,3), weight = 0)
                setup_replay()
                replay_main(val)
                
            else:
            
                root_internet_problem = Tk()
                root_internet_problem.title("Error")
                
                size = (250, 70)
                xoffset = int(home.root_turtle.winfo_width()/2 - size[0]/2)
                yoffset = int(home.root_turtle.winfo_height()/2 - size[1]/2)
                root_internet_problem.geometry(f"{size[0]}x{size[1]}+{xoffset}+{yoffset}")
                root_internet_problem.resizable(width=False, height=False)
                root_internet_problem.attributes('-topmost', True)

                ttk.Label(root_internet_problem, text="Check your internet connection and try again.", width = size[0]).pack(fill='x', side='top')

                def onOkayButtonClick():
                    root_internet_problem.destroy()
                
                ttk.Button(root_internet_problem, text='OK', command=onOkayButtonClick).pack(side='bottom')
            
        else:
            error_alert = Label(entry_frame, text="Invalid Match Number", font = ('Comic Sans', 16, 'bold'), bg = constant.DARKBGCLR, fg="red")
            error_alert.grid(row=0, column=3)
        
    def on_back():
        global main_frame, label_title, frame_top, entry_frame, button_back
        label_title.destroy()
        frame_top.destroy()
        main_frame.destroy()
        entry_frame.destroy()
        button_back.destroy()
        
        #Setting the size of root_turtle
        root_turtle_width = 1050
        root_turtle_height = 650
        home.root_turtle.geometry(f'{root_turtle_width}x{root_turtle_height}')
        home.root_turtle.overrideredirect(False)
        home.root_turtle.withdraw()
        home.root_turtle.deiconify()
        home.root_turtle.resizable(width = False, height = False)
    
        home.root_turtle.grid_columnconfigure((0,1,2,3), weight = 0)
        home.root_turtle.grid_rowconfigure((0,1,2,3), weight = 0)
        home.main_menu()

    def on_turtle_close():
        home.program_running = False
        home.root_turtle.destroy()
        database_functions.close_connection()

    home.root_turtle.protocol("WM_DELETE_WINDOW", on_turtle_close)

    #Configuring root_turtle
    home.root_turtle.configure(bg = constant.DARKBGCLR)
    home.root_turtle.title("Pocket Chess Arena")
    home.root_turtle.attributes('-topmost', False)
    home.root_turtle.resizable(width = True, height = True)
    
    #Gridding root_turtle
    home.root_turtle.grid_columnconfigure(0, weight = 1)
    home.root_turtle.grid_rowconfigure(1, weight = 1)
    
    home.wn.clearscreen()

    frame_top = Frame(home.root_turtle, bg = constant.DARKBGCLR, bd = 0, highlightthickness = 0)
    frame_top.grid(row = 0, column = 0, sticky = NSEW)
    frame_top.grid_columnconfigure(1, weight = 1)
    frame_top.grid_rowconfigure((0,1), weight = 1)
    
    label_title = Label(frame_top, text="GAMES PLAYED", font = ("Algerian", 30, 'bold'), bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR)
    label_title.grid(row = 0, column = 1, sticky = NSEW, padx = (10,90))
    
    #Adding the back button
    img_back = PhotoImage(file = "./Icons/back.png").subsample(2,2)
    button_back = Button(frame_top, image = img_back, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, activebackground = constant.DARKBGCLR, activeforeground = constant.DARKBGTEXTCLR, font = ('Consolas', 20, 'bold'), command = on_back, bd = 0, highlightthickness = 0)
    button_back.grid(row = 0, column = 0, sticky = W, padx = 10)

    #Creating Main Frame
    main_frame = ScrolledFrame(home.root_turtle, bg = constant.DARKBGCLR, max_height = 1000)
    main_frame.grid(row = 1, column = 0, sticky = NSEW)
            
    #Creating a frame to contain the entry box for accepting the match number
    entry_frame = Frame(frame_top, bg = constant.DARKBGCLR)
    entry_frame.grid(row = 1, column = 0, columnspan = 2, sticky = NSEW)
    
    #Gridding entry_frame
    entry_frame.grid_columnconfigure((0,4), weight = 1)

    Label(entry_frame, text = "MATCH NUMBER:", font=('Comic Sans', 16, 'bold'), bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR).grid(row = 0, column = 0, sticky = E , padx = (5,0) , pady = 5, ipadx = 5 , ipady = 2)
    match_number_replay = Entry(entry_frame, font = ('Comic Sans', 16))
    match_number_replay.grid(row = 0, column = 1, sticky = W, padx = (0,5), pady = 5, ipadx = 5 , ipady = 2)
    
    possible_match_numbers=()
    for i in database_functions.receive_all_game_details():
        possible_match_numbers+=(i[0],)

   
    Button(entry_frame, text="SHOW REPLAY", font = ('Comic Sans', 16, 'bold'), bg = constant.SECONDARYCLR, fg = constant.DARKBGTEXTCLR, command=onButtonClick).grid(row=0, column=2 , sticky = W, padx = 5 , ipadx = 5 , ipady = 2, pady = 5)


    #Creating empty space to the left of the canvas
    Label(main_frame, text="               ", bg = constant.DARKBGCLR).pack(side='left')

    #Creating empty to the right of the canvas
    Label(main_frame, text="          ", bg = constant.DARKBGCLR).pack(side='right')
    

    #Creating frame
    main_frame.viewPort.columnconfigure((0,1,2,3,4,5,6,7,8), weight=1)
    
    #Removing bd and highlightthickness
    main_frame.configure(bd = 0, highlightthickness = 0)
    main_frame.viewPort.configure(bd = 0, highlightthickness = 0)
    

    headings = ("MATCH NO.", "DATE", "START TIME", "END TIME", "DURATION", "WHITE", "BLACK")
    for i in range(len(headings)):
        Label(main_frame.viewPort, text=headings[i], font = ("Consolas", 18, 'bold'), bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, borderwidth = 2, relief="raised").grid(row=1, column=i+1, sticky ="WE")

    rownum=2
    for individual_match_details in database_functions.receive_all_game_details():
        colnum=1
        result = individual_match_details[:-2][7]
        for i in individual_match_details[:7]:                    
            label_val = Label(main_frame.viewPort, text=i, font = ("Consolas", 16, 'normal'), bg = constant.LIGHTBGCLR, fg = constant.LIGHTBGTEXTCLR, wraplength=180, justify="center", borderwidth = 1, relief="sunken")
            if (colnum == 6 and result == "W") or (colnum == 7 and result == "B"):
                label_val.config(bg = constant.WINNERCLR)
            elif (colnum == 6 and result == "B") or (colnum == 7 and result == "W"):
                label_val.config(bg = constant.LOSERCLR)
            elif result in ("D", "S") and colnum in (6,7):
                label_val.config(bg = constant.DRAWCLR)
            elif colnum == 2:
                label_val.config(text = i.strftime("%d-%b-%Y"))
            
            label_val.grid(row=rownum, column=colnum, sticky = NSEW, ipadx = 5, ipady = 5)
            colnum+=1
        rownum+=1

    home.root_turtle.mainloop()


def define_basic_global_variables(match_no, list_of_moves, list_of_times, min_time_, increment_):
    global size, sqsize, stretch_square, drift, verticaldrift, boardview, replay_list2d, list_piece_numbers, piece_count, move_count, replay_writeturtle, replay_match_number, replay_writeturtle, moves, times, emp, light_square_clr, dark_square_clr, min_time, increment, times_white, times_black, last_sec
    
    #Initialising a size for the chess board and a corresponding size for root_turtle
    length = (355 + home.max_board_size) / 2
    
    size_canvas_turtle = int(length) + 15
    size_root_turtle = size_canvas_turtle + 35
    home.canvas_turtle.configure(width = size_canvas_turtle, height = size_canvas_turtle)
    home.canvas_turtle.update()
    home.root_turtle.geometry(f"{size_root_turtle}x{size_root_turtle+95}")

    #Size of the chess board
    size = length
    
    #Size of 1 UNIT square in the chess board
    sqsize = size/8 

    #The value by which each unit square should be stretched.
    stretch_square = (size/8)/20 

    #Initialising drifts
    drift = 0
    verticaldrift = 0

    #Board View (Default is white)
    boardview="white"

    #Initialising the colours of the squares
    light_square_clr = constant.LIGHTSQUARECLR
    dark_square_clr = constant.DARKSQUARECLR

    #The replay for which match number is to be shown
    replay_match_number = match_no

    #Initialisation of some more variables
    replay_list2d=logic.copy_of_init_list2d()
    list_piece_numbers = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    piece_count = 0
    move_count = 0

    #Writer turtle of the replay page
    replay_writeturtle = turtle.Turtle()
    replay_writeturtle.ht()
    replay_writeturtle.pu()

    #Initialising the list of the moves made and the times taken
    moves = list_of_moves
    times = list_of_times
    print(times)
    times = [x for x in times if x.total_seconds() >= 0]

    #Initialsing min_time and increment
    min_time = min_time_
    increment = increment_

    #Initialising times_white and times_black
    times_white = times[0::2]
    times_black = times[1::2]

    #Defining emp which will be used as an element in replay_list2d
    emp=["", "", 0, 0]

    #last seconds
    last_sec = 20


def setup_replay():
    global canvas_turtle, var_board_scaler, scale_board, pinned, img_pin_outline, img_pin_filled, button_pin, img_color_chooser, img_flip, volume_toggle, button_volume_toggle, img_volume_on, img_volume_off, button_extend_right, img_save_configuration, img_saved_configurations, img_back, frame_top, frame_bottom, frame_right, img_left_arrow, img_right_arrow, label_white_timer_bottom, label_white_timer_top, label_black_timer_bottom, label_black_timer_top, frame_moves, frame_arrows, frame_pgn
    
    def on_scale_board_release(e):
        global scale_board, var_board_scaler, size, sqsize, stretch_square, button_extend_right
        
        length = (355 + home.max_board_size) / 2
        amplitude = home.max_board_size - length
        size = length + (var_board_scaler.get() - 50)/20 * amplitude
        sqsize = size / 8
        stretch_square=(size/8)/20
        configure_game()

        size_canvas_turtle = int(size) + 15
        size_root_turtle = size_canvas_turtle + 35
        home.canvas_turtle.configure(width = size_canvas_turtle, height = size_canvas_turtle)
        home.canvas_turtle.update()
        width_root_turtle = size_root_turtle
    
        if button_extend_right['text'] == "<":
            frame_right.update_idletasks()
            width_root_turtle += frame_right.winfo_width()
        
        home.root_turtle.geometry(f"{width_root_turtle}x{size_root_turtle+95}")
    

    def on_pin_toggle():
        global pinned, button_pin
        if pinned == True:
            pinned = False
            home.root_turtle.attributes('-topmost',False)
            button_pin.configure(image = img_pin_outline)

        elif pinned == False:
            pinned = True
            home.root_turtle.attributes('-topmost',True)
            button_pin.configure(image = img_pin_filled)


    def on_extend_right():
        global button_extend_right, frame_right

        w = home.root_turtle.winfo_width()
        h = home.root_turtle.winfo_height()

        frame_right.update_idletasks()

        if button_extend_right['text'] == ">":
            frame_right.grid(row = 0, column = 2, rowspan = 3, sticky = NSEW)
            new_w = w + frame_right.winfo_width()
            button_extend_right.configure(text = "<")
        elif button_extend_right['text'] == "<":
            new_w = w - frame_right.winfo_width()
            frame_right.grid_forget()
            button_extend_right.configure(text = ">")

        home.root_turtle.geometry(f"{new_w}x{h}")


    def on_color_chooser():
        global dark_square_clr, light_square_clr
        try:
            clr_dark = colorchooser.askcolor(title ="Choose DARK square color", color = dark_square_clr)[0]
            if clr_dark is None:
                return
        except:
            return
            
        dark_square_clr = rgb_to_hex(clr_dark)
        configure_game()


    def on_volume_toggle():
        global volume_toggle, button_volume_toggle
        if volume_toggle == True:
            volume_toggle = False
            button_volume_toggle.configure(image = img_volume_off)
        elif volume_toggle == False:
            volume_toggle = True
            button_volume_toggle.configure(image = img_volume_on)


    def on_flip():
        global boardview, label_white_timer_bottom, label_white_timer_top, label_black_timer_bottom, label_black_timer_top
        if boardview == "white":
            boardview = "black"

            if move_count != 0:
                label_white_timer_bottom.grid_forget()
                label_white_timer_top.grid(row = 0, column = 3, sticky = EW, padx = 5, ipady = 3)
                label_black_timer_top.grid_forget()
                label_black_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 3)
  
        elif boardview == "black":
            boardview = "white"
            if move_count != 0:
                label_white_timer_top.grid_forget()
                label_white_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 3)
                label_black_timer_bottom.grid_forget()
                label_black_timer_top.grid(row = 0, column = 3, sticky = EW, padx = 5, ipady = 3)

        configure_game()


    def on_back():
        global frame_top, frame_bottom, frame_right
        if database_functions.check_connection()==False:
            database_functions.open_connection()
        if database_functions.check_connection()==True:
            try:
                root_saved_configurations.destroy()
            except:
                pass
            home.wn.clearscreen()
            frame_top.destroy()
            frame_bottom.destroy()
            frame_right.destroy()
            home.canvas_turtle.grid(row = 0, column = 0)
            home.root_turtle.minsize(1050, 550)
            home.root_turtle.resizable(width = True, height = True)
            home.root_turtle.grid_columnconfigure((0,1,2,3), weight = 0)
            home.root_turtle.grid_rowconfigure((0,1,2,3), weight = 0)
            games_played()
        else:
            messagebox.showerror("Error", "Check your internet connection and try again.")
        

    def on_show_saved_configurations(replay_match_number):
        if database_functions.check_connection()==False:
            database_functions.open_connection()
        if database_functions.check_connection()==True:
            show_saved_configurations(replay_match_number)
        else:
            messagebox.showerror("Error", "Check your internet connection and try again.")


    #Configuring home.root_turtle
    home.root_turtle.configure(bg = constant.LIGHTBGCLR)

    #Reconfiguring minsize of the window
    home.root_turtle.minsize(0,0)
    home.root_turtle.resizable(width = False, height = False)
    home.root_turtle.overrideredirect(False)
    home.root_turtle.withdraw()
    home.root_turtle.deiconify()

    #Gridding home.root_turtle
    home.root_turtle.grid_rowconfigure(0, weight = 0)
    home.root_turtle.grid_columnconfigure(0, weight = 0)
    home.root_turtle.grid_rowconfigure(1, weight = 1)
    home.root_turtle.grid_columnconfigure(1, weight = 1)

    #Placing canvas_turtle inside canvas_game
    home.canvas_turtle.grid(row = 1, column = 1, sticky = NSEW)

    #Giving a background colour to wn
    home.wn.bgcolor("#000000")

    #Adding all the other elements present during the replay (except timers)
    
    #Creating all the frames for the 4 sides
    frame_top = Frame(home.root_turtle, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    frame_bottom = Frame(home.root_turtle, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    frame_right = Frame(home.root_turtle, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)

    #Adding all the frames to the screen
    frame_top.grid(row = 0, column = 1, sticky = NSEW)
    frame_bottom.grid(row = 2, column = 1, sticky = NSEW)

    #Gridding all the frames
    frame_top.grid_columnconfigure((3,4,5), weight = 1)
    frame_bottom.grid_columnconfigure((0,1,2), weight = 1)
    frame_right.grid_rowconfigure(0, weight = 1)
    frame_right.grid_columnconfigure(0, weight = 1)
    
    #Adding the left arrow and right arrow key prompt
    img_left_arrow = PhotoImage(file = "./Icons/left_arrow.png")
    img_right_arrow = PhotoImage(file = "./Icons/right_arrow.png")

    #Creating, gridding and adding frame_arrows to frame_top
    frame_arrows = Frame(frame_top, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    frame_arrows.grid_columnconfigure((0,1), weight = 1)
    frame_arrows.grid_rowconfigure(0, weight = 1)
    frame_arrows.grid(row = 0, column = 3, columnspan = 2, sticky = NSEW, padx = 5)

    label_left_arrow = Label(frame_arrows, image = img_left_arrow, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    label_left_arrow.grid(row = 0, column = 0, sticky = 'nse', padx = 5)

    label_right_arrow = Label(frame_arrows, image = img_right_arrow, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    label_right_arrow.grid(row = 0, column = 1, sticky = 'nsw', padx = 5)

    button_extend_right = Button(frame_top, text = ">", font = ('consolas', 20, 'bold'), bg = constant.LIGHTBGCLR, fg = constant.LIGHTBGTEXTCLR, activebackground = constant.LIGHTBGCLR, activeforeground = constant.LIGHTBGTEXTCLR, command = on_extend_right, bd = 0, highlightthickness = 0)
    button_extend_right.grid(row = 0, column = 6, sticky = NSEW, padx = (0,1))

    #Adding frame_moves to frame_right
    frame_moves = ScrolledFrame(frame_right, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0, max_height = 1000)
    frame_moves.grid(row = 0, column = 0, sticky = NSEW, padx = 2, pady = 2, ipadx = 2, ipady = 2)
    
    #Gridding frame_moves.viewPort
    frame_moves.viewPort.grid_columnconfigure((1,2), weight = 1)

    #Adding frame_pgn for copying and downloading pgn of the game after it gets over
    frame_pgn = Frame(frame_right, bg = constant.LIGHTBGCLR, bd = 0, highlightthickness = 0)
    frame_pgn.grid_columnconfigure(0, weight = 1)
    frame_pgn.grid(row = 1, column = 0, sticky = NSEW)

    #Adding the board scaler to frame_top
    var_board_scaler = IntVar()
    scale_board = ttk.Scale(frame_top, variable = var_board_scaler, from_ = 30, to = 70, orient = HORIZONTAL)
    var_board_scaler.set(50)

    scale_board.bind("<ButtonRelease-1>", on_scale_board_release)
    scale_board.grid(row = 0, column = 5, sticky = EW, padx = 5)
    
    #Adding the pin to frame_top
    img_pin_outline = PhotoImage(file = "./Icons/pin_outline.png").subsample(15,15)
    img_pin_filled = PhotoImage(file = "./Icons/pin_filled.png").subsample(15,15)

    #Adding a back button to frame_Top
    img_back = PhotoImage(file = "./Icons/back.png").subsample(3,3)
    button_back = Button(frame_top, image = img_back, bg = constant.LIGHTBGCLR, fg = constant.LIGHTBGTEXTCLR, activebackground = constant.LIGHTBGCLR, activeforeground = constant.LIGHTBGTEXTCLR, font = ('Consolas', 20, 'bold'), command = on_back, bd = 0, highlightthickness = 0)
    button_back.grid(row = 0, column = 1, sticky = W, padx = 10)

    button_pin = Button(frame_top, image = img_pin_outline, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = on_pin_toggle, bd = 0, highlightthickness = 0)
    pinned = False
    button_pin.grid(row = 0, column = 2, sticky = NSEW)

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
    
    #Adding save configuration and saved configurations buttons
    img_save_configuration = PhotoImage(file = "./Icons/save.png").subsample(4,4)
    img_saved_configurations = PhotoImage(file = "./Icons/folder.png").subsample(4,4)

    button_save_configuration = Button(frame_icons, image = img_save_configuration, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = lambda : save_configuration(replay_match_number, move_count), bd = 0, highlightthickness = 0)

    button_saved_configurations = Button(frame_icons, image = img_saved_configurations, bg = constant.LIGHTBGCLR, activebackground = constant.LIGHTBGCLR, command = lambda : on_show_saved_configurations(replay_match_number), bd = 0, highlightthickness = 0)

    #Adding all the icons to frame_icons
    button_color_chooser.grid(row = 0, column = 0, sticky = NSEW)
    button_volume_toggle.grid(row = 0, column = 1, sticky = NSEW)
    button_flip.grid(row = 0, column = 2, sticky = NSEW)
    button_save_configuration.grid(row = 0, column = 3, sticky = NSEW)
    button_saved_configurations.grid(row = 0, column = 4, sticky = NSEW)

    #Adding the timer labels to frame_top and frame_bottom
    label_white_timer_top = Label(frame_top, text = "00:00:00", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('consolas', 15, 'bold'), bd = 2)
    label_white_timer_bottom = Label(frame_bottom, text = "00:00:00", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('consolas', 15, 'bold'), bd = 2)

    label_black_timer_top = Label(frame_top, text = "00:00:00", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('consolas', 15, 'bold'), bd = 2)
    label_black_timer_bottom = Label(frame_bottom, text = "00:00:00", bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('consolas', 15, 'bold'), bd = 2)

    #Adding tooltips for the required widgets
    Tooltip(button_save_configuration, text = "Save current configuration")
    Tooltip(button_saved_configurations, text = "View saved configurations")
    Tooltip(button_flip, text = "Switch view")
    Tooltip(button_volume_toggle, text = "Toggle sound")
    Tooltip(button_color_chooser, text = "Change square colour")
    Tooltip(button_pin, text = "Toggle pin window")
    Tooltip(scale_board, text = "Scale board size")
    Tooltip(label_left_arrow, text = "Previous move")
    Tooltip(label_right_arrow, text = "Next move")

    for _ in range(2):
        on_extend_right()


#Board setup
def board_setup():
    home.wn.tracer(0)
    for y in range(8):
        for x in range(8):
            globals()[f't{x}{y}'] = turtle.Turtle()
            globals()[f't{x}{y}'].shape('square')
            globals()[f't{x}{y}'].shapesize(stretch_square, stretch_square)
            globals()[f't{x}{y}'].up()
            if (x+y)%2==0:
                globals()[f't{x}{y}'].color(light_square_clr)
            elif (x+y)%2==1:
                globals()[f't{x}{y}'].color(dark_square_clr)
            globals()[f't{x}{y}'].goto((sqsize/2) + sqsize*(x-4)+drift , -(sqsize/2) + sqsize*(4-y) + verticaldrift)
    
    display_labels(boardview)


def update_timers(move_count):
    #moves_wo_pp = moves WithOut PawnPromotion
    moves_wo_pp = moves[:move_count+1]
    for i in moves_wo_pp:
        if i[0] == "Pawnpromotion":
            moves_wo_pp.remove(i)
    no_white_moves = len(moves_wo_pp[0::2])
    no_black_moves = len(moves_wo_pp[1::2])

    if min_time == 0:
        white_time = (sum(times_white[0:no_white_moves], datetime.timedelta(0)).total_seconds())
        black_time = (sum(times_black[0:no_black_moves], datetime.timedelta(0)).total_seconds())
    else:
        white_time = ((datetime.timedelta(seconds=min_time) - sum(times_white[0:no_white_moves], datetime.timedelta(seconds=0.0)) + datetime.timedelta(seconds=increment * (no_white_moves))).total_seconds())    
        black_time = ((datetime.timedelta(seconds=min_time) - sum(times_black[0:no_black_moves], datetime.timedelta(seconds=0.0)) + datetime.timedelta(seconds=increment * (no_black_moves))).total_seconds())
        print(white_time , black_time) 
    #Updating the timers on screen
    if white_time < last_sec:
        label_white_timer_top.configure(text = tfor(white_time))
        label_white_timer_bottom.configure(text = tfor(white_time))
    else:
        label_white_timer_top.configure(text = tfor(white_time)[:-2])
        label_white_timer_bottom.configure(text = tfor(white_time)[:-2])
    if black_time < last_sec:
        label_black_timer_top.configure(text = tfor(black_time))
        label_black_timer_bottom.configure(text = tfor(black_time))
    else:
        label_black_timer_top.configure(text = tfor(black_time)[:-2])
        label_black_timer_bottom.configure(text = tfor(black_time)[:-2])
    

#This function is called everytime the user presses the LEFT arrow key. Its function is to reverse the last move made on the screen and also update replay_list2d.
def previous_move():
    global move_count, replay_list2d, list_piece_numbers, piece_count, moves
    if move_count!=0:
        move_count-=1
    else:
        return None

    home.wn.onkeypress(None,"Right")
    home.wn.onkeypress(None, "Left")        
    
    #PLaying Sounds
    if volume_toggle == True:
        playsound("./Sounds/move.mp3",False)

    if moves[move_count][0] != "Pawnpromotion":
        update_timers(move_count-1)

    if moves[move_count][0] not in ("Castling", "Enpassant", "Pawnpromotion"): 
        #Changes in replay_list2d
        startadd = moves[move_count][1]
        endadd = moves[move_count][0]
        replay_list2d[endadd[0]][endadd[1]]=replay_list2d[startadd[0]][startadd[1]]
        replay_list2d[startadd[0]][startadd[1]]=moves[move_count][2]
        replay_list2d[endadd[0]][endadd[1]][2]=endadd[0]
        replay_list2d[endadd[0]][endadd[1]][3]=endadd[1]

        
        globals()[f'piece{list_piece_numbers[startadd[0]][startadd[1]]}'].goto(coord_from_add(endadd[0], endadd[1]))
        list_piece_numbers[endadd[0]][endadd[1]] = list_piece_numbers[startadd[0]][startadd[1]]
        
        if moves[move_count][2] != emp:
            create_chess_piece(startadd[0],startadd[1], moves[move_count][2][0].title(), logic.colour(moves[move_count][2]))      
            home.wn.tracer(1)      
            list_piece_numbers[startadd[0]][startadd[1]]=piece_count
        elif moves[move_count][2] == emp:
            list_piece_numbers[startadd[0]][startadd[1]]=0
    
    elif moves[move_count][0] == "Castling":
        king_startadd, king_endadd = moves[move_count][1][1], moves[move_count][1][0]            
        rook_startadd, rook_endadd = moves[move_count][2][1], moves[move_count][2][0]            

        for startadd, endadd in ((king_startadd, king_endadd), (rook_startadd, rook_endadd)):
            #Changes in replay_list2d
            replay_list2d[endadd[0]][endadd[1]]=replay_list2d[startadd[0]][startadd[1]]
            replay_list2d[startadd[0]][startadd[1]]=["", "", 0, 0]
            replay_list2d[endadd[0]][endadd[1]][2]=endadd[0]
            replay_list2d[endadd[0]][endadd[1]][3]=endadd[1]

            #Making the piece move on the board
            globals()[f'piece{list_piece_numbers[startadd[0]][startadd[1]]}'].goto(coord_from_add(endadd[0], endadd[1]))

            #Modifying the list_piecenumbers
            list_piece_numbers[endadd[0]][endadd[1]] = list_piece_numbers[startadd[0]][startadd[1]]
            list_piece_numbers[startadd[0]][startadd[1]]=0
    
    elif moves[move_count][0] == "Enpassant":
        #Changes in replay_list2d
        startadd, endadd = moves[move_count][2], moves[move_count][1]
        victimadd = moves[move_count][3]

        replay_list2d[endadd[0]][endadd[1]]=replay_list2d[startadd[0]][startadd[1]]
        replay_list2d[startadd[0]][startadd[1]]=["", "", 0, 0]
        replay_list2d[endadd[0]][endadd[1]][2]=endadd[0]
        replay_list2d[endadd[0]][endadd[1]][3]=endadd[1]
        replay_list2d[victimadd[0]][victimadd[1]] = moves[move_count][4]

        #Modifying the list_piecenumbers of the victim piece
        piece_count+=1
        list_piece_numbers[victimadd[0]][victimadd[1]] = piece_count
    
        #Making the piece move on the board
        globals()[f'piece{list_piece_numbers[startadd[0]][startadd[1]]}'].goto(coord_from_add(endadd[0], endadd[1]))
        create_chess_piece(victimadd[0],victimadd[1], "Pawn", logic.colour(moves[move_count][4]))
        home.wn.tracer(1)

        #Modifying the list_piecenumbers of the stronger attacking piece
        list_piece_numbers[endadd[0]][endadd[1]] = list_piece_numbers[startadd[0]][startadd[1]]
        list_piece_numbers[startadd[0]][startadd[1]] = 0

    elif  moves[move_count][0] == "Pawnpromotion":
        #Changes in replay_list2d
        if logic.colour(moves[move_count][2])=="white":
            color_W_or_B = "*"
        else:
            color_W_or_B=""
        replay_list2d[moves[move_count][1][0]][moves[move_count][1][1]] = ["pawn", f"{color_W_or_B}^", moves[move_count][2][2], moves[move_count][2][3]]

        #Modifying the shape of the piece
        globals()[f'piece{list_piece_numbers[moves[move_count][1][0]][moves[move_count][1][1]]}'].shape("Pawn")

        previous_move()

    home.wn.onkeypress(previous_move, "Left")
    home.wn.onkeypress(next_move, "Right")


#This function is called everytime the user presses the RIGHT arrow key. Its function is to display the move on the screen and also update replay_list2d.
def next_move():
    global move_count, replay_list2d, list_piece_numbers, times, boardview, frame_arrows

    if move_count == 0:
        frame_arrows.destroy()
        if boardview == "black":
            label_white_timer_top.grid(row = 0, column = 3, sticky = EW, padx = 5, ipady = 3)
            label_black_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 3)
        elif boardview == "white":
            label_white_timer_bottom.grid(row = 0, column = 2, sticky = EW, padx = 5, ipady = 3)
            label_black_timer_top.grid(row = 0, column = 3, sticky = EW, padx = 5, ipady = 3) 
    if move_count == len(moves):
        return None
    
    home.wn.onkeypress(None,"Right")
    home.wn.onkeypress(None, "Left")

    if moves[move_count][0] != "Pawnpromotion":
        update_timers(move_count)

    if moves[move_count][0] not in ("Castling", "Enpassant", "Pawnpromotion"): 
        #Changes in replay_list2d
        startadd = moves[move_count][0]
        endadd = moves[move_count][1]
        replay_list2d[endadd[0]][endadd[1]]=replay_list2d[startadd[0]][startadd[1]]
        replay_list2d[startadd[0]][startadd[1]]=["", "", 0, 0]
        replay_list2d[endadd[0]][endadd[1]][2]=endadd[0]
        replay_list2d[endadd[0]][endadd[1]][3]=endadd[1]
        
        #Playing Sounds
        if volume_toggle == True:
            if moves[move_count][2] != emp:
                playsound("./Sounds/capture.mp3",False)
            elif moves[move_count][2] == emp:
                playsound("./Sounds/move.mp3",False)

        #Making the piece move on the board
        globals()[f'piece{list_piece_numbers[startadd[0]][startadd[1]]}'].goto(coord_from_add(endadd[0], endadd[1]))
        if moves[move_count][2] != emp:
            globals()[f'piece{list_piece_numbers[endadd[0]][endadd[1]]}'].ht()
            del globals()[f'piece{list_piece_numbers[endadd[0]][endadd[1]]}']

        #Modifying the list_piecenumbers
        list_piece_numbers[endadd[0]][endadd[1]] = list_piece_numbers[startadd[0]][startadd[1]]
        list_piece_numbers[startadd[0]][startadd[1]]=0
    
    elif moves[move_count][0] == "Castling":
        king_startadd, king_endadd = moves[move_count][1][0], moves[move_count][1][1]            
        rook_startadd, rook_endadd = moves[move_count][2][0], moves[move_count][2][1]            

        for startadd, endadd in ((king_startadd, king_endadd), (rook_startadd, rook_endadd)):
            #Changes in replay_list2d
            replay_list2d[endadd[0]][endadd[1]]=replay_list2d[startadd[0]][startadd[1]]
            replay_list2d[startadd[0]][startadd[1]]=["", "", 0, 0]          
            replay_list2d[endadd[0]][endadd[1]][2]=endadd[0]
            replay_list2d[endadd[0]][endadd[1]][3]=endadd[1]

            #Playing Sounds
            if volume_toggle == True:
                playsound("./Sounds/castling.mp3",False)

            #Making the piece move on the board
            globals()[f'piece{list_piece_numbers[startadd[0]][startadd[1]]}'].goto(coord_from_add(endadd[0], endadd[1]))

            #Modifying the list_piecenumbers
            list_piece_numbers[endadd[0]][endadd[1]] = list_piece_numbers[startadd[0]][startadd[1]]
            list_piece_numbers[startadd[0]][startadd[1]]=0
    
    elif moves[move_count][0] == "Enpassant":
        #Changes in replay_list2d
        startadd, endadd = moves[move_count][1], moves[move_count][2]
        victimadd = moves[move_count][3]

        replay_list2d[endadd[0]][endadd[1]]=replay_list2d[startadd[0]][startadd[1]]
        replay_list2d[startadd[0]][startadd[1]]=["", "", 0, 0]
        replay_list2d[endadd[0]][endadd[1]][2]=endadd[0]
        replay_list2d[endadd[0]][endadd[1]][3]=endadd[1]
        replay_list2d[victimadd[0]][victimadd[1]] = emp

        #Playing Sounds
        if volume_toggle == True:
            playsound("./Sounds/capture.mp3",False)

        #Making the piece move on the board
        globals()[f'piece{list_piece_numbers[startadd[0]][startadd[1]]}'].goto(coord_from_add(endadd[0], endadd[1]))
        globals()[f'piece{list_piece_numbers[victimadd[0]][victimadd[1]]}'].ht()
        del globals()[f'piece{list_piece_numbers[victimadd[0]][victimadd[1]]}']

        #Modifying the list_piecenumbers
        list_piece_numbers[endadd[0]][endadd[1]] = list_piece_numbers[startadd[0]][startadd[1]]
        list_piece_numbers[startadd[0]][startadd[1]] = 0
        list_piece_numbers[victimadd[0]][victimadd[1]] = 0
        
    elif  moves[move_count][0] == "Pawnpromotion":
        #Changes in replay_list2d
        replay_list2d[moves[move_count][1][0]][moves[move_count][1][1]] = moves[move_count][2]

        #Modifying the shape of the piece
        globals()[f'piece{list_piece_numbers[moves[move_count][1][0]][moves[move_count][1][1]]}'].shape(moves[move_count][2][0].title())

    move_count+=1
    try:
        if moves[move_count][0] == "Pawnpromotion":
            next_move()
    except:
        pass

    home.wn.onkeypress(previous_move, "Left")
    home.wn.onkeypress(next_move, "Right")


#Displays A,B,C, ...H and 1,2,3...8 on the side of the board for whiteview and blackview taking into account the value of boardview
def display_labels(view):
    home.wn.tracer(0)
    
    #Deletes the OLD labels
    try:
        show_labels(None, None, None, None, False, True)
    except:
        pass
    try:
        show_labels(None, None, None, None, True, True)
    except:
        pass
    
    home.wn.tracer(1)

    #Creates the NEW labels
    distance=17
    startdistance=(sqsize/2)+8
    if view=="white":
        show_labels((-size/2)-distance,(-size/2)-distance + verticaldrift, sqsize, startdistance, False)    
    elif view=="black":
        show_labels((-size/2)-distance,(-size/2)-distance + verticaldrift, sqsize, startdistance, True)    


#Can be used to create a SINGLE piece at the desired board location (UNLIKE pieces_setup in game.py which creates ALL the pieces in the BASE configuration)
def create_chess_piece(row,col,identity, colour):
    global piece_count, list_piece_numbers
    piece_count+=1
    list_piece_numbers[row][col] = piece_count
    
    home.wn.tracer(0)
    globals()[f'piece{piece_count}']=turtle.Turtle()
    globals()[f'piece{piece_count}'].ht()
    globals()[f'piece{piece_count}'].pu()
    globals()[f'piece{piece_count}'].shape(identity.title())
    stretch_piece = stretch_square * 0.2
    border_width = int(stretch_piece * 4)
    globals()[f'piece{piece_count}'].shapesize(stretch_piece,stretch_piece,border_width)
    globals()[f'piece{piece_count}'].speed(4)
    
    if colour == "black":
        globals()[f'piece{piece_count}'].color(constant.BLACKPIECECLR)
        globals()[f'piece{piece_count}'].pencolor("black")
    elif colour == "white":
        globals()[f'piece{piece_count}'].color(constant.WHITEPIECECLR)
        globals()[f'piece{piece_count}'].pencolor("black")
    
    globals()[f'piece{piece_count}'].goto(coord_from_add(row, col))
    globals()[f'piece{piece_count}'].st()


#Return: Central pixel coordinates as a tuple (IMP: Using the global variable boardview, it also acknowledges the changes in BOARD VIEW and returns the coordinates accordingly)
def coord_from_add(row, col):
    step=size/8
    if boardview=="white":    
        return ((col*step)-(4*step)+(step/2)+drift,(4*step)-(row*step)-(step/2)+verticaldrift)
    elif boardview=="black":
        return ((-1 * ((col*step)-(4*step)+(step/2)))+drift,(-1 * ((4*step)-(row*step)-(step/2)))+verticaldrift)


def configure_list(config_num, update_moves = False):
    global moves, pgn

    temp_list2d = logic.copy_of_init_list2d()
    mcount = 0
    row_count = 0
    chess_not = None
    turn = "white"
    pgn = []

    while mcount<config_num:
        
        temp_list2d_start_of_current_move=[]
        for i in temp_list2d:
            temp=[]
            for j in i:
                temp.append(j.copy())
            temp_list2d_start_of_current_move.append(temp)


        #Modifying temp_list2d to take it to the desired configuration
        if moves[mcount][0] not in ("Castling", "Enpassant", "Pawnpromotion"): 
            srow, scol = moves[mcount][0]
            erow, ecol = moves[mcount][1]
            
            #Getting the chess notation of the move
            cn_srow, cn_scol, cn_erow, cn_ecol = srow, scol, erow, ecol
            cn_castle = False
            
            if mcount != (len(moves)-1) and moves[mcount+1][0] == "Pawnpromotion":
                cn_pppiece = moves[mcount+1][2][0]
            else:
                cn_pppiece = ''

            temp_list2d[erow][ecol]=temp_list2d[srow][scol]
            temp_list2d[srow][scol]=["", "", 0, 0]
            temp_list2d[erow][ecol][2] = erow
            temp_list2d[erow][ecol][3] = ecol
            
        elif moves[mcount][0] == "Castling":

            #Getting the chess notation of the move
            kcol, rcol = moves[mcount][1][0][1], moves[mcount][2][0][1]
            cn_srow, cn_scol, cn_erow, cn_ecol = None, kcol, None, rcol
            cn_castle = True
            cn_pppiece = ''

            king_startadd, king_endadd = moves[mcount][1][0], moves[mcount][1][1]            
            rook_startadd, rook_endadd = moves[mcount][2][0], moves[mcount][2][1]            

            for startadd, endadd in ((king_startadd, king_endadd), (rook_startadd, rook_endadd)):
                temp_list2d[endadd[0]][endadd[1]]=temp_list2d[startadd[0]][startadd[1]]
                temp_list2d[startadd[0]][startadd[1]]=["", "", 0, 0]
                temp_list2d[endadd[0]][endadd[1]][2]=endadd[0]
                temp_list2d[endadd[0]][endadd[1]][3]=endadd[1]

        elif moves[mcount][0] == "Enpassant":
            srow, scol = moves[mcount][1]
            erow, ecol = moves[mcount][2]
            vicrow, viccol = moves[mcount][3]

            #Getting the chess notation of the move
            cn_srow, cn_scol, cn_erow, cn_ecol = srow, scol, erow, ecol
            cn_castle = False
            cn_pppiece = ''

            temp_list2d[erow][ecol]=temp_list2d[srow][scol]
            temp_list2d[srow][scol]=["", "", 0, 0]
            temp_list2d[erow][ecol][2] = erow
            temp_list2d[erow][ecol][3] = ecol
            temp_list2d[vicrow][viccol] = emp

        elif  moves[mcount][0] == "Pawnpromotion":
            temp_list2d[moves[mcount][1][0]][moves[mcount][1][1]] = moves[mcount][2]
            mcount+=1
            continue
    
        mcount += 1

        if not update_moves:
            continue
        

        cn_checkinfo = logic.get_game_situation(temp_list2d)[:2]
        
        chess_not = get_chess_notation(temp_list2d_start_of_current_move, cn_srow, cn_scol, cn_erow, cn_ecol, cn_checkinfo, cn_castle, cn_pppiece)

        #Adding the move to frame_moves
        label_chess_not = Label(frame_moves.viewPort, text = chess_not, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Comic Sans', 15, 'bold'), bd = 2, highlightthickness = 2, highlightbackground = constant.LIGHTBGTEXTCLR)
        Label(frame_moves.viewPort, text = row_count + 1, bg = constant.DARKBGCLR, fg = constant.DARKBGTEXTCLR, font = ('Comic Sans', 15, 'bold'), bd = 2, highlightthickness = 2, highlightbackground = constant.LIGHTBGTEXTCLR).grid(row = row_count, column = 0, sticky = NSEW, padx = 1, pady = 1, ipady = 5)

        if turn == "white":
            #Updating pgn
            pgn.append(str(row_count + 1) + '.')
            pgn.append(chess_not)

            label_chess_not.grid(row = row_count, column = 1, sticky = NSEW, padx = 1, pady = 1, ipady = 5)
            turn = "black"
        elif turn == "black":
            #Updating pgn
            pgn.append(chess_not)

            label_chess_not.grid(row = row_count, column = 2, sticky = NSEW, padx = 1, pady = 1, ipady = 5)
            turn = "white"
            row_count += 1
    
    if update_moves:
        generate_pgn()

    return temp_list2d


#Deletes all the existing turtle chess pieces on the board, creates new turtle chess pieces for the desired configuration. Updates/Resets replay_list2d, list_of_piece_numbers, piece_count and move_count as well.
def configure_pieces(config_num):
    global replay_list2d, list_piece_numbers, piece_count, move_count, frame_moves, moves

    #Reconfiguring the board
    home.wn.tracer(0)
    for i in range(1,piece_count+1):
        try:
            globals()[f'piece{i}'].ht()
            globals()[f'piece{i}'].clear()
            del globals()[f'piece{i}']
        except:
            pass

    #Initialisation of some variables

    try:
        del replay_list2d, list_piece_numbers, piece_count, move_count
    except:
        pass
        
    list_piece_numbers = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]
    
    piece_count = 0
    
    replay_list2d = configure_list(config_num, False).copy()
    move_count = config_num

    update_timers(config_num - 1)

    for i in range(8):
        for j in range(8):
            if replay_list2d[i][j] != emp:
                create_chess_piece(i, j, replay_list2d[i][j][0], logic.colour(replay_list2d[i][j]))   

    home.wn.tracer(1)
    
    home.wn.listen()
    home.wn.onkeypress(previous_move, "Left")
    home.wn.onkeypress(next_move, "Right")


def configure_game():
    home.wn.tracer(0)
    
    #Hiding and Deleting all the board turtles on the screen
    for x in range(8):
        for y in range(8):
            try:
                globals()[f't{x}{y}'].ht()
                globals()[f't{x}{y}'].clear()
                del globals()[f't{x}{y}']
            except:
                pass
    
    for x in range(8):
        for y in range(8):
            try:
                globals()[f'tb{x}{y}'].ht()
                globals()[f'tb{x}{y}'].clear()
                del globals()[f'tb{x}{y}']
            except:
                pass
    
    board_setup()
    configure_pieces(move_count)
    home.wn.tracer(1)

    
def switch_view():
    global boardview
    if boardview == "black":
        boardview="white"
        display_labels("white")
    
    elif boardview == "white":
        boardview="black"
        display_labels("black")

    configure_pieces(move_count)


def generate_pgn():
    global pgn, img_copy, button_pgn_copy, frame_pgn

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
    if winner == "W":
        pgn_result = "1-0"
    elif winner == "B":
        pgn_result = "0-1"
    elif winner in ('D', 'S'):
        pgn_result = "1/2-1/2"
     
    pgn_str = f'''
[Site "Pocket Chess Arena"]
[White "{white_name}"]
[Black "{black_name}"]
[Result "{pgn_result}"]
[Date "{date.strftime("%Y.%m.%d")}"]

''' + pgn_str + " " + pgn_result

    img_copy = PhotoImage(file = "./Icons/clipboard.png").subsample(3,3)
    button_pgn_copy = Button(frame_pgn, image = img_copy, text = "Copy PGN to clipboard", compound = LEFT, font = ('Comic Sans', 13), bg = constant.LIGHTBGCLR, fg = constant.LIGHTBGTEXTCLR, activebackground = constant.LIGHTBGCLR, command = on_pgn_copy, bd = 0, highlightthickness = 0)
    button_pgn_copy.grid(row = 0, column = 0, sticky = NSEW)


def replay_main(mat_no):
    global white_name, black_name, winner, date
    
    def on_turtle_close():
        home.program_running = False
        home.root_turtle.destroy()
        try:
            root_save_configuration.destroy()
        except:
            pass
        
        try:
            root_saved_configurations.destroy()
        except:
            pass
        database_functions.close_connection()

    home.root_turtle.protocol("WM_DELETE_WINDOW", on_turtle_close)

    #Receiving all the details of the desired match from the database  
    date, start_time, end_time, duration, white_player, black_player, winner, moves, times, min_time, increment = database_functions.receive_game_details(mat_no)

    home.wn.clearscreen()
    home.wn.bgcolor("black")
    white_name = white_player.title()
    black_name = black_player.title()
    if winner.lower() == 'w':
        home.root_turtle.title(f'*{white_name} vs {black_name}')
    elif winner.lower() == 'b':
        home.root_turtle.title(f'{white_name} vs *{black_name}')
    elif winner.lower() == 'd':
        home.root_turtle.title(f'*{white_name} vs *{black_name}')
    elif winner.lower() == 's':
        home.root_turtle.title(f'#{white_name} vs #{black_name}')
        
    print(moves)
    print(times)

    logic.define_basic_global_variables()
    define_basic_global_variables(mat_no, moves, times, min_time, increment)
    board_setup()
    configure_pieces(0)

    #Adding chess notations of all moves to frame_moves
    configure_list(len(moves), True)

    home.wn.tracer(1)


    