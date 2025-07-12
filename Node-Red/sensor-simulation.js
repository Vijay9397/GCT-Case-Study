const now = new Date();
const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0');
const day = String(now.getDate()).padStart(2, '0');
const hour = String(now.getHours()).padStart(2, '0');
const minute = String(now.getMinutes()).padStart(2, '0');

const filename = `sensor_${hour}${minute}.json`;

// Create folder path
msg.localpath = `C:/Users/vijay/Desktop/GCT Project/raw/Year ${year}/Month ${month}/Day ${day}/${hour}/${filename}`;
msg.filename = `raw/${year}/${month}/${day}/${hour}/${filename}`;

msg.payload = JSON.stringify({
    timestamp: now.toISOString(),
    pH: (6 + Math.random() * 2).toFixed(2),
    conductivity: (100 + Math.random() * 50).toFixed(2),
    pressure: (1 + Math.random() * 5).toFixed(2),
    temperature: (20 + Math.random() * 15).toFixed(2),
    fillLevel: (Math.random() * 100).toFixed(2),
    flow: (10 + Math.random() * 5).toFixed(2),
    humidity: (30 + Math.random() * 20).toFixed(2),
    co2: (400 + Math.random() * 100).toFixed(2)
});

return msg;