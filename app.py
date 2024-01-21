from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Create Flask instance
app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'your_secret_key_here'

#Add a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

#Initialize database
db = SQLAlchemy(app)

#Data model
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False) 
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    all_tasks = Tasks.query.order_by(Tasks.date_added)
    if all_tasks:
        print(all_tasks)
    else:
        print("tasks are empty.")
    return render_template("index.html", all_tasks=all_tasks)

@app.route("/add", methods=["GET", "POST"])
def add():
    todo = request.form['task']
    desc = request.form['desc']
    task = Tasks(title=todo, description=desc)
    db.session.add(task)
    db.session.commit()
    print("Attempted to add a task.")
    return redirect(url_for("index"))

@app.route("/get_all",  methods=["GET"])
def get_all():
    all_tasks = Tasks.query.order_by(Tasks.date_added)
    return all_tasks

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    task_to_edit = Tasks.query.get_or_404(index)
    if request.method == "POST":
        task_to_edit.title = request.form['new_title']
        task_to_edit.description = request.form['new_desc']
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", task_to_edit=task_to_edit)

@app.route("/delete/<int:index>")
def delete(index):
    task_to_delete = Tasks.query.get_or_404(index)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

