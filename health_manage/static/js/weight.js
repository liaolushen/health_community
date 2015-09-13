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
    	if (value['weight']) {
    		var yearAndMonth = getYearAndMonthOfCurrentPage()
        	var className = ".calendar-day-" + yearAndMonth['year'] + "-" + yearAndMonth['month'] + '-' + key;
        	$(className).append('<div class="my-date">' + value['weight'] + ' kg</div>');
    	};
    })
}

// 传入今日的体重值
function changeData() {
    var weightData = $("#inputData").val()
    if (checkData(weightData)) {
        $('#myModal').modal('hide');
        $('#helpBlock').removeClass('warning');
        var yearAndMonth = getYearAndMonthOfCurrentPage();
        var day = $($(".today .day-contents")[0]).text();
        var postData = {};
        postData["weight"] = weightData;
        postData["year"] = yearAndMonth["year"];
        postData["month"] = yearAndMonth["month"];
        postData["day"] = day;
        $.post("/userrecord/update_weight", postData, function(data) {
            $(".today .my-date").remove();
            $(".today").append('<div class="my-date">' + weightData + ' kg</div>');
            alert(data);
        })
    } else {
        $('#helpBlock').addClass('warning');
    }
}