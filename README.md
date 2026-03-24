# code-review-demo

Showcasing agentic Code Reviews with GitHub Copilot

## To-Do List API

A Flask REST API for managing multiple to-do lists and their tasks, backed by SQLite.

### Setup

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Initialize the database
flask --app run:app db init
flask --app run:app db migrate -m "initial"
flask --app run:app db upgrade

# Run the dev server
python run.py
```

The API is available at `http://localhost:5000`.

### API Endpoints

#### Lists

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/lists | List all to-do lists |
| POST | /api/lists | Create a new list |
| GET | /api/lists/:id | Get a single list |
| PUT | /api/lists/:id | Update a list |
| DELETE | /api/lists/:id | Delete a list and its tasks |

#### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/lists/:id/tasks | List tasks in a list |
| POST | /api/lists/:id/tasks | Create a task |
| GET | /api/lists/:id/tasks/:task_id | Get a single task |
| PUT | /api/lists/:id/tasks/:task_id | Update a task |
| DELETE | /api/lists/:id/tasks/:task_id | Delete a task |

### Examples

```bash
# Create a list
curl -X POST http://localhost:5000/api/lists \
  -H "Content-Type: application/json" \
  -d '{"name": "Groceries"}'

# Add a task
curl -X POST http://localhost:5000/api/lists/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk", "description": "2% milk"}'

# Mark a task complete
curl -X PUT http://localhost:5000/api/lists/1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# List all tasks in a list
curl http://localhost:5000/api/lists/1/tasks
```

### Running Tests

```bash
pytest tests/ -v
```
