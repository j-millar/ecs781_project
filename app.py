from flask import Flask, jsonify, request
import db

app = Flask(__name__)

@app.route('/coins', methods=["POST", "GET"])
def coins():
	if request.method == "POST":
		if not request.is_json:
			return jsonify({"msg": "Missing JSON"}), 400
		else:
			db.add_coins(request.get_json())
			return "coin info added", 200

	return db.get_coins()