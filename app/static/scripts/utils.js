$(document).ready(function() {
	$("#to-plot").click(function(e) {
		e.preventDefault();
		window.location.replace("plot");
	});
	$("#back").click(function(e) {
		e.preventDefault();
		window.location.replace("/");
	});
	$("#plot").click(function(e) {
		$.ajax({
			type: "POST",
			url: "plot",
			data: "{'data': 'Bajo'}",
			success: function(data) {
				console.log(data);
			},
			error: function(xhr, status, error) {
				err = JSON.parse(xhr.responseText);
				alert(err.message);
			},
			contentType: "application/json",
			dataType: "json"
		});
	});
});
