// Initialize map
var map = L.map('map').fitBounds([
    [22.741822, 86.0846172], // Southwest
    [22.8510411, 86.279883]  // Northeast
]);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Define custom icons
var userIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/128/149/149071.png',
    iconSize: [40, 40],
    iconAnchor: [20, 40]
});

var doctorIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/128/2966/2966327.png',
    iconSize: [40, 40],
    iconAnchor: [20, 40]
});

// Load doctor data from localStorage
var doctors = [];
let storedDoctors = localStorage.getItem("selectedDoctor"); // Correct key
console.log(storedDoctors)
if (storedDoctors) {
    try {
        let parsedDoctors = JSON.parse(storedDoctors);

        // Extract lat/lng from stored doctors
        doctors = parsedDoctors.map(doctor => ({
            name: doctor.doctorName,
            phone: doctor.phone,
            address: doctor.address,
            time: doctor.time,
            lat: doctor.coordinates.lat,  // Using stored lat/lng
            lng: doctor.coordinates.lng
        }));

        // Add markers
        addDoctorMarkers();

    } catch (error) {
        console.error("Error parsing doctor data from localStorage:", error);
    }
} else {
    // Default sample doctors if no data found
    doctors = [
        { name: "Dr. A", phone: "1234567890", lat: 22.780, lng: 86.150 },
        { name: "Dr. B", phone: "9876543210", lat: 22.800, lng: 86.200 },
        { name: "Dr. C", phone: "9998887776", lat: 22.830, lng: 86.250 }
    ];
    addDoctorMarkers();
}


// Function to add markers for doctors
function addDoctorMarkers() {
    doctors.forEach(doctor => {
        L.marker([doctor.lat, doctor.lng], { icon: doctorIcon })
            .addTo(map)
            .bindPopup(`<b>${doctor.name}</b><br>Phone: ${doctor.phone}<br>Time: ${doctor.time}<br>
                        <button onclick="routeToDoctor(${doctor.lat}, ${doctor.lng})" >Get Route</button>`);
    });
}




// User's location marker
var userMarker;
var userCoords;

// Track User's Location in Real-Time
if (navigator.geolocation) {
    navigator.geolocation.watchPosition(position => {
        userCoords = [position.coords.latitude, position.coords.longitude];

        // If user marker doesn't exist, create it
        if (!userMarker) {
            userMarker = L.marker(userCoords, { icon: userIcon })
                .addTo(map)
                .bindPopup("<b>You are here</b>")
                .openPopup();
        } else {
            // Update marker position
            userMarker.setLatLng(userCoords);
        }

        // Optionally keep map centered on user
        map.setView(userCoords, 14);

    }, error => {
        console.log("Geolocation failed: ", error);
    }, {
        enableHighAccuracy: true,
        maximumAge: 1000,
        timeout: 10000
    });
} else {
    alert("Geolocation is not supported by this browser.");
}

// Routing function
var routeControl;
function routeToDoctor(lat, lng) {
    if (!userCoords) {
        alert("Your location is not available!");
        return;
    }

    // Remove existing route if present
    if (routeControl) {
        map.removeControl(routeControl);
    }

    // Add new route
    routeControl = L.Routing.control({
        waypoints: [
            L.latLng(userCoords[0], userCoords[1]),  // User's location
            L.latLng(lat, lng)  // Doctor's location
        ],
        routeWhileDragging: true
    }).addTo(map);
}
