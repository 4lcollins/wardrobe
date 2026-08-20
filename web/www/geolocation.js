$(document).on('shiny:connected', function(event) {
  Shiny.setInputValue('{{ input_id }}', null);

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        Shiny.setInputValue('{{ input_id }}', {
          lat: position.coords.latitude,
          lon: position.coords.longitude
        });
      },
      function(error) {
        console.warn('Geolocation denied or unavailable:', error.message);
        Shiny.setInputValue('{{ input_id }}', { error: error.message });
      },
      { timeout: 10000 }
    );
  } else {
    Shiny.setInputValue('{{ input_id }}', { error: "Geolocation not supported" });
  }
});