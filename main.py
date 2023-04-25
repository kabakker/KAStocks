from flask import Flask, render_template, request
from ManageDB import ManageDB

app = Flask(__name__)
db = ManageDB()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        searchTerm = request.form['text']
        search_result = db.search_stock(searchTerm)
        return render_template('index.html', search_result=search_result)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
