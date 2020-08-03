import csv

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

@app.route('/<string:page_name>')
def other_pages(page_name):
    return render_template(page_name)

