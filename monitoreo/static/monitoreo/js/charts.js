async function fetchAndRender() {
  try {
    const response = await fetch("/api/datos/");
    const data = await response.json();

    console.log("Datos recibidos:", data);

    const municipios = [];
    const temperaturas = [];
    const humedades = [];
    const uvIndex = [];
    const uvColors = [];

    Object.entries(data).forEach(([municipio, valores]) => {
      municipios.push(municipio);
      temperaturas.push(valores.temperatura ?? null);
      humedades.push(valores.humedad ?? null);

      const uv = valores.uv ?? null;
      uvIndex.push(uv);

      // 🚨 alerta visual UV
      if (uv !== null && uv >= 8) {
        uvColors.push("rgba(255, 0, 0, 0.8)"); // rojo riesgo
      } else {
        uvColors.push("rgba(255, 206, 86, 0.8)"); // amarillo normal
      }
    });

    const canvas = document.getElementById("tempChart");
    if (!canvas) return;

    if (window.chart) {
      window.chart.destroy();
    }

    window.chart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: municipios,
        datasets: [
          {
            label: "Temperatura (°C)",
            data: temperaturas,
            backgroundColor: "rgba(255, 99, 132, 0.7)"
          },
          {
            label: "Humedad (%)",
            data: humedades,
            backgroundColor: "rgba(54, 162, 235, 0.7)"
          },
          {
            label: "Índice UV",
            data: uvIndex,
            backgroundColor: uvColors
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });

  } catch (error) {
    console.error("Error conectando a API", error);
  }
}

// ▶️ Ejecutar al cargar
fetchAndRender();

// 🔁 Auto refresh
setInterval(fetchAndRender, 5000);
