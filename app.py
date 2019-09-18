from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="postgresql://localhost/mydb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usernames = db.Column(db.String(64), index=True, unique=False)
    content = db.Column(db.String(140), index=True)
    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    contents = Content.query.all()
    return render_template('index.html', contents=contents)

@app.route('/', methods=['POST'])
def post():
    if request.form['username'] and  request.form['content']:
        newContent = Content(usernames=request.form['username'], content=request.form['content'])
        db.session.add(newContent)
        db.session.commit()
        return render_template('result.html', username=request.form['username'], content=request.form['content'])   
    else:
        return render_template('error.html')

@app.cli.command('initdb')
def initdb_command():
    db.create_all()