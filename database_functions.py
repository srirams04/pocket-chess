import datetime
import sqlite3
from tkinter import messagebox


def init_database(db_val = "pocketchess.db"):
    global conn, cur
    # conn = sqlite3.connect(db_val)
    # cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Games_Played (
        Match_Number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        Date DATE NOT NULL,
        Start_time TIME NOT NULL,
        End_time TIME NOT NULL,
        Duration INTEGER NOT NULL,
        White_player_name VARCHAR(40) NOT NULL,
        Black_player_name VARCHAR(40) NOT NULL,
        Winner VARCHAR(1) NOT NULL CHECK (Winner IN ('W', 'B', 'S', 'D')),
        Min_time INTEGER,
        Increment INTEGER
        )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Moves_Made (
        Match_Number INTEGER NOT NULL,
        Move VARCHAR(125) NOT NULL,
        Time_Taken TIME(2),
        FOREIGN KEY (Match_Number) REFERENCES Games_Played(Match_Number)
        )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Configurations_Saved (
        Match_Number INTEGER NOT NULL,
        Config_no INTEGER NOT NULL,
        Title VARCHAR(150) NOT NULL,
        Notes VARCHAR(1500) NOT NULL,
        FOREIGN KEY (Match_Number) REFERENCES Games_Played(Match_Number)
        )""")

    conn.commit()


def open_connection(db_val = "pocketchess.db"):
    global conn, cur
    conn = sqlite3.connect(db_val)
    cur = conn.cursor()
    init_database(db_val)


def update_game_details(date, start_time, end_time, duration, white_player, black_player, winner, List_of_Moves, List_of_Times, min_time, increment):
    global conn, cur
    
    # Convert duration to seconds
    duration_seconds = duration.total_seconds()
    
    # Updating the TABLE Games_Played
    cur.execute("INSERT INTO Games_Played (Date, Start_time, End_time, Duration, White_player_name, Black_player_name, Winner, Min_time, Increment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (date, start_time, end_time, int(duration_seconds), white_player, black_player, winner, min_time, increment))

    # Getting the Match number
    mat_no = cur.lastrowid

    # Updating the TABLE Moves_Made
    for move, time_taken in zip(List_of_Moves, List_of_Times):
        # print(move)
        move_str = str(move)
        # print(move_str)
        cur.execute("INSERT INTO Moves_Made (Match_Number, Move, Time_Taken) VALUES (?, ?, ?)", (mat_no, move_str, time_taken))
        

    conn.commit()
    # except Exception as e:
    #     print(f"Error: {e}")


def receive_game_details(mat_no):
    global conn, cur
    # try:
    # Receiving all the details from the database for the match number given as parameter
    cur.execute("SELECT * FROM Games_Played WHERE Match_Number = ?", (mat_no,))
    row = cur.fetchone()
    if row:
        mat_no, date_str, start_time, end_time, duration_seconds, white_player, black_player, winner, min_time, increment = row

        duration = datetime.timedelta(seconds=duration_seconds)
        cur.execute("SELECT Move FROM Moves_Made WHERE Match_Number = ?", (mat_no,))
        move_strings = [move[0] for move in cur.fetchall()]
        moves = [eval(move_str) for move_str in move_strings]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        cur.execute("SELECT Time_Taken FROM Moves_Made WHERE Match_Number = ?", (mat_no,))
        times = [datetime.timedelta(seconds = datetime.datetime.strptime(time[0], "%H:%M:%S.%f").second) for time in cur.fetchall()]
        print(moves)
        print(times)

        return date, start_time, end_time, duration, white_player, black_player, winner, moves, times, min_time, increment
    # except Exception as e:
    #     print(f"Error: {e}")


# def receive_all_game_details():
#     global conn, cur
#     try:
#         cur.execute("SELECT * FROM Games_Played")
#         return cur.fetchall()
#     except Exception as e:
#         print(f"Error: {e}")

def receive_all_game_details():
    global conn, cur
    try:
        cur.execute("SELECT * FROM Games_Played")
        game_details = cur.fetchall()
        modified_details = []
        for detail in game_details:
            match_no, date_str, start_time, end_time, duration_seconds, white_player, black_player, winner, min_time, increment = detail
            duration = datetime.timedelta(seconds=duration_seconds)

            cur.execute("SELECT Move FROM Moves_Made WHERE Match_Number = ?", (match_no,))
            move_strings = [move[0] for move in cur.fetchall()]
            moves = [tuple(move_str.split()) for move_str in move_strings]
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

            modified_detail = (match_no, date, start_time, end_time, duration, white_player, black_player, winner, min_time, increment, moves)
            modified_details.append(modified_detail)

        return modified_details
    except Exception as e:
        print(f"Error: {e}")


def update_configuration_saved(mat_no, config_no, title, notes):
    global conn, cur
    try:
        cur.execute("DELETE FROM Configurations_Saved WHERE Match_Number = ? AND Config_no = ?", (mat_no, config_no))
        cur.execute("INSERT INTO Configurations_Saved (Match_Number, Config_no, Title, Notes) VALUES (?, ?, ?, ?)",
                    (mat_no, config_no, title.rstrip(), notes.rstrip()))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")


def delete_configuration(mat_no, config_no):
    global conn, cur
    try:
        cur.execute("DELETE FROM Configurations_Saved WHERE Match_Number = ? AND Config_no = ?", (mat_no, config_no))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")


def receive_configurations_saved(mat_no):
    global conn, cur
    try:
        _ = cur
    except NameError as e:
        return None
    
    try:
        cur.execute("SELECT * FROM Configurations_Saved WHERE Match_Number = ?", (mat_no,))
        return cur.fetchall()
    except Exception as e:
        messagebox.showerror("Database Error", e)
        return None


def close_connection():
    global conn, cur
    try:
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


def check_connection():
    global conn, cur
    
    _ = receive_configurations_saved(0) #This has been given only to check if there is a connection. Match Numbers start from 1.
    
    if _ == None:
        return False
    else:
        return True 