function loadpage() {
    let pdata = JSON.stringify({token: getCookie("authToken")});
    ajaxPostRequest('/queuedata', pdata, process_queue_data);
    setTimeout(loadpage, 10000);
}
loadpage();

function process_queue_data(queue_response) {
    let decoded = JSON.parse(queue_response);
    if (decoded.valid === 'valid'){
        for (var key in decoded.queues) {
            for (let i = 1; i < 11; i++){
                if (i > decoded[key].length) {
                    document.getElementById(key.toString() + "q" + i.toString()).innerHTML = "";
                } else {
                    document.getElementById(key.toString() + "q" + i.toString()).innerHTML = decoded[key]["queue"][i-1]["name"];
                }
            }
        }
    } else {
        window.location = "/index.html";
    }
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function ajaxPostRequest(path, data, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callback(this.response);
        }
    };
    request.open("POST", path);
    request.send(data);
}