from flask import Flask
from test import obj_size

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/view')
def size():
    obj = obj_size('./1.jpg', 0.955)
    return obj.compute()

if __name__ == '__main__':
    app.run()