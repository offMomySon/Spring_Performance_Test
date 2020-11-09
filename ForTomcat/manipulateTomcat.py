import os
import fileinput
import sys
import subprocess

def removeLog():
    os.system('''rm -rf /root/log ''')

def activeJar(mem,con):
    subprocess.Popen(['java','-Xms'+str(mem)+'m', '-Xmx'+str(mem)+'m', '-jar', '/root/jarFolder/reservation_'+str(con)+'.jar'])

def killJar():
    os.system('''pkill -9 -ef '\-jar'  ''')

def checkJavaCpu():
    mem = ''
    cpu = ''
    newProcessInfo = []
    for x in os.popen('ps h -eo pid:1,command,pmem,pcpu | grep java'):
        res  = x.rstrip('\n').split(' ')
        
        newProcessInfo = []
        for x in res:
            if x != '':
                newProcessInfo.append(x)


        f = open("/root/testRes", 'a')
        for nInfo in newProcessInfo:
            reStr = nInfo + ','
            f.write(reStr)
        f.write('\n')
        f.close()

        if newProcessInfo[1] == 'java':
           mem = newProcessInfo[5]
           f = open("/root/testRes", 'a')
           f.write("5th value - "+ newProcessInfo[6] + ".\n")
           f.close()
           print(newProcessInfo[6])
           cpu = newProcessInfo[6].strip().replace("+","").replace("-","").replace("\n","").replace("\r","")
        
    if cpu == '':
        f = open("/root/testRes", 'a')
        f.write('''can't grep java process, temporary set cpu = 100\n''')
        f.close()
        cpu = "100"


    f = open("/root/testRes", 'a')
    data = "cpu - " + str(cpu) + "\n"
    f.write(data)
    f.close()

    return float(cpu)



