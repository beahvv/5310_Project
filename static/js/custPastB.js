function getTime(str) {
    return str.slice(12, 16) + " " + str.slice(8, 11) + " " + str.slice(5, 7) + " " + str.slice(17, 22);
}

// add on ticket infomations to the table
for (let i = 0; i < info_flask.length; i++) {
    const newtr = document.createElement("tr");
    const newID = document.createElement("td");
    newID.innerHTML = info_flask[i]['hotel_id'];

    const newHotel = document.createElement("td");
    newHotel.innerHTML = info_flask[i]['name'];

    const newCity = document.createElement("td");
    newCity.innerHTML = info_flask[i]['city'];
    const newState= document.createElement("td");
    newState.innerHTML = info_flask[i]['state'];

    const newRoomNumber = document.createElement("td");
    newRoomNumber.innerHTML = info_flask[i]['number'];

    const newCheckInDate = document.createElement("td");
    newCheckInDate.innerHTML = getTime(info_flask[i]['check_in_date']);
    const newCheckOutDate = document.createElement("td");
    newCheckOutDate.innerHTML = getTime(info_flask[i]['check_out_date']);

    newtr.appendChild(newHotel);
    newtr.appendChild(newCity);
    newtr.appendChild(newState);
    newtr.appendChild(newRoomNumber);
    newtr.appendChild(newCheckInDate);
    newtr.appendChild(newCheckOutDate);
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
        hotel_id: info.children[0].innerHTML
    }
    post("/custHome/rateH", retInfo);
} $("button").click(function () {
    toRate(this.id);
});