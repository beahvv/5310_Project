ports.innerHTML += "Rental Date \t" + info_ports["rent_date"][0] +","+" \t Return Date \t" + info_ports["return_date"][0];


// add on ticket infomations to the table
for (let i = 0; i < info_flask.length; i++) {
    const newtr = document.createElement("tr");
    const newCompanyName= document.createElement("td");
    newCompanyName.innerHTML = info_flask[i]['name'];
    const newCar= document.createElement("td");
    newCar.innerHTML = info_flask[i]['car_id'];
    const newBrand = document.createElement("td");
    newBrand.innerHTML = info_flask[i]['brand'];
    const newType = document.createElement("td");
    newType.innerHTML = info_flask[i]['type'];
    const newColor = document.createElement("td");
    newColor.innerHTML = info_flask[i]['color'];
    const newPrice = document.createElement("td");
    newPrice.innerHTML = info_flask[i]['base_price'];

    newtr.appendChild(newCompanyName);
    newtr.appendChild(newCar);
    newtr.appendChild(newBrand);
    newtr.appendChild(newType);
    newtr.appendChild(newColor);
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
        name: info.children[0].innerHTML,
        car_id: info.children[1].innerHTML,
        brand: info.children[2].innerHTML,
        type: info.children[3].innerHTML,
        color: info.children[4].innerHTML,
        base_price: info.children[5].innerHTML
    }
    post("/custHome/purchCar", retInfo);
}
$("button").click(function () {
    toPurchase(this.id);
});
function getTime(str) {
    return str.slice(12, 16) + " " + str.slice(8, 11) + " " + str.slice(5, 7) + " " + str.slice(17, 22);
}