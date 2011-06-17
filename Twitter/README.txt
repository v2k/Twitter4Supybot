###
# Copyright (c) 2011, robbe
#
# needs twitter-1.4.2-py2.5.egg -> http://pypi.python.org/pypi/twitter/1.4.2
# installed and authed appropriately
# Use twglobal only on private ircd server, deprecated on IRCnet for example
#  _______       _ _   _              _  _   
# |__   __|     (_) | | |            | || |  
#    | |_      ___| |_| |_ ___ _ __  | || |_ 
#    | \ \ /\ / / | __| __/ _ \ '__| |__   _|
#    | |\ V  V /| | |_| ||  __/ |       | |  
#    |_| \_/\_/ |_|\__|\__\___|_|       |_|  
#                                           
#                                           
#   _____                   _           _   
#  / ____|                 | |         | |  
# | (___  _   _ _ __  _   _| |__   ___ | |_ 
#  \___ \| | | | '_ \| | | | '_ \ / _ \| __|
#  ____) | |_| | |_) | |_| | |_) | (_) | |_ 
# |_____/ \__,_| .__/ \__, |_.__/ \___/ \__|
#              | |     __/ |                
#              |_|    |___/                 
#
# Twitter for Supybot * version 0.10
# robbe@email.de
#
###

-   Vorraussetzungen
        - Installierter Supybot
        - Python Lib 'phython-irclib-0.4.8'
        - Python Lib 'twitter-1.4.2.tar.gz'
        Dies setzt mindestens Python2.5 oder hoeher vorraus!!

    twitter-1.4.2-py2.5.egg -> http://pypi.python.org/pypi/twitter/1.4.2

-   Installation
        Einfach das Verzeichnis Twitter aus dem Archiv in das gewünschte
        plugin-Verzeichnis kopieren. Dann sollte das Plugin Twitter mit dem
        Supybot-Cmd 'load Twitter' geladen werden koennen

-   Konfiguration
        Supybot-Cmd 'search Twitter' zeigt alle configurierbaren Variablen
        Supybot-Cmd 'config supybot.plugins.Twitter.command' sollte den
            pfadnamen des cmdline-tools zurueck geben.
            Beispiel '/usr/bin/twitter'

-   Bedienung
        Es stehen die Befehle twfriends, twglobal, twreplies, twversion zur
        Verfuegung. Die Ausgabe erscheint in dem Channel oder Query, in dem
        der entsprechende Befehl ausgefuehrt wird!
        
        Mit Hilfe des Scheduler plugins ist kann eine automatisierte Ausgabe
        erfolgen. Dabei muss die zu erwartende Menge an Zeilen geringer sein
        als der in den options konfiguierte Wert da sonst Zeilenverlust droht.
        Entsprechend muss der Schedulerinterval gewaehlt werden!

        Supybot-Cmd 'scheduler repeat twf 60 twfriends'
        
        gibt die neuen Textzeilen, denen ich auf twitter.com folge, im Abstand
        von 60 Sekunden aus.
        
        Thats it, have fun!
        
        