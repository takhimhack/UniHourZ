onload_func();

function onload_func() {
    let pdata = JSON.stringify({token: getCookie('authToken'), edit: 'false', class: document.getElementsByTagName('body')[0].getAttribute('id')});
    ajaxPostRequest('/settings', pdata, update_info);
}

function update_info(set_response) {
    let decoded = JSON.parse(set_response);
    if (decoded["status"] === 'open'){
        document.getElementById('flexSwitchCheckDefault').setAttribute('checked', '');
    }
    document.getElementById('instructor-name').setAttribute('value', decoded["instructor"]);
    document.getElementById('office-location').setAttribute('value', decoded["location"]);
    document.getElementById('estimated-time').setAttribute('value', decoded["eta"]);
}

function toggle() {
  document.getElementById('instructor-name').disabled = false;
  document.getElementById('office-location').disabled = false;
  document.getElementById('estimated-time').disabled = false;
  document.getElementById('flexSwitchCheckDefault').disabled = false;
  document.getElementById('editcse').hidden = true;
  document.getElementById('savecse').hidden = false;
}

function submit_changes() {
    let ison = 'closed';
    if (document.getElementById('flexSwitchCheckDefault').checked) {
        ison = 'open';
    }
    let pdata = JSON.stringify({token: getCookie('authToken'), edit: 'true', class: document.getElementsByTagName('body')[0].getAttribute('id'), instructor: document.getElementById('instructor-name').value, location: document.getElementById('office-location').value, eta: document.getElementById('estimated-time').value, status: ison});
    ajaxPostRequest('/settings', pdata, redir);
}

function redir() {
    window.location = '/courses.html';
}


//function cse220() {
//  document.getElementById('instructor-name-220').disabled = false;
//  document.getElementById('office-location-220').disabled = false;
//  document.getElementById('estimated-time-220').disabled = false;
//  document.getElementById('flexSwitchCheckDefault').disabled = false;
//  document.getElementById('editcse220').hidden = true;
//  document.getElementById('savecse220').hidden = false;
//
//  return false;
//}
//
//
//
//function cse331() {
//  document.getElementById('instructor-name-331').disabled = false;
//  document.getElementById('office-location-331').disabled = false;
//  document.getElementById('estimated-time-331').disabled = false;
//  document.getElementById('flexSwitchCheckDefault').disabled = false;
//  document.getElementById('editcse331').hidden = true;
//  document.getElementById('savecse331').hidden = false;
//
//  return false;
//}

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

