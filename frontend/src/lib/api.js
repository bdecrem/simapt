const BASE = '';

function getToken() {
  return localStorage.getItem('bramble_token');
}

function setToken(token) {
  localStorage.setItem('bramble_token', token);
}

export function hasGame() {
  return !!getToken();
}

export function clearGame() {
  localStorage.removeItem('bramble_token');
}

async function request(path, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) {
    headers['X-Game-Token'] = token;
  }
  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export async function newGame() {
  const result = await request('/game/new', 'POST');
  if (result.token) {
    setToken(result.token);
  }
  return result;
}

export async function getState() {
  return request('/game/state');
}

export async function advanceDay() {
  return request('/game/advance', 'POST');
}

export async function makeChoice(choiceId) {
  return request('/scenario/choose', 'POST', { choice_id: choiceId });
}

export async function fixTask(taskId) {
  return request('/game/fix-task', 'POST', { task_id: taskId });
}
