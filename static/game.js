// Obtener el contexto del canvas
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Ajustar el tamaño del canvas para que ocupe toda la ventana
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Propiedades del círculo
let x = canvas.width / 2;
let y = canvas.height / 2;
let radius = 30;
let dx = 4;
let dy = 4;

// Función para dibujar el círculo
function drawCircle() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Limpiar el canvas antes de redibujar
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2); // Dibuja el círculo
    ctx.fillStyle = "blue"; // Color del círculo
    ctx.fill();
    ctx.closePath();
}

// Función para actualizar la posición del círculo y manejar la animación
function updateGame() {
    drawCircle(); // Redibuja el círculo

    // Actualizar la posición del círculo
    x += dx;
    y += dy;

    // Colisiones con los bordes
    if (x + radius > canvas.width || x - radius < 0) {
        dx = -dx; // Rebotar en el eje X
    }
    if (y + radius > canvas.height || y - radius < 0) {
        dy = -dy; // Rebotar en el eje Y
    }

    // Llamar a la función de animación continuamente
    requestAnimationFrame(updateGame);
}

// Iniciar la animación
updateGame();
