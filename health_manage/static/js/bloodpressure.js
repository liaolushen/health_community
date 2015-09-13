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
        if (value['bloodpressure']) {
            var yearAndMonth = getYearAndMonthOfCurrentPage()
            var className = ".calendar-day-" + yearAndMonth['year'] + "-" + yearAndMonth['month'] + '-' + key;
            $(className).append('<div class="my-date">' + value['bloodpressure'] + ' mmHg</div>');
        };
    })
}

// 传入今日的血压值
function changeData() {
    var bloodpressureData = $("#inputData").val()
    if (checkData(bloodpressureData)) {
        $('#myModal').modal('hide');
        $('#helpBlock').removeClass('warning');
        var yearAndMonth = getYearAndMonthOfCurrentPage();
        var day = $($(".today .day-contents")[0]).text();
        var postData = {};
        postData["bloodpressure"] = bloodpressureData;
        postData["year"] = yearAndMonth["year"];
        postData["month"] = yearAndMonth["month"];
        postData["day"] = day;
        $.post("/userrecord/update_bloodpressure", postData, function(data) {
            $(".today .my-date").remove();
            $(".today").append('<div class="my-date">' + bloodpressureData + ' mmHg</div>');
            alert(data);
        })
    } else {
        $('#helpBlock').addClass('warning');
    }
}