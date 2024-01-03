var form = document.createElement("form");
form.method = "POST";
form.action = arguments[0];

var data = arguments[1];

for (var key in data) {
    if (data.hasOwnProperty(key)) {
        var input = document.createElement("input");
        input.name = key;
        if (input.name === "exchange_rate") {
            input.type = "float";
            input.value = parseFloat(data[key]);
        }
        else{
            input.type="str";
            input.value = data[key];
        }
        form.appendChild(input);
    }
}

document.body.appendChild(form);
form.submit();
