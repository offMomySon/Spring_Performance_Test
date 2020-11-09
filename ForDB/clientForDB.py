from flask import Flask, request, jsonify
from manipulateDb import setDBconntionCount, resetDB

app = Flask(__name__)
 
@app.route('/resetDB')
def resetDb():
    resetDB()
    return jsonify({"result":True})
 
@app.route('/db/<connectionCount>')
#@app.route('/environments/<language>')
def environments(connectionCount):
    setDBconntionCount(int(connectionCount))
    return jsonify({"con":int(connectionCount)})
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

