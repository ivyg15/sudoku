from app import app
from flask import request, render_template, jsonify

@app.route('/')
def index():
    return render_template('index.html')

from app import functions

@app.route('/submit_data', methods=['POST'])
def submit_data():
    sudoku = [[[0 for i in range(9)] for j in range(9)] for k in range(9)]
    data = request.form
    for i in range(1, 10):
        for j in range(1, 10):
            pencils = data.get(f"{i}{j}")
            if pencils is not None:
                pencils = int(pencils)
                while pencils > 0:
                    sudoku[i-1][j-1][pencils%10-1] = 1
                    pencils //= 10

    functionName = data.get("function")
    if functionName == "- - -":
        response = []
    else:
        chosenFunction = functions.functionsDict[data.get("function")]
        response = chosenFunction(sudoku)
    return jsonify({"message": response})