from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask app
app = Flask(__name__, template_folder='templates')

# In-memory list to store to-do items
todos = []

# Route for the homepage. It will render the 'index.html' template and pass the list of todos.
@app.route('/')
def index():
    return render_template('todo.html', todos=todos)

# Route to add a new to-do item with priority and due date
@app.route('/add', methods=['POST'])
def add():
    task = request.form['todo']
    priority = request.form['priority']
    due_date = request.form['due_date']  # Expecting a format like YYYY-MM-DD

    # Append new task to the in-memory todos list
    todos.append({
        'task': task,
        'completed': False,
        'priority': priority,
        'due_date': due_date
    })

    return redirect(url_for('index'))

# Route to edit an existing to-do item
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    todo = todos[index]

    if request.method == 'POST':
        todo['task'] = request.form['todo']
        todo['priority'] = request.form['priority']
        todo['due_date'] = request.form['due_date']
        return redirect(url_for('index'))
    
    return render_template('edit.html', todo=todo, index=index)

# Route to check/uncheck a to-do item, toggling the 'completed' flag
@app.route('/check/<int:index>')
def check(index):
    todos[index]['completed'] = not todos[index]['completed']
    return redirect(url_for('index'))

# Route to delete a to-do item from the list
@app.route('/delete/<int:index>')
def delete(index):
    del todos[index]
    return redirect(url_for('index'))

# Route to filter tasks by completion status
@app.route('/filter/<status>')
def filter(status):
    if status == 'completed':
        filtered_todos = [todo for todo in todos if todo['completed']]
    elif status == 'pending':
        filtered_todos = [todo for todo in todos if not todo['completed']]
    else:
        filtered_todos = todos
    
    return render_template('todo.html', todos=filtered_todos)

if __name__ == '__main__':
    app.run(debug=True)
