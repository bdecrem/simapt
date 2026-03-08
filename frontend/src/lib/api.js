const BASE = 'http://localhost:8000';

async function request(path, method = 'GET', body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export async function newGame() {
  return request('/game/new', 'POST');
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
