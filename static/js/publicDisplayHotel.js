

// add on ticket infomations to the table
for (let i = 0; i < info_flask.length; i++) {
    const newtr = document.createElement("tr");
    const newHotelName= document.createElement("td");
    newHotelName.innerHTML = info_flask[i]['name'];
    const newStars = document.createElement("td");
    newStars.innerHTML = info_flask[i]['stars'];
    const newRoomNumber = document.createElement("td");
    newRoomNumber.innerHTML = info_flask[i]['number'];
    const newPrice = document.createElement("td");
    newPrice.innerHTML = info_flask[i]['price'];

    newtr.appendChild(newHotelName);
    newtr.appendChild(newStars);
    newtr.appendChild(newRoomNumber);
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
$("button").click(function () {
    alert("Purchase Needs Login/Signup First!");
});
function getTime(str) {
    return str.slice(12, 16) + " " + str.slice(8, 11) + " " + str.slice(5, 7) + " " + str.slice(17, 22);
}