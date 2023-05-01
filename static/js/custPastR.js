function getTime(str) {
    return str.slice(12, 16) + " " + str.slice(8, 11) + " " + str.slice(5, 7) + " " + str.slice(17, 22);
}

// add on ticket infomations to the table
for (let i = 0; i < info_flask.length; i++) {
    const newtr = document.createElement("tr");
    const newCompany = document.createElement("td");
    newCompany.innerHTML = info_flask[i]['name'];

    const newCity = document.createElement("td");
    newCity.innerHTML = info_flask[i]['city'];

    const newState = document.createElement("td");
    newState.innerHTML = info_flask[i]['state'];

    const newType = document.createElement("td");
    newType.innerHTML = info_flask[i]['brand'];

    const newRentalDate= document.createElement("td");
    newRentalDate.innerHTML = getTime(info_flask[i]['rent_date']);
    const newReturnDate= document.createElement("td");
    newReturnDate.innerHTML = getTime(info_flask[i]['return_date']);

    newtr.appendChild(newCompany);
    newtr.appendChild(newCity);
    newtr.appendChild(newState);
    newtr.appendChild(newType);
    newtr.appendChild(newRentalDate);
    newtr.appendChild(newReturnDate);
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
        company_id: info.children[0].innerHTML
    }
    post("/custHome/rateC", retInfo);
} $("button").click(function () {
    toRate(this.id);
});