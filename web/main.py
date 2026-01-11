from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os
from datetime import datetime
from typing import Optional

app = FastAPI()

# Templates directory
templates = Jinja2Templates(directory="web/templates")

# File to store tasks
TASKS_FILE = 'todos.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    tasks = load_tasks()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add")
async def add_task(title: str = Form(...), description: str = Form("")):
    tasks = load_tasks()
    new_task = {
        'id': max([t['id'] for t in tasks], default=0) + 1,
        'title': title,
        'description': description,
        'status': 'incomplete',
        'created_at': datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return {"message": "Task added successfully"}

@app.put("/toggle/{task_id}")
async def toggle_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'complete' if task['status'] == 'incomplete' else 'incomplete'
            break
    save_tasks(tasks)
    return {"message": "Task toggled successfully"}

@app.delete("/delete/{task_id}")
async def delete_task(task_id: int):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return {"message": "Task deleted successfully"}

@app.get("/api/tasks")
async def api_tasks():
    tasks = load_tasks()
    return tasks

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))