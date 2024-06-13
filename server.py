import random
import server_ops as sdk

from flask import Flask, render_template, request, redirect,url_for
app = Flask(__name__)
print(__name__)


app = Flask(__name__)

severOps = sdk.ServerOps()


@app.route('/', methods=['POST', 'GET'])
def my_home():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            severOps.wrt_to_csv(data)
            return redirect(url_for('my_home'))
        except:
            return 'did not save to database'
    else:
        return render_template('index.html')


@app.route('/sudoku', methods=['POST', 'GET'])
def sudoku():
    if request.method == 'POST':
        sdk_dict = request.form.to_dict()
        sdk_list = [0 if sdk_dict[k] ==  '' else int(float(sdk_dict[k])) for k,v in sdk_dict.items()]
        grid = [sdk_list[i:i+9] for i in range(0, len(sdk_list), 9)]
        checker = severOps.validate_inputs(grid)
        data = severOps.solver(grid)
        response = {}
        if isinstance(data, list) and checker == 'Valid':
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
        numbers = random.sample(range(1,53),48)

        matrix = [numbers[i*6: (i+1)*6] for i in range(8)]

        response = {}
        response['message_type'] = 'lottery_response'
        response['columns'] = ['A', 'B', 'C', 'D', 'E', 'F']
        response['data'] = matrix
        return render_template('lottery.html', context=kwargs, response=response)
    return render_template('lottery.html', context = kwargs, response={'message_type': "others"})

