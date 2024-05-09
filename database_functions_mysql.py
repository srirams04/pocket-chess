import mysql.connector
import configparser
from tkinter import messagebox

#mysql -h mydbinstance.cm4fylzmmaab.us-east-2.rds.amazonaws.com  -u admin -p

#mysqldump.exe --defaults-file="C:\Users\srira\AppData\Local\Temp\tmpyiffty3b.cnf"  --host=mydbinstance.cm4fylzmmaab.us-east-2.rds.amazonaws.com --port=3306 --default-character-set=utf8 --user=admin --protocol=tcp --skip-triggers "chessdb"


def init_database(db_val):
    global mycur, chessdb
    mycur.execute(f"CREATE DATABASE IF NOT EXISTS {db_val}")
    mycur.execute(f"USE {db_val}")
    
    mycur.execute("""CREATE TABLE IF NOT EXISTS Games_Played (
        Match_Number INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
        Date DATE NOT NULL,
        Start_time TIME NOT NULL,
        End_time TIME NOT NULL,
        Duration TIME NOT NULL,
        White_player_name VARCHAR(40) NOT NULL,
        Black_player_name VARCHAR(40) NOT NULL,
        Winner ENUM('W', 'B', 'S', 'D') NOT NULL,
        Min_time INT,
        Increment INT
        );
        """)

    mycur.execute("""CREATE TABLE IF NOT EXISTS Moves_Made (
        Match_Number INT UNSIGNED NOT NULL,
        Move VARCHAR(125) NOT NULL,
        Time_Taken TIME(2),
        FOREIGN KEY (Match_Number) REFERENCES Games_Played(Match_Number)
        );
        """)

    mycur.execute("""CREATE TABLE IF NOT EXISTS Configurations_Saved (
        Match_Number INT UNSIGNED NOT NULL,
        Config_no INT UNSIGNED NOT NULL,
        Title VARCHAR(150) NOT NULL,
        Notes VARCHAR(1500) NOT NULL,
        FOREIGN KEY (Match_Number) REFERENCES Games_Played(Match_Number)
        );
        """)

    chessdb.commit()


def open_connection():
    global chessdb, mycur
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        host_val = config['DATABASE DETAILS']['HOST']
        if host_val == "public":
            host_val = "mydbinstance.cm4fylzmmaab.us-east-2.rds.amazonaws.com"
            user_val = "admin"
            passwd_val = "npschess"
            db_val = "chessdb"
        else:
            user_val = config['DATABASE DETAILS']['USER']
            passwd_val = config['DATABASE DETAILS']['PASSWORD']
            db_val = config['DATABASE DETAILS']['DATABASE']

        #chessdb=mysql.connector.connect(host="localhost", user="root", passwd="sri21sql04#$", database="chessarena")
        chessdb=mysql.connector.connect(host=host_val, user=user_val, passwd=passwd_val, auth_plugin='mysql_native_password')
        mycur=chessdb.cursor()
        init_database(db_val)

    except:
        pass


def update_game_details(date,start_time, end_time, duration, white_player, black_player, winner, List_of_Moves, List_of_Times, min_time, increment):
    try:
        #Updating the TABLE Games_Played
        mycur.execute("INSERT INTO Games_Played VALUES(NULL,'" + str(date) + "','" + str(start_time) + "','" + str(end_time) + "','" + str(duration) + "','" + white_player + "','" + black_player + "','" + winner + "','" + str(min_time) + "','" + str(increment) + "')")
        
        #Getting the Match number
        mycur.execute("SELECT Match_Number from Games_Played")
        mat_no=mycur.fetchall()[-1][0]

        #Updating the TABLE Moves_Made
        for i,j in zip(List_of_Moves, List_of_Times):
            mycur.execute("INSERT INTO Moves_Made VALUES('" + str(mat_no) + "',\"" + str(i) + "\",\""+ str(j) + "\")") 
        
        chessdb.commit()
    except:
        pass
        

def receive_game_details(mat_no):
    try:
        #Receiving all the details from the database for the match number given as parameter
        mycur.execute("SELECT * from Games_Played where match_number="+str(mat_no))
        mat_no,date,start_time, end_time, duration, white_player, black_player, winner, min_time, increment = mycur.fetchall()[0]

        mycur.execute("SELECT Move from Moves_Made where match_number="+str(mat_no))
        moves=[]
        for i in mycur.fetchall():
            moves.append(eval(i[0]))

        mycur.execute("SELECT Time_Taken from Moves_Made where match_number="+str(mat_no))
        times=[]
        for i in mycur.fetchall():
            times.append(i[0])

        return date,start_time, end_time, duration, white_player, black_player, winner, moves, times, min_time, increment
    except:
        pass


def receive_all_game_details():
    try: 
        mycur.execute("SELECT * from Games_Played")
        return mycur.fetchall()[0:]
    except:
        pass


def update_configuration_saved(mat_no, config_no, title, notes):
    try:
        mycur.execute("DELETE FROM Configurations_Saved WHERE Match_Number = "+str(mat_no)+" and Config_No ="+str(config_no))
        mycur.execute("INSERT INTO Configurations_Saved VALUES("+str(mat_no)+","+str(config_no)+",\""+title.rstrip()+"\",\""+notes.rstrip()+"\")")
        chessdb.commit()
    except:
        pass


def delete_configuration(mat_no, config_no):
    try:
        mycur.execute("DELETE FROM Configurations_Saved WHERE Match_Number = "+str(mat_no)+" and Config_No ="+str(config_no))
        chessdb.commit()
    except:
        pass


def receive_configurations_saved(mat_no):
    global mycur
    try:
        mycur.execute("SELECT * from Configurations_Saved WHERE Match_Number = "+ str(mat_no))
        return mycur.fetchall()
    except mysql.connector.Error as err:
        if err.errno in (2006, 2013):
            pass
        else:
            messagebox.showerror("Database Error", err)
            return "Unknown Error"
    except Exception as e:
        pass
        
        
def close_connection():
    try:
        mycur.close()
        chessdb.close()
    except:
        pass


def check_connection():
    _ = receive_configurations_saved(0) #This has been given only to check if there is a connection. Match Numbers start from 1.
    
    if _ == None:
        return False
    else:
        return True 

