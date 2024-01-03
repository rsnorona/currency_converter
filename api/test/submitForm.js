var form = document.createElement("form");
form.method = "POST";
form.action = arguments[0];

var data = arguments[1];

for (var key in data) {
    if (data.hasOwnProperty(key)) {
        var input = document.createElement("input");
        input.type="str";
        input.name = key;
        input.value = data[key];
        form.appendChild(input);
    }
}

document.body.appendChild(form);
form.submit();
