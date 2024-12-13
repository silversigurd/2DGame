const player = document.getElementById('player');
const gameContainer = document.getElementById('game-container');

let isJumping = false;
let positionX = 50; // Posición inicial en el eje X
let positionY = 50; // Posición inicial en el eje Y
let gravity = 0; // Gravedad para el salto

document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
        positionX += 10; // Mover a la derecha
        player.style.left = positionX + 'px';
    } else if (event.key === 'ArrowLeft') {
        positionX -= 10; // Mover a la izquierda
        player.style.left = positionX + 'px';
    } else if (event.key === ' ') {
        if (!isJumping) {
            jump();
        }
    }
});

function jump() {
    isJumping = true;
    gravity = 0;

    const jumpInterval = setInterval(() => {
        if (gravity < 15) {
            gravity += 1; // Aumentar la gravedad
            positionY += gravity; // Mover hacia arriba
            player.style.bottom = positionY + 'px'; // Actualizar la posición Y
        } else {
            clearInterval(jumpInterval);
            const fallInterval = setInterval(() => {
                if (positionY > 50) {
                    gravity -= 1; // Disminuir la gravedad
                    positionY -= gravity; // Mover hacia abajo
                    player.style.bottom = positionY + 'px'; // Actualizar la posición Y
                } else {
                    clearInterval(fallInterval);
                    isJumping = false; // Permitir otro salto
                    positionY = 50; // Restablecer la posición
                    player.style.bottom = positionY + 'px'; // Asegurarse de que esté en la posición correcta
                }
            }, 20);
        }
    }, 20);
}