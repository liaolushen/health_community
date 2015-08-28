$(document).ready(function(){
    initPage();
    initData();
});

// 页面的初始化
function initPage() {
    $('#myModal').on('shown.bs.modal', function () {
        $('#myInput').focus()
    })

    $(".today").click(function() {
        $('#myModal').modal('show');
    });

    adjustModalMaxHeightAndPosition();
    if ($(window).height() >= 320){
        $(window).resize(adjustModalMaxHeightAndPosition).trigger("resize");
    }
}

function initData() {
    $(".today").append('<div class="my-date">50.4kg</div>');
    $("#inputData").val(50.4);
    var postData = getMonthAndYearOfCurrentPage();
    $.post("/userrecord?info=get_user_record", postData, function(data) {
        alert(data);
    })
}


// 自动调节模态框的大小
function adjustModalMaxHeightAndPosition(){
    $('.modal').each(function(){
        if($(this).hasClass('in') == false){
            $(this).show(); /* Need this to get modal dimensions */
        };
        var contentHeight = $(window).height() - 60;
        var headerHeight = $(this).find('.modal-header').outerHeight() || 2;
        var footerHeight = $(this).find('.modal-footer').outerHeight() || 2;

        $(this).find('.modal-content').css({
            'max-height': function () {
                return contentHeight;
            }
        });

        $(this).find('.modal-body').css({
            'max-height': function () {
                return (contentHeight - (headerHeight + footerHeight));
            }
        });

        $(this).find('.modal-dialog').addClass('modal-dialog-center').css({
            'margin-top': function () {
                return -($(this).outerHeight() / 2);
            },
            'margin-left': function () {
                return -($(this).outerWidth() / 2);
            }
        });
        if($(this).hasClass('in') == false){
            $(this).hide(); /* Hide modal */
        };
    });
};

// 传入今日的体重值
function changeData() {
    var data = $("#inputData").val()
    if (checkData(data)) {
        $('#myModal').modal('hide');
        $('#helpBlock').removeClass('warning');
        var postData = {"weight" : data};
        $.post("/userrecord?info=update_user_record", postData, function(data) {
            alert(data);
        })
    } else {
        $('#helpBlock').addClass('warning');
    }
}

// 验证数据格式是否正确
function checkData(data) {
    var reg = new RegExp("^[0-9]+(.[0-9])$");
    return reg.test(data);
}

// 得到当前页面的年份和月份，返回json格式：{"year":xxxx, "month":xxxx}
function getMonthAndYearOfCurrentPage() {
    var classValue = $($("tbody > tr > td")[6]).attr("class");
    var currentPageDate = new String(classValue.match("[0-9]{4}-[0-9]{2}"));
    var year = currentPageDate.split('-')[0];
    var month = currentPageDate.split('-')[1];
    return {"year":year, "month":month};
}