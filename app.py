from flask import Flask, jsonify
from tinydb import TinyDB

app = Flask(__name__)

db = TinyDB('db.json')

@app.route('/poslowie', methods=['GET'])
def main():
	data = db.all()
	return jsonify(data)

if __name__ == '__main__':
	app.run(host='0.0.0.0')