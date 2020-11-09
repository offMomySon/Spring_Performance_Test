#!/usr/bin/env python
import os
import re
import subprocess

def setDBconntionCount(conCount):

    proc = subprocess.Popen(["mysql","-uconnectuser", "-pconnect123!@#"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    output, errors = proc.communicate("set global max_connections="+str(conCount))
    print(output)

    proc = subprocess.Popen(["mysql","-uconnectuser", "-pconnect123!@#"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    output, errors = proc.communicate("set global mysqlx_max_connections="+str(conCount))
    print(output)

def resetDB():
    os.system('''mysql -u connectuser -p'connect123!@#' connectdb < /root/resetSQL.sql''')
    #proc = subprocess.Popen(["mysql","-uconnectuser", "-pconnect123!@#"],
    #        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    #output, errors = proc.communicate("source /root/resetSQL.sql")
    #print(output)


