from flask import Flask, render_template, request
from database import db

def webSession(session, game_queue):
    app = Flask(__name__)
    print("TEST")
    game_queue.put({
        "for":"sys",
        "data":"API started and running on: 8080"
    })
    @app.route('/')
    def index():
        #game_queue.put({
        #    "for":"creatures",
        #    "data":"get_all_creatures"
        #})
        #try:
        #    msg = game_queue.get_nowait()
        #except:
        #    msg = "Error."
        #
        #creatures = msg['data']
        return render_template('index.html')

    @app.route('/cr')
    def creatures():
        inr = db.get_all_creatures(session)
        return f"{inr}"
    @app.route('/g')
    def gameScreen():
        return render_template('game.html')
    app.run(debug=False, host = '127.0.0.1', port=8080)