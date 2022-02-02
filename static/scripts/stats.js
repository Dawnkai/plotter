// All scripts responsible for fetching stats of the plotter such as
// current state of the plotter and logs file
$(document).ready(function() {
    // Fetch plotter status when on status page
	if (window.location.href.indexOf("stats") != -1) {
		$.ajax({
			type: "GET",
			url: "stats/status",
			success: function(data) {
				el = document.getElementById("plotter-status");
				if (el) {
					if (data.message === "Idle") { el.innerHTML = "<b style='color:green'>Idle</b>"; }
					else if (data.message === "Busy") { el.innerHTML = "<b style='color:yellow'>Busy</b>"; }
					else if (data.message === "Error") { el.innerHTML = "<b style='color:red'>Error</b>"; }
				}
			},
			error: function(xhr, _, _) {
				err = JSON.parse(xhr.responseText);
				alert(err.message);
			},
			contentType: "application/json",
			dataType: "json"
		});
	}
});
