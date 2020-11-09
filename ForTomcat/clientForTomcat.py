from flask import Flask, request, jsonify
from manipulateTomcat import activeJar, killJar, checkJavaCpu, removeLog

app = Flask(__name__)

@app.route('/endJAR')
def endJar():
    killJar()
    return jsonify({"result":True})

@app.route('/startJAR/<memCapacity>/<connectionPool>')
def startJar(memCapacity, connectionPool):
    print(memCapacity)
    print(connectionPool)
    activeJar(int(memCapacity), int(connectionPool))
    return jsonify({"result":True})

@app.route('/checkMEM')
def checkMem():
    cpu = checkJavaCpu()
    return jsonify({"cpu": cpu})

@app.route('/removeLog')
def remove():
    removeLog()
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9841, debug=True)

