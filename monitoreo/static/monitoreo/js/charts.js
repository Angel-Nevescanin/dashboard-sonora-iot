fetch("/api/datos/")
  .then(response => response.json())
  .then(data => {
    console.log("Datos recibidos:", data);

    const municipios = Object.keys(data);
    const temperaturas = municipios.map(m =>
      data[m].temperatura ?? null
    );

    const ctx = document.getElementById("tempChart");

    if (!ctx) {
      console.error("No se encontró el canvas");
      return;
    }

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: municipios,
        datasets: [{
          label: "Temperatura (°C)",
          data: temperaturas,
        }]
      },
      options: {
        responsive: true
      }
    });
  })
  .catch(err => {
    console.error("Error conectando a API", err);
  });
