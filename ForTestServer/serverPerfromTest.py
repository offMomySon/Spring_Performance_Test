import requests
import time
import json

K6_IP = "3.131.116.5"

DB_IP = "3.134.162.196"
DB_MAX_CONNECTION_COUNT=["512"]
#DB_MAX_CONNECTION_COUNT=["125","256","512"]


#MEM = [["128","256","512","1024"]
#       ,["128","256", "512","1024", "2048", "4096", "8192"]]
MEM = [["512"]
        ,["512"]]


#TOMCAT_IP=["3.128.3.160","3.130.35.80"]
TOMCAT_IP=["3.130.35.80"]

#CONNECTION_POOL= ["20","40","100","200"]
CONNECTION_POOL= ["100"]

K6_IP = "3.131.116.5"
TEST_TYPE = [ "Tomcat_upspec"]
#TEST_TYPE = [ "Tomcat_load_balance"]

#VU = ["100","100","15","100","100","100","100"]
VU = ["100","100"]

#API_LIST = ["categories_api_test", "products_api_test",  "products_with_displayInfoId_api_test", "promotion_api_test", "rsv_GET_api",  "rsv_PUT_api", "rsv_POST_api"]
API_LIST = ["categories_api_test", "products_api_test"]


def tomCatCPUCheck(targetUrl):
    print( "start tomcat CPU check - " + targetUrl )
    count = 0
    while count < 5 :
        print("wait cpu to be stabilized. Count : " + str(count))
        cpuPer = getTomcatCpuPer(targetUrl)
        if isNotStablilized(cpuPer) :
            count = 0
            continue
        count = count + 1
    
    print("tomcat server stabilized")
    time.sleep(10)

def getTomcatCpuPer(targetUrl):
    #/checkMEM
    URL = "http://"+targetUrl+":9841/checkMEM"
    res = requests.get(URL)
    print(res.text)
    resDict = json.loads(res.text)
    time.sleep(5)
    return resDict["cpu"]

def isNotStablilized(cpuPer):
    if int(cpuPer) >= 10:
        return True
    return False

def startTomcat(targetUrl, mem, con):
    #/startJAR/<memCapacity>/<connectionPool>
    print("target - " + targetUrl)
    print("mem - " + mem)
    print("con - " + con)
    URL = "http://"+targetUrl+":9841/startJAR/" + mem + "/" + con
    print("URL - " + URL)
    res = requests.get(URL)
    print("start tomcat - " +  res.text)
    time.sleep(30)

def stopTomcat(tomcatUrl):
    #/endJAR
    #/removeLog
    endURL = "http://" + tomcatUrl + ":9841/endJAR"
    removeURL = "http://" + tomcatUrl + ":9841/removeLog"
    

    res = requests.get(removeURL)
    print("REMOVE Log res - " + res.text)
    
    time.sleep(10)

    res =requests.get(endURL)
    print("ENDJAR res - " + res.text)

    time.sleep(30)

def startTest(k6url, testType, testApi, vu):
    #'/actTest/<testType>/<testApi>/<userCount>'
    print("start Test api - " + testApi + ",vu - " + vu  + ". wait.. until finish")
    URL = "http://" + k6url + ":8080/actTest/" + testType + "/" + testApi + "/" + vu
    res = requests.get(URL)
    print("test res - " + res.text)
    return res.text

def writeTestRes(testAPI, testRes):
    f = open("/root/testRes", 'a')
    print("write res seq")
    resDict = json.loads(testRes)
    data = '''| ''' + testAPI + ''' | ''' + resDict['avg'] + ''' | ''' + resDict['per'] + ''' | ''' + resDict['req'] + ''' | ''' + "\n"
    f.write(data)
    f.close()

def resetDB(targetIp):
    #/resetDB
    URL = "http://" + targetIp + ":8080/resetDB"
    res = requests.get(URL)
    print( "RESET DB res : " + res.text)
    time.sleep(10)


def setDBconMax(targetIp, count):
    #/db/<connectionCount>
    URL = "http://" + targetIp + ":8080/db/" + count
    res = requests.get(URL)
    print( "setDB res : " + res.text)
    time.sleep(10)

def writeTestInit(dbMax, tomcatType, conPool, mem ):
    f = open("/root/testRes", 'a')
    data = "DB_MAX - " + dbMax  + ", TOMCAT - " + tomcatType + ", ConPool - " + conPool + ", MEM - "+ mem +"\n"
    f.write(data)
                
    data = '''| TS API | avg process time |per process request | request time   | \n'''
    f.write(data)
    
    data = '''|--      |--               |--                 |--           |--           | \n'''
    f.write(data)
    
    f.close()


#def startTomcat(targetUrl, mem, con):
for dbMaxIdx in range(len(DB_MAX_CONNECTION_COUNT)):
    setDBconMax(DB_IP, DB_MAX_CONNECTION_COUNT[dbMaxIdx])

    for tomcatTypeIdx in range(len(TEST_TYPE)):
        for conPoolIdx in range(len(CONNECTION_POOL)):
            for memIdx in range(len(MEM[tomcatTypeIdx])) :

                writeTestInit(DB_MAX_CONNECTION_COUNT[dbMaxIdx], TEST_TYPE[tomcatTypeIdx], CONNECTION_POOL[conPoolIdx], MEM[tomcatTypeIdx][memIdx] )

                for apiIdx in range(len(API_LIST)):
                    print('t start')
                    #startTomcat("3.128.3.160", "512", "100")
                    startTomcat("3.130.35.80", "512","100")    
                    
                    tomCatCPUCheck(TOMCAT_IP[tomcatTypeIdx])

                    testRes = startTest(K6_IP, TEST_TYPE[tomcatTypeIdx], API_LIST[apiIdx], VU[apiIdx])
                    writeTestRes(API_LIST[apiIdx], testRes)

                    #stopTomcat(TOMCAT_IP[tomcatTypeIdx])
                    stopTomcat("3.130.35.80")
                    #stopTomcat("3.128.3.160")

                    resetDB(DB_IP)


