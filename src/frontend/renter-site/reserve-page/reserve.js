// Get facility from URL query params
const urlParams = new URLSearchParams(window.location.search);
const facilityName = urlParams.get('facility');

if (facilityName) {
  document.getElementById('facility').value = facilityName;
}

// Handle form submission
document.getElementById('reservationForm').addEventListener('submit', async function(e) {
  e.preventDefault();

const urlParams = new URLSearchParams(window.location.search);
const facilityName = urlParams.get('facility');

if (facilityName) {
  document.getElementById('facility').value = facilityName;
}


  const data = {
    facility: document.getElementById('facility').value,
    event_type: document.getElementById('event_type').value,
    attendees: parseInt(document.getElementById('attendees').value),
    date: document.getElementById('date').value,
    time_start: document.getElementById('time_start').value,
    time_end: document.getElementById('time_end').value
  };

  try {
    const response = await fetch('http://127.0.0.1:5000/reserve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById('responseMessage').innerText = result.message;
  } catch (error) {
    document.getElementById('responseMessage').innerText = 'Error connecting to server.';
  }
});

document.getElementById('reservationForm').addEventListener('submit', function(e) {
  e.preventDefault();

  // Collect data (for the payment breakdown if needed)
  const facility = document.getElementById('facility').value || 'Facility';
  const attendees = document.getElementById('attendees').value || 0;

  // Redirect to payment page with query parameters
  window.location.href = `../payment-page/payment.html?facility=${encodeURIComponent(facility)}&attendees=${attendees}`;
});
