function createNewOrderPeople() {
	var name = $('#name').val();
	var idCard = $('#id-card').val();
	var telephone = $('#telephone').val();
	var hospitalCard = $('#hospital-card').val();

	if (!name || !idCard || !telephone || !hospitalCard) {
		alert("有选项未填！");
		return false;
	}

	var postDate = {
						"name": name,
						"id_card": idCard,
						"telephone": telephone,
						"hospital_card": hospitalCard
					};

	$.ajax({
		url: "/doctor/addorderpeople",
		method: "POST",
		data: postDate,
		xhrFields: {
			withCredentials: true
		},
		success: function(data) {
			if (data['code'] == 500) {
				alert(data['info']);
				return false;
			} else {
				backToCreateOrderPage();
			}
		}
	})
}

function backToCreateOrderPage() {
	window.location = document.referrer;
}
