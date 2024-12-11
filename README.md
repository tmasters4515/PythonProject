# Python Project
ToDo Manager

# Overview

A simple Python app to manage tasks using a SQLite database

# Features
- Add tasks with optional due dates
- View all tasks or only overdue ones
- Mark tasks as complete
- Delete Tasks
- Help message

# Usage 
# Programmatic Usage
- Add a task
insert_todo("Buy Groceries", "2024-12-15")
- View all tasks
get_all_todos()
- Mark a task as complete
mark_todo_complete(1)
- Delete a Task
delete_todo(1) 
# Command-Line Usage
- Show help message
python Pyproject.py -h
- Add a task
python Pyproject.py -a "Buy Groceries" -d 2024-12-31
- List all tasks
python Pyproject.py -l
- List overdue tasks
python Pyproject.py -o
- Mark a task as complete
python Pyproject.py -c 1
- Delete a task
python Pyproject.py -r 1
# Command-Line Options
- -h, --help: Show Help Message
- -a, --add: Add new todo
- -d, --due: Specify due date
- -l, --list: List all todos
- -o, --overdue: List overdue todos
- -c, --complete: Mark a todo as complete
- -r, --remove: Remove a todo by ID

# Dependencies
- Python 3.x
- SQLite
