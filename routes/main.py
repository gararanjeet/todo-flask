from flask import Blueprint
from ..extensions import db
from ..models.tasks import task_schema, tasks_schema, Tasks

main = Blueprint("main", __name__)

@main.route("/addTask", methods=["POST"])
def addTask():
    task = request.json.get('task')
    isImportant = request.json.get('isImportant')
    isCompleted = False
    new_task = Tasks(task, isImportant, isCompleted)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

# update description of the task
@main.route("/modifyTask", methods=['PUT'])
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
@main.route("/toggleImportant", methods=["PUT"])
def toggleImportant():
    id = request.json.get("id")
    if id == None:
        return jsonify({"message":"Please provide id"}), 400
    task = Tasks.query.get(id)
    task.isImportant = bool(task.isImportant) ^ True
    db.session.commit()
    return jsonify({"message": "success"})

# toggle isCompleted flag
@main.route("/toggleComplete", methods=["PUT"])
def toggleComplete():
    id = request.json.get("id")
    if id == None:
        return jsonify({data:"Please provide id"}), 400
    task = Tasks.query.get(id)
    task.isCompleted = bool(task.isCompleted) ^ True 
    db.session.commit()
    return jsonify({"message":"success"})

# delete task
@main.route("/deleteTask", methods=["DELETE"])
def deleteTask():
    id = request.json.get("id")
    if id == None:
        return jsonify({"message":"Please provide id"}), 400
    task = Tasks.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({"message":"success"})