const list = document.getElementById("questions-list");
const bodyView = document.getElementById("only");
const errorView = document.getElementById("error");

class bgColour {
    static idx = -1;
    static color = ["#a3623a", "#0ed095", "#fc5f9b"];
    static getColor() {
        return this.color[this.idx=(++this.idx)%this.color.length];
    }
}

const assignColor = function() {
    let entries = document.getElementsByClassName("question-box");
    for(let i=0; i<entries.length; i++) {
        entries[i].style.setProperty('--clr', bgColour.getColor());
    }
}

const ws = new WebSocket('ws://127.0.0.1:8000/ws/display')

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
        let questionerP = clone.getElementsByClassName("name")[0];
        questionerP.innerText = "~"+data.questioner;
        textP.innerText = data.text;
        clone.id = data.id;
        clone.style.setProperty('--clr', bgColour.getColor());
        clone.classList.remove("hidden");
        list.appendChild(clone);
    }
    else {
        let node = document.getElementById(data.id);
        node.remove()
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