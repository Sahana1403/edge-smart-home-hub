async function fetchDevices(){
  const r = await fetch('/api/devices');
  const devices = await r.json();
  const root = document.getElementById('devices');
  root.innerHTML = '<h2>Devices</h2>' + devices.map(d => `<div class="dev"><b>${d.friendly_name||d.id}</b> <small>${d.type}</small></div>`).join('');
}

window.onload = () => {
  fetchDevices();
  setInterval(fetchDevices, 5000);
}
