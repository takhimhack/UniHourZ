function loadpage() {
    //let pdata = JSON.stringify({token: getCookie("authToken")});
    ajaxGetRequest('/queuedata', process_queue_data);
    setTimeout(loadpage, 10000);
}
onload_func();
loadpage();
let open220 = 0;
let open250 = 0;
let open331 = 0;

function onload_func() {
    //let pdata = JSON.stringify({token: getCookie("authToken")});
    ajaxGetRequest('/checkstatus', html_setup);
}



function html_setup(setup_response) {
    let decoded = JSON.parse(setup_response);
    if (decoded.valid === 'valid'){
        let doms =document.getElementsByTagName('h4');
              for (var k = 0; k < doms.length; k++) {
            if (doms[k].hasAttribute("homehidden")) {
                  var myobj = document.getElementsByClassName("homeremove");
                doms[k].remove(myobj)
            }
        }

               doms = document.getElementsByTagName('a');
        for (var k = 0; k < doms.length; k++) {
            if (doms[k].hasAttribute("homehidden")) {
                  var myobj = document.getElementsByClassName("homeremove");
                doms[k].remove(myobj)
            }
        }


            doms=document.getElementsByTagName('button');
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
            if (decoded["queues"][key]["status"] === 'open') {
                if (key === 'CSE220') {
                    if (open220 === 0) {
                        document.getElementById('CSE220closed').innerHTML = "";
                        document.getElementById('CSE220q').removeAttribute('hidden');
                        cse220 = 1;
                    }
                } else if (key === 'CSE250') {
                    if (open250 === 0) {
                        document.getElementById('CSE250closed').innerHTML = "";
                        document.getElementById('CSE250q').removeAttribute('hidden');
                        cse250 = 1;
                    }
                } else if (key === 'CSE331') {
                    if (open331 === 0) {
                        document.getElementById('CSE331closed').innerHTML = "";
                        document.getElementById('CSE331q').removeAttribute('hidden');
                        cse331 = 1;
                    }
                }
                for (let i = 1; i < 11; i++) {
                    if (i > decoded["queues"][key].length) {
                        document.getElementById(key.toString() + "q" + i.toString()).innerHTML = "";
                    } else {
                        document.getElementById(key.toString() + "q" + i.toString()).innerHTML = decoded["queues"][key]["queue"][i-1]["name"];
                    }
                }
                document.getElementById(key.toString() + "-instructor").innerHTML = decoded["queues"][key]["instructor"];
                document.getElementById(key.toString() + "-office").innerHTML = decoded["queues"][key]["location"];
                document.getElementById(key.toString() + "-eta").innerHTML = decoded["queues"][key]["eta"] + " minutes";
                document.getElementById(key.toString() + "-current-student").innerHTML = decoded["queues"][key]["student"];
            } else {
                if (key === 'CSE220') {
                    if (open220 === 1) {
                        document.getElementById('CSE220closed').innerHTML = "The queue is currently closed";
                        document.getElementById('CSE220q').setAttribute('hidden', '');
                        cse220 = 0;
                    }
                } else if (key === 'CSE250') {
                    if (open250 === 1) {
                        document.getElementById('CSE250closed').innerHTML = "The queue is currently closed";
                        document.getElementById('CSE250q').setAttribute('hidden', '');
                        cse250 = 0;
                    }
                } else if (key === 'CSE331') {
                    if (open331 === 1) {
                        document.getElementById('CSE331closed').innerHTML = "The queue is currently closed";
                        document.getElementById('CSE331q').setAttribute('hidden', '');
                        cse331 = 0;
                    }
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