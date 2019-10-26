console.log("Script loaded")

function spotify_redirect(){
    let url = "https://accounts.spotify.com/authorize?client_id=aaaf8139c94f404690029d989a13f529&response_type=code&redirect_uri=http%3A%2F%2localhost:5000&scope=user-read-private%20user-read-email"
    window.location.replace(url)
}