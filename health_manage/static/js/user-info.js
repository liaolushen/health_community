function storeForm(argument) {
    var vals = $("#healthForm").serialize();
    $.post("/userinfo", vals, function (data) {
        alert(data)
    })
}