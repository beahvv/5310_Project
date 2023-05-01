ports.innerHTML += "Check-in Date \t" + info_ports["check_in_date"][0] +","+" \t Check-Out Date \t" + info_ports["check_out_date"][0];


// add on ticket infomations to the table
for (let i = 0; i < info_flask.length; i++) {
    const newtr = document.createElement("tr");
    const newHotelName= document.createElement("td");
    newHotelName.innerHTML = info_flask[i]['name'];
    const newStars = document.createElement("td");
    newStars.innerHTML = info_flask[i]['stars'];
    const newRoomID = document.createElement("td");
    newRoomID.innerHTML = info_flask[i]['room_id'];
    const newPrice = document.createElement("td");
    newPrice.innerHTML = info_flask[i]['price'];

    newtr.appendChild(newHotelName);
    newtr.appendChild(newStars);
    newtr.appendChild(newRoomID);
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
        hotel_name: info.children[0].innerHTML,
        hotel_stars: info.children[1].innerHTML,
        room_id: info.children[2].innerHTML,
        rate_per_night: info.children[3].innerHTML
    }
    post("/custHome/purchHotel", retInfo);
}
$("button").click(function () {
    toPurchase(this.id);
});
function getTime(str) {
    return str.slice(12, 16) + " " + str.slice(8, 11) + " " + str.slice(5, 7) + " " + str.slice(17, 22);
}