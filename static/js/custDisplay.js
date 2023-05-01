// ports.innerHTML += "From \t" + info_ports["depart_port"][0] + " \t To \t" + info_ports["arrival_port"][0];
 

// add on ticket infomations to the table
for (let i = 0; i < info_flask.length; i++) {
    const newtr = document.createElement("tr");
    const newAirline = document.createElement("td");
    newAirline.innerHTML = info_flask[i]['airline_name'];
    const newFlight = document.createElement("td");
    newFlight.innerHTML = info_flask[i]['flight_num'];
    const newDepartTime = document.createElement("td");
    newDepartTime.innerHTML = getTime(info_flask[i]['depart_time']);
    const newArrivalTime = document.createElement("td");
    newArrivalTime.innerHTML = getTime(info_flask[i]['arrival_time']);
    const newPrice = document.createElement("td");
    newPrice.innerHTML = info_flask[i]['base_price'];
    newtr.appendChild(newAirline);
    newtr.appendChild(newFlight);
    newtr.appendChild(newDepartTime);
    newtr.appendChild(newArrivalTime);
    newtr.appendChild(newPrice);
    thing.appendChild(newtr);
}

// add buy buttons to each column, each with unique id
for (let i = 0; i < thing.childElementCount; i++) {
    const newtd = document.createElement("td");
    const newButton = document.createElement("button");
    newButton.innerHTML = "Buy";
    newButton.id = "btn-" + i;
    newButton.className = "btn btn-primary";
    newtd.appendChild(newButton);
    thing.children[i].appendChild(newtd);
}
function toPurchase(id) {
    info = document.getElementById(id).parentElement.parentNode;
    retInfo = {
        airline: info.children[0].innerHTML,
        flight_num: info.children[1].innerHTML,
        depart_date: info.children[2].innerHTML,
        arrival_date: info.children[3].innerHTML,
        price: info.children[4].innerHTML
    }
    post("/custHome/purch", retInfo);
}
$("button").click(function () {
    toPurchase(this.id);
});
function getTime(str) {
    return str.slice(12, 16) + " " + str.slice(8, 11) + " " + str.slice(5, 7) + " " + str.slice(17, 22);
}