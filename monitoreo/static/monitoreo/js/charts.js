async function fetchAndRender() {
  try {
    const response = await fetch("/api/datos/");
    const data = await response.json();

    console.log("Datos recibidos:", data);

    // ✅ Convertimos el objeto en arrays
    const municipios = [];
    const temperaturas = [];
    const humedades = [];

    Object.entries(data).forEach(([municipio, valores]) => {
      municipios.push(municipio);
      temperaturas.push(valores.temperatura ?? null);
      humedades.push(valores.humedad ?? null);
    });

    const canvas = document.getElementById("tempChart");
    if (!canvas) {
      console.error("No se encontró el canvas");
      return;
    }

    // ✅ Evitar múltiples gráficas encima
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
          },
          {
            label: "Humedad (%)",
            data: humedades,
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

// ✅ Ejecutar al cargar la página
fetchAndRender();

// ✅ AUTO REFRESH cada 5 segundos
setInterval(fetchAndRender, 5000);