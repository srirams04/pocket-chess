#Import of Modules
import turtle
from logmessage import log
from math import floor
from tkinter import *
from random import randint
from playsound import playsound
from colorsys import rgb_to_hls, hls_to_rgb
from hashlib import sha512

#Import of created files
import home
import game
import logic
import constant
import csv

class Tooltip:
    def __init__(self, widget, *, bg='#18191C', fg = "#FFFFFF", pad=(8, 6, 6, 5), text='widget info', waittime=400, wraplength=250):
        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)
        self.bg = bg
        self.fg = fg
        self.pad = pad
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self):
        def tip_pos_calculator(widget, label, *, tip_delta=(10, 5), pad=(5, 3, 5, 3)):
            w = widget

            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

            width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                             pad[1] + label.winfo_reqheight() + pad[3])

            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automagically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        fg = self.fg
        bg = self.bg
        pad = self.pad
        widget = self.widget

        # creates a toplevel window
        self.tw = Toplevel(widget)
        self.root = self.tw.winfo_toplevel()
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = Frame(self.tw,
                       background=bg,
                       borderwidth=0)
        label = Label(win,
                          text=self.text,
                          justify=LEFT,
                          font = ('Comic Sans', 13, 'bold'),
                          background=bg,
                          foreground=fg,
                          relief=SOLID,
                          borderwidth=0,
                          wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]),
                   pady=(pad[1], pad[3]),
                   sticky=NSEW)
        win.grid()

        x, y = tip_pos_calculator(widget, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        tw = self.tw
        if tw:
            tw.destroy()
        self.tw = None


class CustomButton(Button):
    def __init__(self, master, hover = False, hover_text = '', hover_bg = "#000000", hover_fg = "#FFFFFF", *args, **kwargs):
        super().__init__(master, *args, **kwargs, activebackground = constant.ACTIVEBGCLR, activeforeground = constant.ACTIVEFGCLR)

        if hover:
            self.bind("<Enter>", lambda e: self.onHoverShowButton())
            self.hover_text = hover_text
            self.hover_bg = hover_bg
            self.hover_fg = hover_fg
        else:
            self.bind("<Enter>", lambda e: self.onEnter())
    
    def onEnter(self):
        org_bg = self['bg']
        conv_org_bg = tuple(int(org_bg.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        
        new_bg = '#%02x%02x%02x' % darken_color(*conv_org_bg, 0.2)
        
        self.config(bg = new_bg)
        
        def onLeave(e):
            if new_bg == self['bg']:
                self.config(bg = org_bg)
            self.unbind("<Leave>")
            
        self.bind("<Leave>", onLeave)
    
    def onHoverShowButton(self):
        org_bg = self['bg']
        new_bg = self.hover_bg
        
        org_fg = self['fg']
        new_fg = self.hover_fg
        
        org_text = self['text']
        
        def onLeave(e):
            self.config(text = org_text, bg = org_bg, fg = org_fg)
            self.unbind("<Leave>")
            
        self.config(text = self.hover_text, bg = new_bg, fg = new_fg)
        self.bind("<Leave>", onLeave)
 
   
class ScrolledFrame(Frame):
    def __init__(self, parent, max_height, *args, **kwargs):
        super().__init__(parent, *args, **kwargs) # create a frame (self)

        #Storing the value of max_height
        self.max_height = max_height
        
        #place canvas on self
        self.canvas = Canvas(self, *args, **kwargs)
        
        #place a frame on the canvas, this frame will hold the child widgets
        self.viewPort = Frame(self.canvas, *args, **kwargs)
        
        #place a vertical scrollbar on self
        self.vsb = Scrollbar(self, orient= VERTICAL)
        
        #Setting the command for vertical scrollbar
        self.vsb.config(command = self.canvas.yview)
        
        #pack the vertical scrollbar to right of self
        self.vsb.pack(side = RIGHT, fill = Y)
        
        #attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand = self.vsb.set)
        
        #pack canvas to left of self and expand to fil
        self.canvas.pack(side = TOP, fill = 'both', expand = True)
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw")
        
        #bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        
        #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        
        #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.onFrameConfigure(None)

        self.viewPort.bind('<Enter>', self._bound_to_mousewheel)
        self.viewPort.bind('<Leave>', self._unbound_to_mousewheel)


    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)


    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")


    def _on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass


    def onFrameConfigure(self, event):
        viewPort_ht = self.viewPort.winfo_height()
        
        if viewPort_ht < self.max_height:
            self.canvas.config(height = viewPort_ht)
        else:
            self.canvas.config(height = self.max_height)
        
        #whenever the size of the frame changes, alter the scroll region respectively.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
  
    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width

        #whenever the size of the canvas changes alter the window region respectively.
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)
    
    
    def config(self, **kwargs):
        self.viewPort.config(**kwargs)
        self.canvas.config(**kwargs)
        self.viewPort.update_idletasks()
        self.canvas.update_idletasks()
    
    
    def configure(self, **kwargs):
        self.viewPort.config(**kwargs)
        self.canvas.config(**kwargs)
        self.viewPort.update_idletasks()
        self.canvas.update_idletasks()


   
class CustomEntry(Entry):
    
    def __init__(self, master, readonly, onEntryUpdate, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.config(state = 'readonly')
        self.onEntryUpdate = onEntryUpdate
        if not readonly:
            self.bind("<Double-Button-1>", lambda e: self.onDoubleClick())

    def onDoubleClick(self):
        org_text = self.get()
        org_bg = self['bg']
        org_fg = self['fg']
        self.config(state = NORMAL, bg = "white", fg = "black")
        self.focus_set()
        
        def onReturn(e):
            self.config(state = 'readonly')
            #self.onEntryUpdate(self.get(), org_text)
            self.config(bg = org_bg, fg = org_fg)

            self.unbind("<Return>")
            self.bind("<Double-Button-1>", lambda e: self.onDoubleClick())
        
        
        def onFocusOut(e):
            self.delete(0, END)
            self.insert(INSERT, org_text)
            self.config(state = 'readonly')
            self.config(bg = org_bg, fg = org_fg)
            self.unbind("<FocusOut>", funcid_focus_out)
            self.bind("<Double-Button-1>", lambda e: self.onDoubleClick())
            
        self.unbind("<Double-Button-1>")
        self.bind("<Return>", onReturn)
        funcid_focus_out = self.bind("<FocusOut>", onFocusOut, add = True)
  

class DataManager(Tk):
    def __init__(self, title, subtitles, file_name):
        super().__init__()
        self._title = title
        self._subtitles = subtitles #Tuple
        self._entries = [] #Nested list of all the entries
        self._rowcount = 1
        self._file_name = file_name #Complete path
    
    def create_manager(self):
        self.title(self._title)

        #Gridding self
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        #Creating frame_data and frame_buttons
        self.frame_data = ScrolledFrame(self, max_height = 200, bg = constant.LIGHTBGCLR)
        self.frame_buttons = Frame(self, bg = constant.DARKBGCLR, highlightthickness = 0)

        #Displaying frame_data and frame_buttons
        self.frame_data.grid(row = 1, column = 0, sticky = NSEW, padx = 10, pady = 10)
        self.frame_buttons.grid(row = 2, column = 0, sticky = NSEW, padx = 10, pady = 10)
        
        #Gridding frame_data and frame_buttons
        self.frame_data.grid_columnconfigure(tuple(range(len(self._subtitles)) + 1), weight = 1)
        self.frame_buttons.grid_columnconfigure(1, weight = 1)

        #Adding buttons to frame_buttons
        button_add = Button(self.frame_buttons, text = "ADD", font = ('Comic Sans', 15, 'bold'), bg = constant.PRIMARYCLR, fg = constant.DARKBGTEXTCLR, activebackground = constant.ACTIVEBGCLR, activeforeground = constant.ACTIVEFGCLR, command = None)
        button_cancel = Button(self.frame_buttons, text = "CANCEL", font = ('Comic Sans', 15, 'bold'), bg = constant.TERTIARYCLR, fg = constant.DARKBGTEXTCLR, activebackground = constant.ACTIVEBGCLR, activeforeground = constant.ACTIVEFGCLR, command = None)
        button_save = Button(self.frame_buttons, text = "SAVE", font = ('Comic Sans', 15, 'bold'), bg = constant.SECONDARYCLR, fg = constant.DARKBGTEXTCLR, activebackground = constant.ACTIVEBGCLR, activeforeground = constant.ACTIVEFGCLR, command = None)
        
        button_add.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10, ipadx = 5, ipady = 5)
        button_cancel.grid(row = 0, column = 1, sticky = E, padx = 10, pady = 10, ipadx = 5, ipady = 5)
        button_save.grid(row = 0, column = 2, sticky = W, padx = 10, pady = 10, ipadx = 5, ipady = 5)

    def add(self):
        temp_list = []
        for colcount in range(len(self._subtitles)):
            entry_temp = CustomEntry(self.frame_data, False, None, font = ('Comic Sans', 13))
            entry_temp.grid(row = self._rowcount, column = colcount, padx = 2, pady = 2, ipadx = 2, ipady = 2, sticky = NSEW)
            temp_list.append(entry_temp)
        
        self._entries.append(temp_list)
    
    def display(self):
        creader = csv.reader(self._file_name)
        

#General Purpose Function: Used by both game.py and replay.py
def show_labels(x,y,division, divisionstart, reverse, delete=False): #origin coordinates and space in between each character 
    home.wn.tracer(0)
    if reverse==False:
        letters = [chr(_) for _ in range(65,65+8)]
        numbers = [_ for _ in range(1,9)]
    elif reverse==True:
        letters = [chr(_) for _ in range(65+7,64,-1)]
        numbers = [_ for _ in range(8,0,-1)]
    
    if reverse==False:
        lt = "w"
    else:
        lt = "b"

    if delete == True:
        for letter in letters:
            globals()[f'{lt}{letter}'].clear()
            del globals()[f'{lt}{letter}']
    
        for number in numbers:
            globals()[f'{lt}l{number}'].clear()
            del globals()[f'{lt}l{number}']
        return None
            
    letter_coor=[None]
    number_coor=[None]
    letter_coor = [((x + divisionstart) + a*division, y) for a in range(0,8)] 
    number_coor = [(x, (y + divisionstart) + a*division) for a in range(0,8)]


    for letter,coor in zip(letters,letter_coor):
        globals()[f'{lt}{letter}'] = turtle.Turtle()
        globals()[f'{lt}{letter}'].ht()
        globals()[f'{lt}{letter}'].up()
        globals()[f'{lt}{letter}'].pencolor(constant.DARKBGTEXTCLR)
        globals()[f'{lt}{letter}'].goto(coor[0]+5,coor[1])
        globals()[f'{lt}{letter}'].write(letter,font=("Comic Sans", 10, "bold"))

    for number,coor in zip(numbers,number_coor):
        globals()[f'{lt}l{number}'] = turtle.Turtle()
        globals()[f'{lt}l{number}'].ht()
        globals()[f'{lt}l{number}'].up()
        globals()[f'{lt}l{number}'].pencolor(constant.DARKBGTEXTCLR)
        globals()[f'{lt}l{number}'].goto(coor[0],coor[1])
        globals()[f'{lt}l{number}'].write(str(number),font=("Comic Sans", 10, "bold"))

    home.wn.update()


#time format, n in seconds
def tfor(n):
    s = n%60
    m = int((n//60)%60)
    h = int((n//60)//60)
    
    sec = "0"*(2-len(str(int(round(s,1))))) + str(float(round(s,1))) 

    time = f'{"0"*(2-len(str(h)))+str(h)} : {"0"*(2-len(str(m)))+str(m)} : {sec}'
    return time
  
#Parameters: Exact Pixels on the screen
#Return: Assuming the board to just be a MATRIX, it returns the row num and the col num (Doesn't care about WV and BV.)
def get(x,y):
    return floor(3 - y//game.sqsize), floor(x//game.sqsize + 4)


#Return: central pixel coordinates as a tuple
def antiget(row,col): #index2d ==> 2dindex tuple, l-side length of the board in pixels
    step=game.size/8    
    return ((col*step)-(4*step)+(step/2),(4*step)-(row*step)-(step/2))


#Parameters: WV-Row num,  WV-Col num
#Return: Chess Naming for the square (Eg: A6, E4 etc)
def info(row, col): 
    return chr(col + 65) + str(8-row)
    

#Converting x coordinate to centre of the board
#While Processing, it is easier deal with the board as if it was actaully in the centre. Now, x and y work like as though the board is at the centre
def shift_to_centre(x):
    if game.white==True:
        x = x - game.drift
    elif game.black==True:
        x = x + game.drift
    else:
        x=0
    return x
    

def whiteview_blackview_equivalents(row,col):
    if game.white==True:
        whrow=row
        whcol=col
        blrow, blcol=7-row, 7-col
        
    elif game.black==True:
        blrow, blcol = row, col  
        whrow=7-row 
        whcol=7-col
    else:
        whrow, whcol, blrow, blcol=0,0,0,0
        
    return whrow, whcol, blrow, blcol


def find(pinfo, f2d_start_of_current_move):
    l = f2d_start_of_current_move
    altpieces = []
    for y in range(8):
        for x in range(8):
            if l[y][x] == pinfo:
                continue
            elif l[y][x][1] == pinfo[1]:
                altpieces += [l[y][x]]
    return altpieces


def get_chess_notation(f2d_start_of_current_move, srow,scol,erow,ecol,checkinfo,castle,pppiece=''):
    
    check = '+' if checkinfo[0] and not checkinfo[1] else ''
    checkmate = '#' if checkinfo[1] else ''
    check_str = check + checkmate

    if castle:
        return ('O-O' if ecol > scol else 'O-O-O') + check_str

    pinfo = f2d_start_of_current_move[srow][scol]
    piece = pinfo[0][0].upper() if pinfo[0] != 'pawn' else 'abcdefgh'[scol]
    piece = 'N' if piece == 'H' else piece
    process = '' if not f2d_start_of_current_move[erow][ecol][0] else 'x'
    suffix = f'{"abcdefgh"[ecol]}{8-erow}'

    if piece in ('Q','N','B','R'):
        altpieces = find(pinfo, f2d_start_of_current_move)

        if altpieces:
            filtered_altpieces = []
            for r in range(len(altpieces)):
                otherp = altpieces[r]
                sr,sc = otherp[2],otherp[3]
                possible = logic.legal((sr,sc),f2d_start_of_current_move)[1]
                if (erow,ecol) in possible:
                    filtered_altpieces += [altpieces[r]]
            altpieces = filtered_altpieces

            row = col = False
            prefix = ''
            for opiece in altpieces:
                prefix = f'{piece}{"abcdefgh"[scol]}'
                col = True if opiece[3] == scol else col
                row = True if opiece[2] == srow else row
                if row or col:
                    prefix = ''
                if row and col:
                    break
            if not prefix:
                prefix = f'{piece}{"abcdefgh"[scol]}' if row else piece
                prefix = f'{piece}{8-srow}' if col else prefix
                prefix = f'{piece}{"abcdefgh"[scol]}{8-srow}' if row and col else prefix
            
        else:
            prefix = piece
    else:
        if piece.lower() == piece: #Pawn
            prefix = piece if scol != ecol  else ''
        else: #King
            prefix = piece
    
    if pinfo[0] == "pawn" and scol != ecol:
        if pppiece:
            if pppiece.lower() == "horse":
                return f'{prefix}x{suffix}=N' + check_str
            else:
                return f'{prefix}x{suffix}={pppiece[0].upper()}' + check_str
        else:
            return f'{prefix}x{suffix}' + check_str

    if pppiece:
        if pppiece.lower() == "horse":
            return f'{prefix}{process}{suffix}=N' + check_str
        else:
            return f'{prefix}{process}{suffix}={pppiece[0].upper()}' + check_str
    return f'{prefix}{process}{suffix}' + check_str


#Aim: Play sound effects for movement, captures and check
#Parameters: Ending row, Ending column, enpassant capture?, castling?, check?, checkmate?, stalemate?
def sounds(erow, ecol, enpassant, castle,  check, checkmate, stalemate):
    if check!= True and checkmate!=True and stalemate!=True:
        if castle==True:
            playsound("./Sounds/castling.mp3", False)
        elif enpassant==True:
            playsound("./Sounds/capture.mp3", False)
        else:
            if logic.list2d_start_of_current_move[erow][ecol] == logic.emp:
                playsound("./Sounds/move.mp3", False)
            elif logic.list2d_start_of_current_move[erow][ecol] != logic.emp:
                playsound("./Sounds/capture.mp3", False)
    elif check == True and checkmate != True:
        playsound("./Sounds/check.mp3", False)
                

def adjust_color_lightness(r, g, b, factor):
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)
    
    
def lighten_color(r, g, b, factor=0.1):
    r = int(r)
    g = int(g)
    b = int(b)
    return adjust_color_lightness(r, g, b, 1 + factor)


def darken_color(r, g, b, factor=0.1):
    return adjust_color_lightness(r, g, b, 1 - factor) 
 
   
def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length // 3], 16) for i in range(0, length, length // 3))


def rgb_to_hex(rgb):
    rgb = tuple(int(i) for i in rgb)
    return '#%02x%02x%02x' % rgb



   