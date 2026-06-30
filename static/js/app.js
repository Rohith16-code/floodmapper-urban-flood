/** Frontend application logic for the Urban Flood Inundation Mapping dashboard. */
const API_BASE = '/api/v1';

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return response;
}

async function loadSystemHealth() {
  const el = document.getElementById('health');
  try {
    const data = await fetchJson(`${API_BASE}/health`);
    el.innerHTML = `<p class="status-ok">Status: ${data.status}</p>`;
  } catch (err) {
    el.innerHTML = `<p class="status-error">Error: ${err.message}</p>`;
  }
}

async function loadFloodData() {
  const el = document.getElementById('flood-data');
  try {
    const prediction = await postJson(`${API_BASE}/flood/predict`, {
      location_id: 'demo_location',
      timestamp: new Date().toISOString(),
      rainfall_mm: 35.0,
      water_level_cm: 110.0,
    });
    const predData = await prediction.json();
    el.innerHTML = `
      <p>Risk level: <strong>${predData.risk_level}</strong></p>
      <p>Inundation depth: ${predData.inundation_depth_cm} cm</p>
    `;
  } catch (err) {
    el.innerHTML = `<p class="status-error">Error: ${err.message}</p>`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadSystemHealth();
  loadFloodData();
});
