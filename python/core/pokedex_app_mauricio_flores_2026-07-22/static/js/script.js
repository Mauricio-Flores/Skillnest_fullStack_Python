document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".tarjeta-imagen img").forEach((img) => {
        img.addEventListener("error", () => {
            img.style.display = "none";
            const aviso = document.createElement("div");
            aviso.className = "imagen-no-disponible";
            aviso.textContent = "Sin imagen";
            img.parentElement.appendChild(aviso);
        });
    });

    document.querySelectorAll(".poder-relleno").forEach((barra) => {
        const anchoFinal = barra.style.width;
        barra.style.width = "0%";
        requestAnimationFrame(() => {
            setTimeout(() => {
                barra.style.width = anchoFinal;
            }, 100);
        });
    });
});