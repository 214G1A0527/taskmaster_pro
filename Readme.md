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
