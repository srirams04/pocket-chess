import flask
from threading import Thread
from random import *
import time

server = flask.Flask(__name__)

rooms = {} #code: [code,me,move]
timers = {} #code: {(whitetime,running), (blacktime,running) ,mintime ,inc, movenumber}
inccheck = {} #code : [whiteinc bool , blackinc bool]
move_durations = {} #code : move duration
offers = {} # code : drawoffers or gameover
connection = {}# code : [[white connection , black connection]]

debug = ''

def clean(code):
    try :
        del rooms[code] , timers[code] , inccheck[code] , move_durations[code] , connection[code] , offers[code]
    except:
        pass

def generate_code():
    number = list(str(randint(100,999)))
    characters = [choice([chr(x + 64) for x in range(1,27)]) for t in range(2)]
    
    l = number + characters
    shuffle(l)
    code = ''.join(l)
    if code in rooms:
        return generate_code()
    return code


def handle_room(code,timer=True):
    global oldb, oldw, connection
    t0 = int(time.time())
    while code in rooms:

        if timer:
            if timers[code]['black'][0] <= 0:
                timers[code]['black'][0] = 0
                offers[code] = {'status':'gameover', 'resignations':None, 'draw offers':None, 'flagged':'black', 'lost connection':None, 'game result':'W'}
                break

            elif timers[code]['white'][0] <= 0:
                timers[code]['white'][0] = 0
                offers[code] = {'status':'gameover', 'resignations':None, 'draw offers':None, 'flagged':'white', 'lost connection':None, 'game result':'B'}
                break
            if inccheck[code][0]:
                timers[code]['white'][0] += timers[code]['inc']
                inccheck[code][0] = False

            elif inccheck[code][1]:
                timers[code]['black'][0] += timers[code]['inc']
                inccheck[code][1] = False
            
            if timers[code]['white'][1]:
                timers[code]['white'][0] = oldw - time.time()

            elif timers[code]['black'][1]:
                timers[code]['black'][0] = oldb - time.time()


        if int(time.time())%30 == 15 and t0 != int(time.time()):
            t0 = int(time.time())
            if connection[code][0]-connection[code][1] >= 10:
                offers[code] = {'status':'gameover', 'resignations':None, 'draw offers':None, 'flagged':None, 'lost connection':'black', 'game result':'W'}
                break
            elif connection[code][1]-connection[code][0] >= 10:
                offers[code] = {'status':'gameover', 'resignations':None, 'draw offers':None, 'flagged':None, 'lost connection':'white', 'game result':'B'}
                break


@server.route('/',methods=['GET', 'POST'])
def troll():
    return flask.render_template('rickroll.html')

@server.route('/connect',methods=['POST','GET'])
def on_connect():
    return generate_code()


@server.route(f'/rooms',methods=['POST','GET'])
def host():
    global rooms, oldb, oldw, timers , debug, connection 
    if flask.request.method == 'POST':
        info = dict(flask.request.form)
        code = info['code']
        if 'status' in rooms:
            pass
        if code not in rooms:
            rooms[code] = info
            mintime = info['mintime']
            timer = False
            connection[code] = [0,0]
            offers[code] = {'status':'running', 'resignations':None, 'draw offers':None, 'flagged':None, 'lost connection':None, 'game result':None}
            if mintime.lower() != 'unlimited':
                mintime = int(mintime)*60   
                timers[code] = {'white' : [mintime , False] , 'black' : [mintime , False] , 'inc':int(info['inc']) , 'moveno':0 , 'mintime':mintime}
                inccheck[code] = [False, False]
                move_durations[code] = []
                timer=True
            else:
                timers[code] = {}
                move_durations[code] = []
            Thread(target=handle_room,args=(code,timer)).start()

        else :
            rooms[code] = info
            pawn_promo = (info['pppiece'] != '')
            try :
                if timers[code]:
                    if info['side'] == 'white':
                        oldb = timers[code]['black'][0] + time.time()
                        timers[code]['white'][1] = False
                        timers[code]['black'][1] = True
                        inccheck[code][0] = True
                        timers[code]['moveno'] += 1
                        move_durations[code] += [int(timers[code]['mintime'] - timers[code]['white'][0] + timers[code]['inc']*timers[code]['moveno'] - sum(move_durations[code][:-1:2]))]

                    elif info['side'] == 'black':
                        oldw = timers[code]['white'][0] + time.time()
                        timers[code]['black'][1] = False
                        timers[code]['white'][1] = True
                        inccheck[code][1] = True
                        move_durations[code] += [int(timers[code]['mintime'] - timers[code]['black'][0] + timers[code]['inc']*timers[code]['moveno'] - sum(move_durations[code][1:-1:2]))]
                else:
                    move_durations[code] += [0]

                if pawn_promo:
                    move_durations[code] += [-1]

            except Exception as er:
                pass
                #print(f'Some Error : {er}')
        return 'null'#flask.render_template()
    else:
        code = flask.request.args.get('code')
        try:
            return rooms[code]
        except :
            return 'null'

@server.route('/connection',methods=['POST','GET'])
def on_connection_recv():
    global connection
    if flask.request.method == 'GET':
        side = flask.request.args.get('side')
        code = flask.request.args.get('code')
        if code is None:
            pass
        else:
            connectoption = (flask.request.args.get('connectop') == 'True')
            try :
                if connectoption:
                    if side == 'white':
                        connection[code][0] += 1 
                    else:
                        connection[code][1] += 1
            except :
                pass
    
    elif flask.request.method == 'POST':
        info = dict(flask.request.form)
        code = info['code']
        if 'resign' in info:
            offers[code]['status'] = 'gameover'
            offers[code]['resignations'] = info['side']

        elif 'draw' in info:
            if not offers[code]:
                offers[code]['draw offers'] = info['side']
            else:
                offers[code]['draw offers'] = info['draw']
                if info['draw'] == 'accepted':
                    offers[code]['status'] = 'gameover'
                    offers[code]['game result'] = 'D'

        elif 'checkmate' in info:
            offers[code] = {'status':'gameover', 'resignations':None, 'draw offers':None, 'flagged':None, 'lost connection':None, 'game result':info['side'][0].upper()}

        elif 'reset' in info:
            offers[code] = {'status':'running', 'resignations':None, 'draw offers':None, 'flagged':None, 'lost connection':None, 'game result':None}

        elif 'clean' in info:
            clean(code)

    try :
        return {'connection':connection[code] , 'timers':timers[code] , 'offers':offers[code] , 'move durations':move_durations[code]}
    except Exception as e:
        return 'null'


@server.route('/buffer',methods=['POST','GET'])
def debug_():
    global connection
    return move_durations, connection
    
server.run(debug=1,host='192.168.1.104',port=7979)
