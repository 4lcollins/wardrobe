const setLocation = function() {
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
};

if (window.Shiny) {
  setLocation();
} else {
  $(document).one('shiny:connected', setLocation);
}
