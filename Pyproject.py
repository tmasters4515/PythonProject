import sqlite3
import re
import time
import sys
import argparse

conn = sqlite3.connect('todos.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY,
    task TEXT NOT NULL,
    due_date TEXT,
    completed INTEGER DEFAULT 0
)
''')
conn.commit()

def validate_date(date_string):
    date_pattern = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
    match = date_pattern.match(date_string)
    
    if not match:
        return False
    
    year, month, day = match.groups()
    
    try:
        if int(month) < 1 or int(month) > 12:
            return False
        
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if int(day) < 1 or int(day) > days_in_month[int(month)-1]:
            return False
        
        return True
    except ValueError:
        return False

def get_current_date():
    return time.strftime('%Y-%m-%d')

def insert_todo(task, due_date=None):
    if due_date and not validate_date(due_date):
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    cursor.execute("INSERT INTO todos (task, due_date) VALUES (?, ?)", (task, due_date))
    conn.commit()
    return cursor.lastrowid

def get_all_todos():
    cursor.execute("SELECT * FROM todos")
    return cursor.fetchall()

def get_overdue_todos():
    current_date = get_current_date()
    
    cursor.execute("SELECT * FROM todos WHERE completed = 0 AND due_date IS NOT NULL AND due_date < ? ORDER BY due_date", (current_date,))
    return cursor.fetchall()

def mark_todo_complete(todo_id):
    cursor.execute("UPDATE todos SET completed = 1 WHERE id = ?", (todo_id,))
    
    updated_rows = cursor.rowcount
    conn.commit()
    
    return updated_rows > 0

def delete_todo(todo_id):
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    deleted_rows = cursor.rowcount
    conn.commit()
    return deleted_rows > 0

def print_todos(todos):
    if not todos:
        print("No todos found.")
        return
    
    print("ID | Task | Due Date | Status")
    print("-" * 50)
    for todo in todos:
        status = "Completed" if todo[3] else "Pending"
        print(f"{todo[0]} | {todo[1]} | {todo[2] or 'No due date'} | {status}")

def main():
    parser = argparse.ArgumentParser(description="Simple Todo List Application")
    
    parser.add_argument('-a', '--add', nargs='+', help='Add a new todo. Use -a "Task description" [-d YYYY-MM-DD]')
    parser.add_argument('-d', '--due', help='Specify due date for the todo (YYYY-MM-DD)', default=None)
    parser.add_argument('-l', '--list', action='store_true', help='List all todos')
    parser.add_argument('-o', '--overdue', action='store_true', help='List overdue todos')
    parser.add_argument('-c', '--complete', type=int, help='Mark a todo as complete by ID')
    parser.add_argument('-r', '--remove', type=int, help='Remove a todo by ID')

    args = parser.parse_args()

    try:
        if args.add:
            task = ' '.join(args.add)
            todo_id = insert_todo(task, args.due)
            print(f"Todo added with ID {todo_id}")
        
        elif args.list:
            todos = get_all_todos()
            print_todos(todos)
        
        elif args.overdue:
            overdue_todos = get_overdue_todos()
            print_todos(overdue_todos)
        
        elif args.complete:
            if mark_todo_complete(args.complete):
                print(f"Todo {args.complete} marked as complete")
            else:
                print(f"No todo found with ID {args.complete}")
        
        elif args.remove:
            if delete_todo(args.remove):
                print(f"Todo {args.remove} deleted")
            else:
                print(f"No todo found with ID {args.remove}")
        
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()