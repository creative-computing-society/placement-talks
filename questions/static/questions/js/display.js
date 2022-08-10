const host_name = document.getElementById("host_name");
const list = document.getElementById("questions-list");
const bodyView = document.getElementById("only");
const errorView = document.getElementById("error");

const ws = new WebSocket('ws://'+host_name.innerText+'/ws/display')

ws.onopen = function() {
    console.log("websocket connection open...");
}

ws.onmessage = function(event) {
    console.log("message.. ", event)
    const data = JSON.parse(event.data)
    if(data.type=='question') {
        let node = document.getElementById("sample-entry");
        let clone = node.cloneNode(true);
        let textP = clone.getElementsByClassName("question")[0];
        textP.innerText = data.text;
        clone.id = data.id;
        clone.classList.remove("hidden");
        list.appendChild(clone);
    }
    else {
        let node = document.getElementById(data.id);
        node.classList.add("hidden");
    }
}

ws.onclose = function(event) {
    console.log('disconnect.. ', event)
    bodyView.classList.add("hidden");
    errorView.classList.remove("hidden");
}

ws.onerror = function(event) {
    console.log('error.. ', event);
    bodyView.classList.add("hidden");
    errorView.classList.remove("hidden");
}
