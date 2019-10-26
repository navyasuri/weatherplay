$( document ).ready(function() {

    console.log("Script loaded")

    const baseURL = 'http://localhost:5000/';

    function spotify_redirect(){
        let url = "https://accounts.spotify.com/authorize?client_id=aaaf8139c94f404690029d989a13f529&response_type=code&redirect_uri=http%3A%2F%2localhost:5000&scope=user-read-private%20user-read-email"
        window.location.replace(url)
    }

    function sendGeolocationData(data) {
        $.post(
            baseURL + 'getLocation',
            { payload: data },
            function (data) {
                console.log(data);
            }
        );
    }

    function getGeolocationData() {
        navigator.geolocation.getCurrentPosition(response => {
            // response.coords.latitude
            // response.coords.longitude
            const gpsData = {
                lat: response.coords.latitude,
                lon: response.coords.longitude
            }
            sendGeolocationData(gpsData);
        }, error => {
            console.error("Error getting geolocation data.")
        })
    }

    getGeolocationData();
})