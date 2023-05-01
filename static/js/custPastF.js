function getTime(str) {
    return str.slice(12, 16) + " " + str.slice(8, 11) + " " + str.slice(5, 7) + " " + str.slice(17, 22);
}

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

    const newDepartAirport = document.createElement("td");
    newDepartAirport.innerHTML = info_flask[i]['depart_airport'];
    const newArrivalAirport = document.createElement("td");
    newArrivalAirport.innerHTML = info_flask[i]['arrival_airport'];

    newtr.appendChild(newAirline);
    newtr.appendChild(newFlight);
    newtr.appendChild(newDepartTime);
    newtr.appendChild(newArrivalTime);
    newtr.appendChild(newDepartAirport);
    newtr.appendChild(newArrivalAirport);
    thing.appendChild(newtr);
}
for (let i = 0; i < thing.childElementCount; i++) {
    const newtd = document.createElement("td");
    const newButton = document.createElement("button");
    newButton.innerHTML = "Rate";
    newButton.id = "btn-" + i;
    newButton.className = "btn btn-primary";
    newtd.appendChild(newButton);
    thing.children[i].appendChild(newtd);
}
function toRate(id) {
    info = document.getElementById(id).parentElement.parentNode;
    retInfo = {
        airline: info.children[0].innerHTML,
        flight_num: info.children[1].innerHTML,
        depart_date: info.children[2].innerHTML
    }
    post("/custHome/rate", retInfo);
} $("button").click(function () {
    toRate(this.id);
});