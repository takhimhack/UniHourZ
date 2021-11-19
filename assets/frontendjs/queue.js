function loadpage() {
    let pdata = JSON.stringify({token: getCookie("authToken")});
    ajaxPostRequest('/queuedata', pdata, process_queue_data);
    setTimeout(loadpage, 10000);
}
onload_func();
loadpage();

function onload_func() {
    let pdata = JSON.stringify({token: getCookie("authToken")});
    ajaxPostRequest('/checkstatus', pdata, html_setup);
}

function html_setup(setup_response) {
    let decoded = JSON.parse(setup_response);
    if (decoded.valid === 'valid'){
        let doms = document.getElementsByTagName('button');
        for (var k = 0; k < doms.length; k++) {
            if (doms[k].hasAttribute("studenthidden")) {
                doms[k].removeAttribute('hidden');
            }
        }
        doms = document.getElementsByTagName('a');
        for (var k = 0; k < doms.length; k++) {
            if (doms[k].hasAttribute("studenthidden")) {
                doms[k].removeAttribute('hidden');
            }
        }
    }
}

function process_queue_data(queue_response) {
    let decoded = JSON.parse(queue_response);
    if (decoded.valid === 'valid'){
        for (var key in decoded.queues) {
            for (let i = 1; i < 11; i++){
                if (i > decoded["queues"][key].length) {
                    document.getElementById(key.toString() + "q" + i.toString()).innerHTML = "";
                } else {
                    document.getElementById(key.toString() + "q" + i.toString()).innerHTML = decoded["queues"][key]["queue"][i-1]["name"];
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

function dequeue_250(){
    let pdata = JSON.stringify({token: getCookie("authToken"), class: "cse250"});
    ajaxPostRequest('/dequeue', pdata, process_queue_data);
}

function dequeue_220(){
    let pdata = JSON.stringify({token: getCookie("authToken"), class: "cse220"});
    ajaxPostRequest('/dequeue', pdata, process_queue_data);
}

function dequeue_331(){
    let pdata = JSON.stringify({token: getCookie("authToken"), class: "cse331"});
    ajaxPostRequest('/dequeue', pdata, process_queue_data);
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