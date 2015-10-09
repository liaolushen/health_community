$(function () {
	var orderDate = getURLParameter("date");
	var DateItem = orderDate.split('-');
	orderDate = DateItem[0] + '年' + DateItem[1] + '月' + DateItem[2] + '日';

	var orderTime = getURLParameter("time");
	if (orderTime == "morning") orderTime = "9:00~11:00";
	if (orderTime == "afternoon") orderTime = "14:00~17:00";
	$('#order-time').replaceWith('<span class="order-value" id="order-time">'
		+ orderDate + ' ' + orderTime
		+'</span>');
});

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
}

function addPeople() {
    window.location.href = "/doctor/addorderpeople";
}

function createOrder() {
	var orderPeopleInfo = $("input[type='radio'][name='people-info']:checked").val();
	if (!orderPeopleInfo) {
		alert("请选择一位预约人");
		return false;
	}
	var postData = JSON.parse(orderPeopleInfo);
	postData['doctor_id'] = getURLParameter('doctor_id');
	postData['community'] = $($('.order-value')[0]).text();
	postData['doctor'] = $($('.order-value')[1]).text();
	postData['time'] = $($('.order-value')[2]).text();
	console.log(postData);
	
	$.ajax({
		url: "/doctor/createorder",
		method: "POST",
		data: postData,
		xhrFields: {
			withCredentials: true
		},
		success: function(data) {
			if (data['code'] == 500) {
				alert(data['info']);
				return false;
			} else {
				window.location.href = "/doctor";
			}
		}
	})
}