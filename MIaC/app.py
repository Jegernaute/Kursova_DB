from flask import Flask, jsonify
from models import User, Record, db

app = Flask(__name__)

@app.route('/statistics', methods=['GET'])
def get_statistics():
    num_users = User.query.count()
    num_records = Record.query.count()
    # Додайте інші агреговані дані, які вам потрібні
    return jsonify({
        'num_users': num_users,
        'num_records': num_records,
        # Додайте інші дані тут
    })

if __name__ == '__main__':
    app.run(debug=True)
