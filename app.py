import os
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)


class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append({"task": task, "done": False})

    def mark_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = True

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)


todo = ToDoList()

TEMPLATE = """
<!doctype html>
<html>
<head><title>To-Do List</title></head>
<body style="font-family: sans-serif; max-width: 500px; margin: 40px auto;">
  <h2>📋 My To-Do List</h2>

  <form action="/add" method="post">
    <input type="text" name="task" placeholder="Enter a task" required>
    <button type="submit">Add</button>
  </form>

  <ul>
    {% for i, t in tasks %}
      <li>
        {% if t.done %}✔️{% else %}⏳{% endif %}
        {{ t.task }}
        <a href="/done/{{ i }}">[mark done]</a>
        <a href="/remove/{{ i }}">[remove]</a>
      </li>
    {% endfor %}
  </ul>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(TEMPLATE, tasks=list(enumerate(todo.tasks)))


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        todo.add_task(task)
    return redirect(url_for("index"))


@app.route("/done/<int:index>")
def done(index):
    todo.mark_done(index)
    return redirect(url_for("index"))


@app.route("/remove/<int:index>")
def remove(index):
    todo.remove_task(index)
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False)
