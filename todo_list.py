import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize session state for tasks if not already initialized
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

# Function to add a task
def add_task(task, priority, due_date):
    st.session_state['tasks'].append({"Task": task, "Priority": priority, "Due Date": due_date, "Completed": False})

# Function to remove a task
def remove_task(index):
    del st.session_state['tasks'][index]

# Function to mark a task as completed
def complete_task(index):
    st.session_state['tasks'][index]['Completed'] = True

# Function to edit a task
def edit_task(index, task, priority, due_date):
    st.session_state['tasks'][index] = {"Task": task, "Priority": priority, "Due Date": due_date, "Completed": False}

# Title of the app
st.title('To-Do List and Reminder')

# Input fields for adding a new task
with st.form("add_task_form"):
    task = st.text_input("Task")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("Due Date")
    add_task_button = st.form_submit_button("Add Task")

# Add task when the form is submitted
if add_task_button and task:
    add_task(task, priority, due_date)
    st.success("Task added successfully")

# Display the tasks
st.subheader("Tasks")
tasks_df = pd.DataFrame(st.session_state['tasks'])
if not tasks_df.empty:
    st.table(tasks_df)

    # Options to edit or remove tasks
    for i, task in enumerate(st.session_state['tasks']):
        st.write(f"Task {i+1}: {task['Task']}")
        if st.button(f"Remove Task {i+1}"):
            remove_task(i)
            st.experimental_rerun()
        if st.button(f"Complete Task {i+1}"):
            complete_task(i)
            st.experimental_rerun()
        with st.expander(f"Edit Task {i+1}"):
            new_task = st.text_input("Task", task['Task'], key=f"edit_task_{i}")
            new_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(task['Priority']), key=f"edit_priority_{i}")
            new_due_date = st.date_input("Due Date", task['Due Date'], key=f"edit_due_date_{i}")
            if st.button(f"Save Task {i+1}"):
                edit_task(i, new_task, new_priority, new_due_date)
                st.experimental_rerun()

# Reminders for tasks due soon
st.subheader("Reminders")
reminders = []
for task in st.session_state['tasks']:
    if not task['Completed'] and task['Due Date'] <= datetime.today().date() + timedelta(days=1):
        reminders.append(task)

if reminders:
    st.write("Tasks due soon:")
    for task in reminders:
        st.write(f"Task: {task['Task']}, Due Date: {task['Due Date']}, Priority: {task['Priority']}")
else:
    st.write("No tasks due soon.")

# Optionally, you can add synchronization with a calendar using an API like Google Calendar API.
# This part is optional and would require additional setup and API credentials.