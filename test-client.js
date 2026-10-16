// test-client.js
const IP = '3.135.214.137';
const PORT = 6061; // Cambia esto si tu servidor usa otro puerto, ej: 3000

async function probarConexion() {
    try {
        console.log(`Intentando conectar a http://${IP}:${PORT}...`);
        
        const response = await fetch(`http://${IP}:${PORT}`);
        const data = await response.text();
        
        console.log('¡Conexión exitosa!');
        console.log('Respuesta del servidor:', data);
    } catch (error) {
        console.error('Error de conexión:', error.message);
    }
}

probarConexion();