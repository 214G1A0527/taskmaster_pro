# To-Do List App

## Overview
This To-Do List App is a task management application built using Python's Tkinter library. The app allows users to create, edit, delete, and track tasks, with additional features such as notifications for tasks due soon, priority management, and dark mode. It saves tasks to a JSON file and loads them when the app is reopened.

## Features

- **Add Tasks**: Create new tasks by specifying a name, due date, due time, priority (High, Medium, Low), creator, assignee, and description.
  
- **Edit Tasks**: Modify existing tasks by updating their details.
  
- **Remove Tasks**: Delete tasks from the list.
  
- **Complete Tasks**: Mark tasks as completed.

- **Search Tasks**: Search for tasks by their name using the search bar.

- **Task Priority and Status**: Tasks can have a priority and completion status, displayed with color codes for easy identification:
    - Completed tasks are shown in green.
    - Overdue tasks appear in red.
    - Tasks due on the same day are yellow.
    - Tasks with a high priority are pink.

- **Notifications**: The app provides reminders for tasks that are due within 30 minutes, using a pop-up notification.

- **Dark Mode**: Users can toggle between light and dark modes.

- **Data Persistence**: All tasks are saved in a `tasks.json` file, ensuring tasks are loaded upon reopening the app.

## Installation

### Prerequisites
- Python 3.x
- Tkinter (usually included with Python installations)
- `json` (standard library module)
- `threading`, `time`, `datetime` (standard library modules)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/todo-list-app.git
2. Navigate to the project folder:
   ```bash
   cd todo-list-app
3. Run the application:
   ```bash
   python main.py

## How to Use

1. **Adding Tasks**: Click the "Add Task" button and fill in the task's name, due date, time, priority, creator, assignee, and description. Click "OK" to save the task.

2. **Editing Tasks**: Select a task by clicking on it, then click "Edit Task" to modify its details.

3. **Removing Tasks**: Select a task and click "Remove Task" to delete it.

4. **Marking Tasks as Completed**: Select a task and click "Mark Completed" to mark it as finished.

5. **Searching Tasks**: Type in the search bar to filter tasks by name.

6. **Notifications**: The app will notify you 30 minutes before a task is due.

## File Structure
   ```bash
    .
    ├── main.py        # Main application file
    ├── tasks.json     # File where tasks are saved
    └── README.md      # Project README file
   ```
## Future Improvements
- Add support for recurring tasks.
- Implement more advanced notification options.
- Allow task categorization and sorting by priority or due date.
  
## License
- This project is licensed under the MIT License.

Feel free to contribute by opening issues or submitting pull requests!




  
  
   
