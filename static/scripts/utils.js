$(document).ready(function() {
	$("#to-plot").click(function(e) {
		e.preventDefault();
		window.location.replace("plot");
	});
	$("#to-camera").click(function(e) {
		e.preventDefault();
		window.location.replace("camera");
	})
	$("#back").click(function(e) {
		e.preventDefault();
		window.location.replace("/");
	});
	$("#plot").click(function(e) {
		e.preventDefault();
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
	$("#camera").click(function(e) {
		e.preventDefault();
		var el = document.getElementById("cam-status");
		if (el) { el.innerHTML = "<p><i>Taking picture...</i></p>"}
		$.ajax({
			type: "POST",
			url: "camera",
			data: "{}",
			success: function(data) {
				if (el) {
					el.innerHTML = "<p style='color:green'>Picture taken successfully.</p>";
				}
			},
			error: function(xhr, status, error) {
				err = JSON.parse(xhr.responseText);
				alert(err.message);
				if (el) {
					el.innerHTML = "<p style='color:red'>Failed to take a picture.</p>";
				}
			},
			contentType: "application/json",
			dataType: "json"
		})
	});
});
