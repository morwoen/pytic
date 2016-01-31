from flask import Flask, render_template, session, request
import game
import random, copy

app = Flask(__name__)
app.config["SECRET_KEY"] = "verysecretmuchlol"
app.config["DEBUG"] = True

game.load()

def aiTurn():
    board = session["board"]
    row, column = game.nextMove(board)
    if row == -1 or column == -1:
        return # no possible actions
    session["own"].append([copy.deepcopy(board), row, column])
    board[row][column] = "o"

def resetSession():
    del session["board"]
    del session["own"]
    del session["player"]

@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [["", "", ""],
                            ["", "", ""],
                            ["", "", ""]]

        first = random.randint(0, 1)
        session["own"] = []
        session["player"] = []

        # 0 AI 1 Hooman
        if first:
            message = "You play first!"
        else:
            # execute action
            aiTurn()

    board = session["board"]

    if "column" in request.args and "row" in request.args:
        column = int(request.args["column"]) - 1
        row = int(request.args["row"]) - 1

        if not board[row][column]:
            # field empty can be set
            session["player"].append([copy.deepcopy(board), row, column])
            board[row][column] = "x"
            if not game.isWinning(board):
                aiTurn()
        else:
            message = "Invalid action"

    winner = game.isWinning(board)
    tie = game.isTie(board)
    if winner or tie:
        if winner == "x":
            # player won
            # game.remember(session["own"], False)
            game.remember(session["player"])
            game.lost()
        elif winner == "o":
            # ai won
            game.remember(session["own"])
            # game.remember(session["player"], False)
            game.won()
        elif tie:
            game.remember(session["own"])
            game.remember(session["player"])
            game.tie()

        game.save()
        resetSession()

    return render_template("index.html", **locals())

if __name__ == "__main__":
    app.run()
