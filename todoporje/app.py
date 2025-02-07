from flask import Flask, render_template, request, redirect, url_for  # type: ignore

# Create an instance of the Flask class. The app will use the 'templates' folder for HTML files.
app = Flask(__name__, template_folder='templates')

# A list to store to-do items. Each item is a dictionary with a 'task' and a 'completed' flag.
todos = []

# Route for the homepage. It will render the 'index.html' template and pass the 'todos' list to the template.
@app.route('/')
def index():
    # Render the main page with the current list of todos
    return render_template('todo.html', todos=todos)

# Route to add a new to-do item. It listens for POST requests when a new to-do is submitted.
@app.route('/add', methods=['POST'])
def add():
    # Get the 'todo' data from the form
    todo = request.form['todo']
    # Add the new task to the 'todos' list with a 'completed' status set to False
    todos.append({'task': todo, 'completed': False})
    # After adding the task, redirect the user back to the main page ('index')
    return redirect(url_for('index'))

# Route to edit an existing to-do item. It supports both GET (to display) and POST (to update) requests.
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    # Get the to-do item that corresponds to the given 'index'
    todo = todos[index]
    
    # If the request is a POST (when the form is submitted for editing)
    if request.method == 'POST':
        # Update the task with the new value from the form
        todo['task'] = request.form['todo']
        # After editing the task, redirect the user back to the main page ('index')
        return redirect(url_for('index'))
    else:
        # If it's a GET request, render the 'edit.html' template and pass the current todo and its index
        return render_template('edit.html', todo=todo, index=index)

# Route to check/uncheck a to-do item, which toggles the 'completed' flag (True/False).
@app.route('/check/<int:index>')
def check(index):
    # Toggle the 'completed' status of the to-do item
    todos[index]['completed'] = not todos[index]['completed']
    # After toggling, redirect the user back to the main page ('index')
    return redirect(url_for('index'))

# Route to delete a to-do item from the list based on its index.
@app.route('/delete/<int:index>')
def delete(index):
    # Remove the to-do item at the specified index from the 'todos' list
    del todos[index]
    # After deleting the task, redirect the user back to the main page ('index')
    return redirect(url_for('index'))

# Check if this script is being executed directly (not imported as a module).
# If true, start the Flask application with debugging enabled.
if __name__ == '__main__':
    app.run(debug=True)
