const host_name = document.getElementById("host_name");
const list = document.getElementById("questions-list");
const bodyView = document.getElementById("only");
const errorView = document.getElementById("error");

const ws = new WebSocket('wss://placementtalks.ccstiet.com/ws/moderator')

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
        let questionerB = textP.getElementsByClassName("questioner")[0];
        questionerB.innerText = data.questioner;
        let textNode = document.createTextNode(data.text);
        textP.appendChild(textNode);
        clone.id = data.id;
        clone.classList.remove("hidden");
        list.appendChild(clone);
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
        let buttonContainer = node.getElementsByClassName("button-container")[0];
        let imgs = buttonContainer.getElementsByTagName("img");
        let loader = buttonContainer.getElementsByClassName("loading")[0];
        for(let i=0; i<imgs.length; i++) {
            imgs[i].classList.remove("hidden");
        }
        loader.classList.add("hidden");
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

function accept(id) {
    const data = {
        id: Number(id),
        isAccepted: true,
    };
    let buttonContainer = document.getElementById(id).getElementsByClassName("button-container")[0];
    let imgs = buttonContainer.getElementsByTagName("img");
    let loader = buttonContainer.getElementsByClassName("loading")[0];
    for(let i=0; i<imgs.length; i++) {
        imgs[i].classList.add("hidden");
    }
    loader.classList.remove("hidden");
    ws.send(JSON.stringify(data));
}

function reject(id) {
    const data = {
        id: Number(id),
        isAccepted: false,
    };
    let buttonContainer = document.getElementById(id).getElementsByClassName("button-container")[0];
    let imgs = buttonContainer.getElementsByTagName("img");
    let loader = buttonContainer.getElementsByClassName("loading")[0];
    for(let i=0; i<imgs.length; i++) {
        imgs[i].classList.add("hidden");
    }
    loader.classList.remove("hidden");
    ws.send(JSON.stringify(data));
}
