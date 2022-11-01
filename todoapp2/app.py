
from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://brian:brian@localhost:5432/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)

class Todo(db.Model):
  __tablename__='todos'
  id=db.Column(db.Integer, primary_key=True)
  description=db.Column(db.String(), nullable=False)
  completed=db.Column(db.Boolean, nullable=False, default=False)
  list_id=db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

  def __repr__(self):
    return f'<Todos {self.id} {self.description}>'

class Todolist(db.Model):
  __tablename__="todolists"
  id=db.Column(db.Integer, primary_key=True)
  name=db.Column(db.String(), nullable=False)
  todos=db.relationship('Todo', backref='list', lazy=True)



@app.route('/todos/create', methods=['POST'])
def create_todos():
  try:
      description=request.get_json()['description']
      todo=Todo(description=description)
      db.session.add(todo)
      db.session.commit()
      return ({
            'description': todo.description
        })
  except:
    db.session.rollback()
    error=True
    print(sys.exc_info())
  finally:
    db.seesion.close()

@app.route('/todos/<todo_id>/set-completed',methods=['POST']) 
def edit(todo_id):
  try:
    completed=request.get_json()['completed'] 
    todo=Todo.query.get(todo_id)
    todo.completed=completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))  

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
  return render_template('index.html',lists=Todolist.query.all(), 
  active_list=Todolist.query.get(list_id),
  data=Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
  return redirect(url_for('get_list_todos', list_id=1))

@app.route('/')
def hello():
  return render_template('index.html',  data=Todo.query.all().order_by('id').all())

