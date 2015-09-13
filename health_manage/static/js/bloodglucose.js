$(document).ready(function(){
    initData();
});

function initData() {
    var postData = getYearAndMonthOfCurrentPage();
    $.post("/userrecord/get_user_record", postData, function(data) {
        inputData(data);
        console.log(data);
    })
}

// 将取到的数据放入页面中
function inputData(data) {
    $.each(data, function(key, value) {
        if (value['bloodglucose']) {
            var yearAndMonth = getYearAndMonthOfCurrentPage()
            var className = ".calendar-day-" + yearAndMonth['year'] + "-" + yearAndMonth['month'] + '-' + key;
            $(className).append('<div class="my-date">' + value['bloodglucose'] + ' mg</div>');
        };
    })
}

// 传入今日的血糖值
function changeData() {
    var bloodglucoseData = $("#inputData").val()
    if (checkData(bloodglucoseData)) {
        $('#myModal').modal('hide');
        $('#helpBlock').removeClass('warning');
        var yearAndMonth = getYearAndMonthOfCurrentPage();
        var day = $($(".today .day-contents")[0]).text();
        var postData = {};
        postData["bloodglucose"] = bloodglucoseData;
        postData["year"] = yearAndMonth["year"];
        postData["month"] = yearAndMonth["month"];
        postData["day"] = day;
        $.post("/userrecord/update_bloodglucose", postData, function(data) {
            $(".today .my-date").remove();
            $(".today").append('<div class="my-date">' + bloodglucoseData + ' mg</div>');
            alert(data);
        })
    } else {
        $('#helpBlock').addClass('warning');
    }
}