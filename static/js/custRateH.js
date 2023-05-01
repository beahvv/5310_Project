keys = Object.keys(info_fla);
values = Object.values(info_fla);
var left = document.getElementById("unchange");
const outer = document.createElement("div");
outer.className = "form-group row";

const label = document.createElement("label");
label.className = "col-3 col-form-label";
label.innerHTML = "Email";

const inner = document.createElement("div");
inner.className = "col-9";
const input = document.createElement("input");
input.className = "form-control";
input.type = "text";
input.readOnly = true;
input.value = email;
input.name = "cust_email";
inner.appendChild(input);
outer.appendChild(label);
outer.appendChild(inner);
left.appendChild(outer);
for (let i = 0; i < keys.length; i++) {
    const outer = document.createElement("div");
    outer.className = "form-group row";

    const label = document.createElement("label");
    label.className = "col-3 col-form-label";
    label.innerHTML = keys[i];
    if (label.innerHTML == "hotel_id") {
        label.innerHTML = "Hotel ID";
    }

    const inner = document.createElement("div");
    inner.className = "col-9";
    const input = document.createElement("input");
    input.className = "form-control";
    input.type = "text";
    input.readOnly = true;
    input.value = values[i];
    input.name = keys[i];
    inner.appendChild(input);
    outer.appendChild(label);
    outer.appendChild(inner);
    left.appendChild(outer);
}
