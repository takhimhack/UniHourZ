function loadpage() {
    ajaxGetRequest('/queuedata', process_queue_data);
    setTimeout(loadpage, 5000);
}
loadpage();

function process_queue_data(queue_response) {
    let decoded = JSON.parse(queue_response);
    console.log(decoded);
    for (var key in decoded) {
        for (let i = 1; i < 11; i++){
            if (i > decoded[key].length) {
                document.getElementById(key.toString() + "q" + i.toString()).innerHTML = "";
            } else {
                document.getElementById(key.toString() + "q" + i.toString()).innerHTML = decoded[key]["queue"][i-1]["name"];
            }
        }
    }
}

function ajaxGetRequest(path, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
          callback(this.response);
        }
    };
    request.open("GET", path);
    request.send();
}