// All scripts responsible for handling camera requests
$(document).ready(function() {
    // Take a picture
	$("#camera").click(function(e) {
		e.preventDefault();
		// Ask user to wait
		var el = document.getElementById("cam-status");
		if (el) { el.innerHTML = "<p><i>Taking picture...</i></p>"}
		$.ajax({
			type: "POST",
			url: "camera",
			data: "{}",
			success: function() {
				if (el) {
					el.innerHTML = "<p style='color:green'>Picture taken successfully.</p>";
				}
			},
			error: function(xhr, _, _) {
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
