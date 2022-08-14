const host_name = document.getElementById("host_name");
const list = document.getElementById("user-questions-list");
const bodyView = document.getElementById("question");
const errorView = document.getElementById("error");
const submitButton = document.getElementById("submit-button");
const loader = document.getElementById("loader");

const ws = new WebSocket('ws://placementtalks.ccstiet.com/ws/public')

ws.onopen = function() {
    console.log("websocket connection open...");
}

ws.onmessage = function(event) {
    console.log("message.. ", event)
    const data = JSON.parse(event.data)
    if(data.type=='question') {
        let node = document.createElement("li");
        let textNode = document.createTextNode(data.text);
        node.appendChild(textNode);
        node.id = data.id;
        node.classList.add("previous-question")
        list.appendChild(node);
        submitButton.classList.remove("hidden");
        loader.classList.add("hidden");
    }
    else {
        let node = document.getElementById(data.id);
        if(data.isAccepted) {
            node.classList.remove("rejected");
            node.classList.add("accepted");
        }
        else {
            node.classList.remove("accepted");
            node.classList.add("rejected");
        }
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

function raiseQuestion() {
    const questioner = document.getElementById('questioner');
    const text = document.getElementById('text');
    const data = {
        questioner: questioner.value,
        text: text.value,
    };
    submitButton.classList.add("hidden");
    loader.classList.remove("hidden");
    ws.send(JSON.stringify(data));
    text.value = "";
    return false;
}
