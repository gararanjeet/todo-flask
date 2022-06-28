from ..extensions import db, ma
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


task_schema = TasksSchema()
tasks_schema = TasksSchema(many=True)