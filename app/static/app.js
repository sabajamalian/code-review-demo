const API = "/api";

// ── State ──
let currentListId = null;
let currentListName = "";
let lists = [];

// ── DOM refs ──
const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebar-overlay");
const sidebarToggle = document.getElementById("sidebar-toggle");
const listItems = document.getElementById("list-items");
const newListInput = document.getElementById("new-list-name");
const mainContent = document.getElementById("main-content");
const welcomeState = document.getElementById("welcome-state");
const tasksView = document.getElementById("tasks-view");
const tasksTitle = document.getElementById("tasks-title");
const taskItems = document.getElementById("task-items");
const newTaskInput = document.getElementById("new-task-title");

// Rename modal
const renameModal = document.getElementById("rename-modal");
const renameInput = document.getElementById("rename-list-input");
const renameForm = document.getElementById("rename-list-form");
const renameCancel = document.getElementById("rename-cancel");

// ── Sidebar toggle (mobile) ──
function openSidebar() {
  sidebar.classList.add("open");
  sidebarOverlay.classList.add("active");
}

function closeSidebar() {
  sidebar.classList.remove("open");
  sidebarOverlay.classList.remove("active");
}

sidebarToggle.addEventListener("click", () => {
  sidebar.classList.contains("open") ? closeSidebar() : openSidebar();
});
sidebarOverlay.addEventListener("click", closeSidebar);

// ── Lists ──
async function loadLists() {
  const res = await fetch(`${API}/lists`);
  lists = await res.json();
  renderListNav();
}

function renderListNav() {
  listItems.innerHTML = "";
  if (lists.length === 0) {
    listItems.innerHTML = '<li class="empty">No lists yet</li>';
    return;
  }
  for (const l of lists) {
    const li = document.createElement("li");
    if (l.id === currentListId) li.classList.add("active");

    const label = document.createElement("span");
    label.className = "nav-label";
    label.textContent = l.name;

    const count = document.createElement("span");
    count.className = "nav-count";
    count.textContent = l.task_count ?? "";

    li.append(label, count);
    li.addEventListener("click", () => selectList(l.id, l.name));
    listItems.appendChild(li);
  }
}

function selectList(id, name) {
  currentListId = id;
  currentListName = name;
  tasksTitle.textContent = name;
  welcomeState.hidden = true;
  tasksView.hidden = false;
  renderListNav();
  loadTasks();
  closeSidebar(); // auto-close on mobile
}

async function addList() {
  const name = newListInput.value.trim();
  if (!name) return;
  const res = await fetch(`${API}/lists`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  const created = await res.json();
  newListInput.value = "";
  await loadLists();
  selectList(created.id, created.name);
}

async function deleteList(id) {
  if (!confirm("Delete this list and all its tasks?")) return;
  await fetch(`${API}/lists/${encodeURIComponent(id)}`, { method: "DELETE" });
  if (currentListId === id) {
    currentListId = null;
    currentListName = "";
    tasksView.hidden = true;
    welcomeState.hidden = false;
  }
  await loadLists();
}

async function renameList(id, newName) {
  await fetch(`${API}/lists/${encodeURIComponent(id)}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: newName }),
  });
  if (currentListId === id) {
    currentListName = newName;
    tasksTitle.textContent = newName;
  }
  await loadLists();
}

// ── Rename modal ──
document.getElementById("edit-list-btn").addEventListener("click", () => {
  if (!currentListId) return;
  renameInput.value = currentListName;
  renameModal.hidden = false;
  renameInput.focus();
  renameInput.select();
});

renameCancel.addEventListener("click", () => { renameModal.hidden = true; });

renameModal.addEventListener("click", (e) => {
  if (e.target === renameModal) renameModal.hidden = true;
});

renameForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const newName = renameInput.value.trim();
  if (!newName || !currentListId) return;
  renameModal.hidden = true;
  await renameList(currentListId, newName);
});

// ── Delete list button ──
document.getElementById("delete-list-btn").addEventListener("click", () => {
  if (currentListId) deleteList(currentListId);
});

// ── Tasks ──
async function loadTasks() {
  const res = await fetch(`${API}/lists/${encodeURIComponent(currentListId)}/tasks`);
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
    del.className = "icon-btn danger task-delete-btn";
    del.setAttribute("aria-label", "Delete task");
    del.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/></svg>';
    del.addEventListener("click", () => deleteTask(t.id));

    li.append(cb, label, del);
    taskItems.appendChild(li);
  }
}

async function addTask() {
  const title = newTaskInput.value.trim();
  if (!title) return;
  await fetch(`${API}/lists/${encodeURIComponent(currentListId)}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  newTaskInput.value = "";
  loadTasks();
  loadLists(); // refresh task counts
}

async function toggleTask(taskId, completed) {
  await fetch(`${API}/lists/${encodeURIComponent(currentListId)}/tasks/${encodeURIComponent(taskId)}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  loadTasks();
}

async function deleteTask(taskId) {
  await fetch(`${API}/lists/${encodeURIComponent(currentListId)}/tasks/${encodeURIComponent(taskId)}`, {
    method: "DELETE",
  });
  loadTasks();
  loadLists(); // refresh task counts
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

// ── Init ──
loadLists();
