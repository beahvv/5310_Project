
ret1 = info_flask[0];
ret2 = info_flask[1];
if (ports) {
    ports.innerHTML += "From \t" + info_ports["depart_port"][0] + " \t To \t" + info_ports["arrival_port"][0];
}


// add on ticket infomations to the table
if (thing) {
    for (let i = 0; i < ret1.length; i++) {
        const newtr = document.createElement("tr");
        const newAirline = document.createElement("td");
        newAirline.innerHTML = ret1[i]['airline_name'];
        const newFlight = document.createElement("td");
        newFlight.innerHTML = ret1[i]['flight_num'];
        const newDepartTime = document.createElement("td");
        newDepartTime.innerHTML = getTime(ret1[i]['depart_time']);
        const newArrivalTime = document.createElement("td");
        newArrivalTime.innerHTML = getTime(ret1[i]['arrival_time']);
        const newPrice = document.createElement("td");
        newPrice.innerHTML = ret1[i]['base_price'];
        newtr.appendChild(newAirline);
        newtr.appendChild(newFlight);
        newtr.appendChild(newDepartTime);
        newtr.appendChild(newArrivalTime);
        newtr.appendChild(newPrice);
        thing.appendChild(newtr);
    }
}

if (ports2) {
    ports2.innerHTML += "From \t" + info_ports["arrival_port"][0] + " \t To \t" + info_ports["depart_port"][0];
}
if (thing2) {
    for (let i = 0; i < ret2.length; i++) {
        const newtr = document.createElement("tr");
        const newAirline = document.createElement("td");
        newAirline.innerHTML = ret2[i]['airline_name'];
        const newFlight = document.createElement("td");
        newFlight.innerHTML = ret2[i]['flight_num'];
        const newDepartTime = document.createElement("td");
        newDepartTime.innerHTML = getTime(ret2[i]['depart_time']);
        const newArrivalTime = document.createElement("td");
        newArrivalTime.innerHTML = getTime(ret2[i]['arrival_time']);
        const newPrice = document.createElement("td");
        newPrice.innerHTML = ret2[i]['base_price'];
        newtr.appendChild(newAirline);
        newtr.appendChild(newFlight);
        newtr.appendChild(newDepartTime);
        newtr.appendChild(newArrivalTime);
        newtr.appendChild(newPrice);
        thing2.appendChild(newtr);
    }
}

// add buy buttons to each column, each with unique id
for (let i = 0; i < thing.childElementCount; i++) {
    const newtd = document.createElement("td");
    const newButton = document.createElement("button");
    newButton.innerHTML = "Buy";
    newButton.id = "btn-forward" + i;
    newButton.className = "btn btn-primary";
    newtd.appendChild(newButton);
    thing.children[i].appendChild(newtd);
}
for (let i = 0; i < thing2.childElementCount; i++) {
    const newtd = document.createElement("td");
    const newButton = document.createElement("button");
    newButton.innerHTML = "Buy";
    newButton.id = "btn-return" + i;
    newButton.className = "btn btn-primary";
    newtd.appendChild(newButton);
    thing2.children[i].appendChild(newtd);
}
$("button").click(function () {
    alert("Purchase Needs Login/Signup First!");
});
function getTime(str) {
    return str.slice(12, 16) + " " + str.slice(8, 11) + " " + str.slice(5, 7) + " " + str.slice(17, 22);
}