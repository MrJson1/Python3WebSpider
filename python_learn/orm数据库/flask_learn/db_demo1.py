from flask import Flask
from flask import request
from  flask_sqlalchemy   import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

db.create_all()

@app.route('/names/<name>')
def hello_world(name):
    return 'Hello %s' % name

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent

if __name__ == '__main__':
    app.run(debug=True)