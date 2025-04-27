const facilityData = {
    revenue: 1200,
    usageRequests: 15,
    payments: 12,
    rentersPerMonth: [5, 8, 6, 12, 9, 15, 18, 13, 14, 10, 7, 11],//arbituary 
    monthlyRevenue: [50, 70, 90, 110, 95, 85, 100, 130, 115, 105, 80, 70] // adding to 1200
};

let chart; // global variable to store the chart instance

function showData(type) {
    const ctx = document.getElementById('infoChart').getContext('2d');

    // Destroy old chart if exists
    if (chart) {
        chart.destroy();
    }

    if (type === 'revenue') {
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ],
                datasets: [{
                    label: 'Revenue per Month ($)',
                    data: facilityData.monthlyRevenue,
                    backgroundColor: '#4a90e2'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: 18
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            font: {
                                size: 16
                            }
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                size: 16
                            }
                        }
                    }
                }
            }
        });
    
    } else if (type === 'usage') {
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ],
                datasets: [{
                    label: 'Renters per Month',
                    data: facilityData.rentersPerMonth,
                    borderColor: '#4a90e2',
                    backgroundColor: '#4a90e2',
                    fill: false,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } else if (type === 'payments') {
        chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Paid', 'Unpaid'],
                datasets: [{
                    label: 'Payments',
                    data: [facilityData.payments, 20 - facilityData.payments], // fake total 20
                    backgroundColor: ['#4a90e2', '#d1d1d1']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
}

function goHome() {
    window.location.href = "../index.html";
}