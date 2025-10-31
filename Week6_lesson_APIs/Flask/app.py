from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory list to store todos
todos = []
next_id = 1

# GET endpoint to fetch all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

# POST endpoint to add a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    global next_id
    data = request.get_json()

    if not data or 'task' not in data:
        return jsonify({'error': 'Task field is required'}), 400

    todo = {'id': next_id, 'task': data['task']}
    todos.append(todo)
    next_id += 1

    return jsonify(todo), 201  # 201 = Created


if __name__ == '__main__':
    app.run(debug=True)
