// All scripts called on plotting view
$(document).ready(function() {
	if (window.location.href.indexOf("plot") != -1) { fetchImages("plt"); }
});

// Initiate plotting of specified image
function plotImage(val) {
	var el = document.getElementById("plot-status");
	if (el) {
		el.innerHTML = "<span><i>Plotting your image, please wait...</i></span>";
	}
	$.ajax({
		type: "POST",
		url: "plot",
		data: '{"image": "' + val + '"}',
		success: function() {
			if (el) {
				el.innerHTML = "<span style='color:green'>Image successfully plotted!</span>";
			}
		},
		error: function(xhr, _, _) {
			err = JSON.parse(xhr.responseText);
			if (el) {
				el.innerHTML = "<span style='color:red'>" + err.message + "</span>";
			}
		},
		contentType: "application/json",
		dataType: "json"
	});
}

// Get and display single image with option for plotting
function getPlotImage(val) {
	$.ajax({
		type: "GET",
		url: "images/" + val,
		success: function() {
			el = document.getElementById("img-list");
			if (el) {
				el.innerHTML = "<img style='width:100%;height:300px' src='display'/></br></br>";
				el.innerHTML += "<button type='button' class='btn btn-secondary' style='margin-right:5px' onClick='displayImages()'>Cancel</button>";
				el.innerHTML += "<button type='button' class='btn btn-primary' onClick='plotImage(\"" + val + "\")'>Plot</button>";
			}
		},
		error: function(xhr, _, _) {
			err = JSON.parse(xhr.responseText);
			alert(err.message);
		},
	});
}
