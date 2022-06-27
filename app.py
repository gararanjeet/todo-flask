from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

db = SQLAlchemy(app)

ma = Marshmallow(app)

# configuring database uri
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

# Model
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(250))
    isCompleted = db.Column(db.Boolean, default = False)
    isImportant = db.Column(db.Boolean, default = False)

    def __init__(self, task, isCompleted = False, isImportant = False):
        self.task = task
        self.isCompleted = isCompleted
        self.isImportant = isImportant

# Schema
class TasksSchema(ma.Schema):
    class Meta:
        fields = ("id", "task", "isCompleted", "isImportant")

# Init Schemas
task_schema = TasksSchema()
tasks_schema = TasksSchema(many=True)

# get all tasks
@app.route("/")
def getTasks():
    tasks = Tasks.query.all()
    return tasks_schema.jsonify(tasks)

# add new task
@app.route("/addTask", methods=["POST"])
def addTask():
    task = request.json.get('task')
    isImportant = request.json.get('isImportant')
    isCompleted = False
    new_task = Tasks(task, isImportant, isCompleted)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

# update description of the task
@app.route("/modifyTask", methods=['PUT'])
def modifyTask():
    id = request.json.get("id")
    newTask = request.json.get("newTask")
    if id == None:
        return jsonify({"message":"Please provide id"}), 400
    elif newTask == "":
        return jsonify({"message":"Cannot update empty string"}), 400
    
    task = Tasks.query.get(id)
    task.task = newTask
    db.session.commit()
    return jsonify({"message":"success"})
        

# toggle isImportant flag
@app.route("/toggleImportant", methods=["PUT"])
def toggleImportant():
    id = request.json.get("id")
    if id == None:
        return jsonify({"message":"Please provide id"}), 400
    task = Tasks.query.get(id)
    task.isImportant = bool(task.isImportant) ^ True
    db.session.commit()
    return jsonify({"message": "success"})

# toggle isCompleted flag
@app.route("/toggleComplete", methods=["PUT"])
def toggleComplete():
    id = request.json.get("id")
    if id == None:
        return jsonify({data:"Please provide id"}), 400
    task = Tasks.query.get(id)
    task.isCompleted = bool(task.isCompleted) ^ True 
    db.session.commit()
    return jsonify({"message":"success"})

# delete task
@app.route("/deleteTask", methods=["DELETE"])
def deleteTask():
    id = request.json.get("id")
    if id == None:
        return jsonify({"message":"Please provide id"}), 400
    task = Tasks.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({"message":"success"})
    

if __name__ == "main":
    app.run(debug=True)