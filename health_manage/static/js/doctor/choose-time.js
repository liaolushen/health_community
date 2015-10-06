$(function () {
	getOrderSize($('#date').val());
	
    $('.input-group.date').datepicker({
	    format: "yyyy-mm-dd",
	    language: "zh-CN",
	    orientation: "top left",
	    startDate: Date(),
	    todayHighlight: true
	}).on('changeDate', function(e) {
        getOrderSize($('#date').val());
	});
});

function getOrderSize(choosenDate) {
	if (choosenDate == "") return;

	var postDate = {
						"date": choosenDate,
						"doctor_id": getURLParameter("doctor_id")
					};

	$.ajax({
		url: "/doctor/getordersize",
		data: postDate,
		xhrFields: {
			withCredentials: true
		},
		success: function(data) {
			replacePage(data);
		}
	})
}

/**
* the format of data is {"morning": xx, "afternoon": xx}
*/
function replacePage(data) {
	$('#morning-data').replaceWith('<span id="morning-data">' + data["morning"] + '</span>');
	$('#afternoon-data').replaceWith('<span id="afternoon-data">' + data["afternoon"] + '</span>');

	if (data["morning"] > 0) {
		$('#morning').attr("onclick", "pageJump('morning');");
	} else {
		$('#morning').removeAttr("onclick");
	}

	if (data["afternoon"] > 0) {
		$('#afternoon').attr("onclick", "pageJump('afternoon');");
	} else {
		$('#afternoon').removeAttr("onclick");
	}
}

function pageJump(time) {
	window.location.href =
		"/doctor/createorder?doctor_id="
		+decodeURIComponent("doctor_id")
		+"&date="+$('#date').val()
		+"&time="+time;  
}

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
}