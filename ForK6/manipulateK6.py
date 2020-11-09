import os
import re
import subprocess

def testJarServer(testType,testApi,userCount):

    args = ["k6","run", "--vus", str(userCount), "--duration", "30s", "/root/"+testType+"/"+testApi+".js" ]
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    output, errors = proc.communicate("result\n")

    return parseResult(output);

def parseResult(res):
    f = open("testResult.txt","w")
    f.write(res)
    f.close()

    requestNum = 0
    perRequestNum = ''
    avgRequestProcessTime = ''
    f = open("testResult.txt","r")
    line_data = f.readline()
    while line_data:
        if line_data.find("http_req_waiting") != -1:
            print("http_req_waiting find")
            httpReqWaiting = line_data.replace('\n','').split(' ')

            newHttpReqWaiting = []
            for x in httpReqWaiting:
                if x != '':
                    newHttpReqWaiting.append(x)

            print(httpReqWaiting)
            print(newHttpReqWaiting)
            print("split")
            avgRequestProcessTime = newHttpReqWaiting[1]

        if line_data.find("http_reqs") != -1:

            print("http_reqs find")
            httpReq = line_data.replace('\n','').split(' ')

            newHttpReq = []
            for x in httpReq:
                if x != '':
                    newHttpReq.append(x)

            print(httpReq)
            print(newHttpReq)
            print("split")

            requestNum = newHttpReq[1]
            perRequestNum = newHttpReq[2]

        line_data = f.readline()
    f.close()

    avgRequestProcessTime = avgRequestProcessTime.replace('\n','')
    perRequestNum = perRequestNum.replace('\n','')
    requestNum = requestNum.replace('\n','')

    return avgRequestProcessTime, perRequestNum, requestNum
