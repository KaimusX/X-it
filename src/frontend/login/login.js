// Auto-select role from URL
const urlParams = new URLSearchParams(window.location.search);
const roleParam = urlParams.get('role');

if (roleParam) {
  document.getElementById('role').value = roleParam;
}

document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const role = document.getElementById('role').value;

  const data = { username, password, role };

  try {
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    
    if (result.success) {
      // Redirect based on role
      if (role === 'renter') {
        window.location.href = 'renter_dashboard.html';
      } else {
        window.location.href = 'staff_dashboard.html';
      }
    } else {
      document.getElementById('loginResponse').innerText = 'Invalid credentials!';
    }
  } catch (error) {
    document.getElementById('loginResponse').innerText = 'Error connecting to server.';
  }
});
