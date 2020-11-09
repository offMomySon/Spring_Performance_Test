from flask import Flask, request, jsonify
from manipulateK6 import testJarServer

app = Flask(__name__)

@app.route('/actTest/<testType>/<testApi>/<userCount>')
def testK6(testType,testApi,userCount):
    
    print(testType)
    print(testApi)
    print(userCount)
    #print(testType,testApi,userCount)
#    res = testJarServer(testType, testApi,int(userCount))

    avgRequestProcessTime, perRequestNum, requestNum =  testJarServer(testType, testApi,int(userCount))

    return jsonify({"avg":avgRequestProcessTime, "per":perRequestNum, "req":requestNum})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

