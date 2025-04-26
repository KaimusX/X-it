function loadFacilityData() {
    const facilityData = {
        name: "Main Gym",
        image: "facility-images/gym.jpg",
        revenue: 1200,
        usageRequests: 15,
        payments: 12
    };

    document.getElementById('facility-name').textContent = facilityData.name;
    document.getElementById('facility-image').src = facilityData.image;
    document.getElementById('revenue').textContent = `$${facilityData.revenue}`;
    document.getElementById('usage-requests').textContent = facilityData.usageRequests;
    document.getElementById('payments').textContent = facilityData.payments;
}

function goHome() {
    // Remember: dashboard.html is inside /staff-site/facility-dashboard/
    // To go back to /staff-site/index.html we need to go up one level ("../")
    window.location.href = "../index.html";
}

window.onload = loadFacilityData;