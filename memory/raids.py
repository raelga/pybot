import datetime
import os
import sys
import re

init_path = './memory/__raids__/'
hours = ['10:00','16:00','20:00','22:30']
difficulties = ['hard']

date = datetime.datetime.today()
next_init = date + datetime.timedelta(days=(8 - date.weekday()))
next_end = next_init + datetime.timedelta(days=6)
current_end = date + datetime.timedelta(days=(7 - date.weekday()))
current_init = current_end - datetime.timedelta(days=6)


def format_date(date):
    date=date.strftime("%d-%m-%y")
    return date

def week_file(day):
    r = day.split('-')
    d = datetime.datetime(int(r[2]), int(r[1]), int(r[0]))
    now_wd = date.weekday()
    req_wd = d.weekday()
    week = ''
    if (now_wd == 1) or (now_wd == 0 and req_wd == 0) or (now_wd >= 2 and req_wd >= now_wd):
        week = 'current'
    else:
        week = 'next'

    if week == 'current':
        p = init_path+'Destiny_'+format_date(current_init)+'_'+format_date(current_end)+'.txt'
    if week == 'next':
        p = init_path+'Destiny_'+format_date(next_init)+'_'+format_date(next_end)+'.txt'
    return(p)

def convert_date(day):
    iday = None
    if day.lower() == 'lunes':
        iday=int('0')
    elif day.lower() == 'martes':
        iday=int('1')
    elif day.lower() == 'miercoles' or day.lower() == 'miércoles':
        iday=int('2')
    elif day.lower() == 'jueves':
        iday=int('3')
    elif day.lower() == 'viernes':
        iday=int('4')
    elif day.lower() == 'sabado' or day.lower() == 'sábado':
        iday=int('5')
    elif day.lower() == 'domingo':
        iday=int('6')
    elif day.lower() == 'hoy':
        iday=date.weekday()
    elif day.lower() == 'mañana':
        iday=date.weekday()+1

    if iday:
        day = date + datetime.timedelta(days=(iday - date.weekday()))
        return(format_date(day))
    else:
        return(day)

def create_file(m, p):
    if m == 'current':
        first_day = current_init
    elif m == 'next':
        first_day = next_init
    with open(p, 'w') as f:
        for i in range(7):
            print(format_date(first_day + datetime.timedelta(days=i))+'\n', file=f)
            for difficulty in difficulties:
                print(difficulty+'\n', file=f)
                for hour in hours:
                    print(hour+'\n', file=f)

def new_week():
    c = init_path+'Destiny_'+format_date(current_init)+'_'+format_date(current_end)+'.txt'
    if not os.path.isfile(c):
        create_file('current',c)
    n = init_path+'Destiny_'+format_date(next_init)+'_'+format_date(next_end)+'.txt'
    if os.path.isfile(n):
        return('Ya se han creado convocatorias para la siguiente semana.')
    else:
        create_file('next',n)
        return('Convocatorias creadas!!')

def see_raid(day, difficulty, hour):
    day_point = None
    diff_point = None
    hour_point = None
    result = []

    if day:
        day = convert_date(day)
        p = week_file(day)

        with open(p, 'r') as fr:
            get_all = fr.readlines()
        
        for i,line in enumerate(get_all):
            if day.lower() in line.lower():
                day_point = i
            elif day_point and difficulty.lower() in line.lower():
                diff_point = i
                day_point = None
            elif diff_point and hour.lower() in line.lower():
                hour_point = i
                diff_point = None
            elif hour_point:
                r = re.search(r'^(\d).', line, re.I)
                if r:
                    hour_point = i
                else:
                    hour_point = None
            elif re.search( r'^\d\d-\d\d-\d\d', line, re.I):
                day_point = None
                diff_point = None
                hour_point = None
 
            if day_point:
                result.append(line)
            elif diff_point:
                result.append(line)
            elif hour_point:
                result.append(line)

        if result:
            return(''.join(result))
        else:
            return('No se ha encontrado esa convocatoria.')
                    
    else:
        c = init_path+'Destiny_'+format_date(current_init)+'_'+format_date(current_end)+'.txt'
        return(c)

def manage_player(name, day, difficulty, hour):
    day_point = None
    diff_point = None
    hour_point = None
    delete_point = None
    newline = None
    dropline = None
    pos = int(1)
    day = convert_date(day)
    p = week_file(day)
    result = 'No se ha encontrado esa convocatoria.'

    with open(p, 'r') as fr:
        get_all = fr.readlines()
    
    with open(p, 'w') as f:
        for i,line in enumerate(get_all):
            if day.lower() in line.lower():
                day_point = i
            elif day_point and difficulty.lower() in line.lower():
                diff_point = i
                day_point = None
            elif diff_point and hour.lower() in line.lower():
                hour_point = i
                diff_point = None
            elif hour_point:
                d = re.search(r'^(\d). '+name, line, re.I)
                r = re.search(r'^(\d).', line, re.I)
                if d:
                    delete_point = i
                    result='Jugador eliminado.'
                elif r and delete_point:
                    pos = int(r.group(1))-1
                    dropline = line.replace(r.group(1), str(pos))
                elif delete_point:
                    delete_point = None
                    hour_point = None
                elif r:
                    pos = int(r.group(1))+1
                else:
                    newline = str(pos)+'. '+name+'\n'
                    result='Jugador añadido.'                    
                    hour_point = None
                    
            if dropline:
                f.writelines(dropline)
                dropline = None
            elif newline:
                f.writelines(newline)
                f.writelines(line)
                newline = None
            elif delete_point:
                None
            else:
                f.writelines(line)
    return(result)
                
                    
def raids(words):
    nw = re.search( r'(?:^.|^)\braid\b.*crea.*conv.*', words, re.I|re.M)
    sr = re.search( r'(?:^.|^)\braid\b.*ver.*conv\S*\s*(\S*)\s*(\S*)\s*(\S*)', words, re.I|re.M)
    mp = re.search( r'(?:^.|^)\braid\b\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)', words, re.I|re.M)
    if nw:
        return(new_week())
    elif sr:
        date = sr.group(1)
        difficulty = sr.group(2)
        hour = sr.group(3)
        if ':' in hour:
            None
        elif ':' in difficulty:
            difficulty = '***'
            hour = '***'
        else:
            hour = '***'
            
        return(see_raid(date, difficulty, hour))
    elif mp:
        name = mp.group(1)
        date = mp.group(2)
        difficulty = mp.group(3)
        hour = mp.group(4)
        return(manage_player(name, date, difficulty, hour))


def hear(words):
    return raids(words)

def main(argv):
    if len(sys.argv)>1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')
    print(hear('/raid Rael hoy 10:00'))

if __name__ == "__main__":
    main(sys.argv)
