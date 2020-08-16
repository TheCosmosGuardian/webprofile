import csv
import random

from flask import Flask, render_template, request, redirect
app = Flask(__name__)
print(__name__)


def wrt_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

@app.route('/', methods=['POST', 'GET'])
def my_home():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            wrt_to_csv(data)
            return redirect('index.html')
        except:
            return 'did not save to database'
    else:
        return render_template('index.html')

def possible(y,x,n,grid):
    for i in range(0,9):
        if grid[y][i] == n:
            return False
    for i in range(0,9):
        if grid[i][x] == n:
            return False
    x0 = (x//3)*3
    #print(f'X0 = {x0}')
    y0 = (y//3)*3
    #print(f'Y0 = {y0}')
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j] == n:
                return False
    return True

def solver(grid):
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if possible(y,x,n,grid):
                        grid[y][x] = n
                        solver(grid)
                        if 0 not in grid[8]:
                            return grid
                        grid[y][x] = 0
                return


@app.route('/sudoku', methods=['POST', 'GET'])
def sudoku():
    if request.method == 'POST':
        sdk_dict = request.form.to_dict()
        sdk_list = [0 if sdk_dict[k] ==  '' else int(sdk_dict[k]) for k,v in sdk_dict.items()]
        grid = [sdk_list[i:i+9] for i in range(0, len(sdk_list), 9)]
        data = solver(grid)
        response = {}
        if isinstance(data, list):
            response['message_type'] = 'success'
            response['data'] = data
        else:
            response['message_type'] = 'failure'
        return render_template('sudoku_results.html', response=response)
    else:
        return render_template('sudoku.html')
    return render_template('sudoku.html')

@app.route('/lottery', methods=['POST', 'GET'])
def lotto():
    kwargs = {'my_title': "Lotto QuickPick Machine",
              'my_heading': "Lotto QuickPick Machine",
              'my_paragraph': ""}
    if request.method == 'POST':
        numbers = []
        for i in range(8):
            numbers.append([])
            for j in range(6):
                rand = random.randint(1, 50)
                while rand in numbers[i]:
                    rand = random.randint(1, 50)
                numbers[i].append(rand)
            numbers[i].sort()
        response = {}
        response['message_type'] = 'lottery_response'
        response['columns'] = ['A', 'B', 'C', 'D', 'E', 'F']
        response['data'] = numbers
        return render_template('lottery.html', context=kwargs, response=response)
    return render_template('lottery.html', context = kwargs, response={'message_type': "others"})

