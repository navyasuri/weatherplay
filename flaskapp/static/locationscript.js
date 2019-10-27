console.log("locationscript loaded")
navigator.geolocation.getCurrentPosition(response => {
    const lat = response.coords.latitude
    const lon = response.coords.longitude
    const params = new URLSearchParams({
        lat: lat, lon: lon
    })
    window.location.replace("/location?"+params.toString())
}, error => {
    console.log("error with geolocation")
})