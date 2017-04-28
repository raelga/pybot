import time
import os
import sys
import re
import sqlite3

INIT_PATH = '.raids'
DB_PATH = INIT_PATH + '/pybot'

indent = ' '

def date_parser(date):
    """Function to parse the date to an universal format"""
    date = date.replace('-', ' ').replace('/', ' ')
    if re.search(r'(\d{4}$)', date):
        conv = time.strptime(date, "%d %m %Y")
    else:
        conv = time.strptime(date, "%d %m %y")
    date = time.strftime("%d/%m/%Y", conv)
    return(date)

def hour_parser(hour):
    """Function to parse the hour to an universal format"""
    if ':' in hour:
        conv = time.strptime(hour, "%H:%M")
    else:
        conv = time.strptime(hour, "%H")
    hour = time.strftime("%H:%M", conv)
    return(hour)

def get_game(chat_id):
    """Function to get game by chat, you have to set the properly id"""
    cg_matrix = [(37284770,'destiny'),
                (54322,'division')]
    for c, g in cg_matrix:
        if c == chat_id:
            game = g
            return(game)

def get_values(data):
    """Function to get the values"""
    game = None
    day = None
    mode = ''
    hour = None
    psnid = None
    info = ''

    d = re.search( r'(\d+(?:-|\/)\d+(?:-|\/)\d+)', data, re.I) #Search the date
    if d:
        day = date_parser(d.group(1))
        h = re.search( r'(?:\d+(?:-|\/)\d+(?:-|\/)\d+)\s+(\S+)', data, re.I) #Search the hour based on date
        if h:
            hour = hour_parser(h.group(1))
        p = re.search( r'(?:\d+(?:-|\/)\d+(?:-|\/)\d+)\s+(?:\S+)\s+(\S+)', data, re.I) #Search the psnid based on date and hour
        if p:
            psnid = p.group(1).lower()
        m = re.search( r'(.+)\s+(?:\d+(?:-|\/)\d+(?:-|\/)\d+)', data, re.I) #Search the mode based on date
        if m:
            mode = m.group(1).lower()
        i = re.search( r'(?:\d+(?:-|\/)\d+(?:-|\/)\d+)\s+(?:\S+)\s+(?:\S+)\s+(.+)', data, re.I) #Search aditional info based on date, hour and psnid
        if i:
            info = i.group(1).lower()

    return(game, mode, day, hour, psnid, info)

def init_table():
    """Function to create the init DB and table if doesn't exists"""
    if not os.path.exists(INIT_PATH):
        os.makedirs(INIT_PATH)
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS fireteams
                   (chatid INTEGER NOT NULL,
                    userid INTEGER NOT NULL,
                    game TEXT NOT NULL,
                    mode TEXT,
                    day TEXT NOT NULL,
                    hour TEXT NOT NULL,
                    psnid TEXT NOT NULL,
                    info TEXT,
                    timestamp TEXT NOT NULL,
                    UNIQUE (day, hour, psnid))""")
    con.commit()
    con.close()

def exec_sql(sql):
    """Function to execute an sql command"""
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    try:
        cursor.execute(sql)
        row = cursor.fetchall()
        con.commit()
        con.close()
        return(row)
    except:
        con.close()
        return()

def fireteam_query(game, mode, day, hour):
    """Function to query a fireteam"""
    result = []

    if mode:
        append_sql = "and mode = '"+mode+"'"
    else:
        append_sql = 'and mode = ""'

    if not day:
        return('Día incorrecto.')
    else:
        sql = ''
        result.append(day)
        if not hour:
            sql = """select distinct hour from fireteams where day = '"""+day+"""' and game = '"""+game+"""' order by hour"""
            hours = exec_sql(sql)
            for hour in hours:
                result.append(indent*1 + hour[0])
                if not mode:
                    sql = """select distinct mode from fireteams where day = '"""+day+"""' and game = '"""+game+"""' and hour = '"""+hour[0]+"""' order by mode"""
                    modes = exec_sql(sql)
                    for mode in modes:
                        if mode[0]:
                            result.append(indent*2 + mode[0].upper())
                        sql = """select psnid, info from fireteams where day = '"""+day+"""' and game = '"""+game+"""' and hour = '"""+hour[0]+"""' and mode = '"""+mode[0]+"""' order by timestamp"""
                        rows = exec_sql(sql)
                        for row in rows:
                            result.append(indent*3 + row[0] + indent*1 + row[1])
                        result.append('')
                else:
                    result.append(indent*2 + mode.upper())
                    sql = """select psnid, info from fireteams where day = '"""+day+"""' and game = '"""+game+"""' and hour = '"""+hour[0]+"""' """+append_sql+""" order by timestamp"""
                    rows = exec_sql(sql)
                    for row in rows:
                        result.append(indent*3 + row[0] + indent*1 + row[1])
        else:
            result.append(indent*1 + hour)
            if not mode:
                sql = """select distinct mode from fireteams where day = '"""+day+"""' and game = '"""+game+"""' and hour = '"""+hour+"""' order by mode"""
                modes = exec_sql(sql)
                for mode in modes:
                    if mode[0]:
                        result.append(indent*2 + mode[0].upper())
                    sql = """select psnid, info from fireteams where day = '"""+day+"""' and game = '"""+game+"""' and hour = '"""+hour+"""' and mode = '"""+mode[0]+"""' order by timestamp"""
                    rows = exec_sql(sql)
                    for row in rows:
                        result.append(indent*3 + row[0] + indent*1 + row[1])
                    result.append('')
            else:
                result.append(indent*2 + mode.upper())
                sql = """select psnid, info from fireteams where day = '"""+day+"""' and game = '"""+game+"""' and hour = '"""+hour+"""' """+append_sql+""" order by timestamp"""
                rows = exec_sql(sql)
                for row in rows:
                    result.append(indent*3 + row[0] + indent*1 + row[1])

    return('\n'.join(result))

def insert_player(chat_id, user_id, game, mode, day, hour, psnid, info):
    """Function to insert players"""
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    sql = """INSERT INTO fireteams
                   (chatid, 
                   userid, 
                   game,
                   mode,
                   day,  
                   hour,
                   psnid,
                   info,
                   timestamp)
                   VALUES
                   ("""+str(chat_id)+""",
                   """+str(user_id)+""",
                   '"""+game+"""',
                   '"""+mode+"""',
                   '"""+day+"""',
                   '"""+hour+"""',
                   '"""+psnid+"""',
                   '("""+info+""")',
                   (SELECT datetime(\'now\')))"""
    try:
        cursor.execute(sql)
        con.commit()
        con.close()
        return('Jugador añadido.')
    except sqlite3.IntegrityError:
        con.rollback()
        con.close()
        return('del_player')

def delete_player(user_id, day, hour, psnid):
    """Function to delete players"""
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    check = exec_sql("""SELECT COUNT(*) FROM fireteams WHERE
                   userid = """+str(user_id)+""" AND
                   day = '"""+day+"""' AND
                   hour = '"""+hour+"""' AND
                   psnid = '"""+psnid+"""'""")
    
    if check[0][0] == 0:
        return('El jugador debe ser eliminado por quien le registró.')
    
    sql = """DELETE FROM fireteams WHERE
                   userid = """+str(user_id)+""" AND
                   day = '"""+day+"""' AND
                   hour = '"""+hour+"""' AND
                   psnid = '"""+psnid+"""'"""
    try:
        cursor.execute(sql)
        con.commit()
        con.close()
        return('Jugador eliminado.')
    except:
        con.rollback()
        con.close()
        return('Me encuentro mal...')


def fireteams(words, chat_id, user_id):
    """Function to manage fireteams"""
    r = re.search( r'(?:^|^\/|^\@\S+:.+)\braid\b(.*)', words, re.I|re.M) #Edit mode
    s = re.search( r'(?:^|^\/|^\@\S+:.+)\braid\b\s+\b(?:ver|mostrar)\b(.*)', words, re.I|re.M) #Search mode
    if s:
        data = s.group(1)
    elif r:
        data = r.group(1)
    
    if data:
        init_table()
        game, mode, day, hour, psnid, info = get_values(data)
        
        if not game:
                game = get_game(chat_id)

        if s:
            result = fireteam_query(game, mode, day, hour)
        else:
            if not day:
                return('Día incorrecto.')
            elif not hour:
                return('Hora incorrecta.')
            elif not psnid:
                return('PSNid incorrecto.')
            
            result = insert_player(chat_id, user_id, game, mode, day, hour, psnid, info)
            
            if result == 'del_player':
                result = delete_player(user_id, day, hour, psnid)

        return(result)

def raid(message):
    return fireteams(message.text, message.chat.chat_id, message.user.user_id)

def main(argv):
    if len(sys.argv)>1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')

if __name__ == "__main__":
    main(sys.argv)
