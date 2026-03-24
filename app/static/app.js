const API = "/api";

// ── State ──
let currentListId = null;
let currentListName = "";

// ── DOM refs ──
const listsView = document.getElementById("lists-view");
const tasksView = document.getElementById("tasks-view");
const listItems = document.getElementById("list-items");
const taskItems = document.getElementById("task-items");
const newListInput = document.getElementById("new-list-name");
const newTaskInput = document.getElementById("new-task-title");
const tasksTitle = document.getElementById("tasks-title");

// ── Navigation ──
function showLists() {
  currentListId = null;
  listsView.hidden = false;
  tasksView.hidden = true;
  loadLists();
}

function showTasks(listId, listName) {
  currentListId = listId;
  currentListName = listName;
  tasksTitle.textContent = listName;
  listsView.hidden = true;
  tasksView.hidden = false;
  loadTasks();
}

// ── Lists ──
async function loadLists() {
  const res = await fetch(`${API}/lists`);
  const lists = await res.json();
  listItems.innerHTML = "";
  if (lists.length === 0) {
    listItems.innerHTML = '<li class="empty">No lists yet. Create one above!</li>';
    return;
  }
  for (const l of lists) {
    const li = document.createElement("li");

    const label = document.createElement("span");
    label.className = "label";
    label.textContent = l.name;
    label.addEventListener("click", () => showTasks(l.id, l.name));

    const del = document.createElement("button");
    del.className = "btn btn-danger btn-sm";
    del.textContent = "Delete";
    del.addEventListener("click", () => deleteList(l.id));

    li.append(label, del);
    listItems.appendChild(li);
  }
}

async function addList() {
  const name = newListInput.value.trim();
  if (!name) return;
  await fetch(`${API}/lists`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  newListInput.value = "";
  loadLists();
}

async function deleteList(id) {
  await fetch(`${API}/lists/${id}`, { method: "DELETE" });
  loadLists();
}

// ── Tasks ──
async function loadTasks() {
  const res = await fetch(`${API}/lists/${currentListId}/tasks`);
  const tasks = await res.json();
  taskItems.innerHTML = "";
  if (tasks.length === 0) {
    taskItems.innerHTML = '<li class="empty">No tasks yet. Add one above!</li>';
    return;
  }
  for (const t of tasks) {
    const li = document.createElement("li");

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = t.completed;
    cb.addEventListener("change", () => toggleTask(t.id, cb.checked));

    const label = document.createElement("span");
    label.className = "label" + (t.completed ? " completed" : "");
    label.textContent = t.title;

    const del = document.createElement("button");
    del.className = "btn btn-danger btn-sm";
    del.textContent = "Delete";
    del.addEventListener("click", () => deleteTask(t.id));

    li.append(cb, label, del);
    taskItems.appendChild(li);
  }
}

async function addTask() {
  const title = newTaskInput.value.trim();
  if (!title) return;
  await fetch(`${API}/lists/${currentListId}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  newTaskInput.value = "";
  loadTasks();
}

async function toggleTask(taskId, completed) {
  await fetch(`${API}/lists/${currentListId}/tasks/${taskId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  loadTasks();
}

async function deleteTask(taskId) {
  await fetch(`${API}/lists/${currentListId}/tasks/${taskId}`, {
    method: "DELETE",
  });
  loadTasks();
}

// ── Event listeners ──
document.getElementById("add-list-form").addEventListener("submit", (e) => {
  e.preventDefault();
  addList();
});

document.getElementById("add-task-form").addEventListener("submit", (e) => {
  e.preventDefault();
  addTask();
});

document.getElementById("back-to-lists").addEventListener("click", (e) => {
  e.preventDefault();
  showLists();
});

// Handle Enter key in inputs
newListInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") { e.preventDefault(); addList(); }
});
newTaskInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") { e.preventDefault(); addTask(); }
});

// ── Init ──
showLists();
