$(function() {
	$('.search .search-bar .dropdown-toggle').dropdown();

	$('.search-li').click(function(event) {
		var that = event.target;
		var content = $(that).text();
		$('.search-select-content').text(content);
		$('.search-input-hidden').val(content);
	});

	$('.search-func-li').click(function(event) {
		var that = event.target;
		var content = $(that).text();
		$('.search-function-content').text(content);
		$('.search-input-func-hidden').val(content);
	});


})