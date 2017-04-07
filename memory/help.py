#!/usr/bin/env python

import re
import sys

main_help = 'Para obtener ayuda de un tema específico escribe \'@raelbot ayuda *TEMA*\' con uno de los siguientes temas: \
\n-Raids \
\n-Trofeos'

raid = 'Para apuntarte o eliminarte de una raid debes escribir \'/raid *psnid* *día/fecha(DD-MM-AA)* *dificultad* *hora*\'. \
\nTambién puedes ver las convocatorias escribiendo \'/raid ver convocatoria *fecha* *dificultad* *hora*\'. \
\nEjemplos: \
\n/raid raelga hoy hard 10:00 \
\n/raid raelga 12-04-17 hard 10:00 \
\n/raid ver convocatoria mañana hard 10:00'

trophies='Pendiente de documentar'

def bot_help(words):

        r=re.search( r'(?:^.|^)\b\S*bot\b.*\bayuda\b\s*(\S*)', words, re.I|re.M)
        if r:
                if r.group(1).lower()=='raids':
                        return (raid)
                elif r.group(1).lower()=='trofeos':
                        return (trophies)
                else:
                        return (main_help)

def hear(words):
    return bot_help(words)

def main(argv):
    if len(sys.argv)>1:
        print(hear(' '.join(sys.argv)))
    else:
        print('I heard nothing.')

if __name__ == "__main__":
    main(sys.argv)
