// Global variables
// This could be done in React with state, but will work fine
// for this simple project
var imgs = [];
// Range of images to display, img_idx * 5 to img_ix * 5 + 5
img_idx = 0;

// Main AJAX application
$(document).ready(function() {
	// Redirect to plotting page
	$("#to-plot").click(function(e) {
		e.preventDefault();
		window.location.replace("plot");
	});
	// Redirect to camera page
	$("#to-camera").click(function(e) {
		e.preventDefault();
		window.location.replace("camera");
	});
	// Redirect to image browsing page
	$("#to-images").click(function(e) {
		e.preventDefault();
		window.location.replace("images");
	});
	// Redirect to image uploading page
	$("#to-upload").click(function(e) {
		e.preventDefault();
		window.location.replace("upload");
	});
	$("#to-logs").click(function(e) {
		e.preventDefault();
		window.location.replace("stats");
	})
	// Redirect to home page
	$("#back").click(function(e) {
		e.preventDefault();
		window.location.replace("/");
	});
	// Call plotting API
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
	// Call camera API
	$("#camera").click(function(e) {
		e.preventDefault();
		// Ask user to wait
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
	// Call when user uploads an image
	$("#upload-form").submit(function(e) {
		var el = document.getElementById("upload-resp");
		if (el) { el.innerHTML = "<span><i>Uploading file, please wait...</i></span>"; }
		e.preventDefault();
		var formData = new FormData(this);
		$.ajax({
			type: "POST",
			url: "upload",
			data: formData,
			cache: false,
        	contentType: false,
        	processData: false,
			success: function(data) {
				if (el) {
					el.innerHTML = "<span style='color:green'>File uploaded successfully.</span>";
				}
			},
			error: function(xhr, status, error) {
				var el = document.getElementById("upload-resp");
				if (el) {
					el.innerHTML = "<span style='color:red'>" + JSON.parse(xhr.responseText).message + "</span>";
				}
			}
		});
	});
	// Call images API when user is on images page
	// Fetch all image names from database
	if (window.location.href.indexOf("images") != -1) {
		$.ajax({
			type: "POST",
			url: "images",
			success: function(data) {
				img_idx = 0;
				imgs = data.images;
				displayImages("del");
			},
			error: function(xhr, status, error) {
				err = JSON.parse(xhr.responseText);
				alert(err.message);
			},
			contentType: "application/json",
			dataType: "json"
		});
	}
	// Do the same on plotting page, there is probably a shorter way to do it
	// using functions
	if (window.location.href.indexOf("plot") != -1) {
		$.ajax({
			type: "POST",
			url: "images",
			success: function(data) {
				img_idx = 0;
				imgs = data.images;
				displayImages("plt");
			},
			error: function(xhr, status, error) {
				err = JSON.parse(xhr.responseText);
				alert(err.message);
			},
			contentType: "application/json",
			dataType: "json"
		});
	}
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
			error: function(xhr, status, error) {
				err = JSON.parse(xhr.responseText);
				alert(err.message);
			},
			contentType: "application/json",
			dataType: "json"
		});
	}
});

// Display images based on img_idx
// From (img_idx * 5) to (img_idx * 5 + 5) 
function displayImages(type) {
	html = "<ul class='list-group'>";
	for (var img of imgs.slice(img_idx * 5, (img_idx * 5) + 5)) {
		if (type === "del") html += "<a class='list-group-item list-group-item-action' onClick='getImage(\"";
		else html += "<a class='list-group-item list-group-item-action' onClick='getPlotImage(\"";
		html += img;
		html += "\")'>";
		html += img;
		html += "</a>"
	}
	html += "</ul>"
	var el = document.getElementById("img-list")
	if (el) {
		el.innerHTML = html;
	}
}

// Increment img_idx and fetch next images
function getNextImages() {
	// Prevent going beyond range
	if ((img_idx+1) * 5 <  imgs.length) {
		img_idx += 1;
		el = document.getElementById("img-pag");
		if (el) {
			el.innerHTML = "Images: ";
			el.innerHTML += (img_idx * 5);
			el.innerHTML += " - ";
			el.innerHTML += (img_idx * 5) + 5;
		}
	}
	displayImages();
}

// Decrement img_idx and fetch previous images
function getPrevImages() {
	// Prevent negative index
	if (img_idx > 0) {
		img_idx -= 1;
		el = document.getElementById("img-pag");
		if (el) {
			el.innerHTML = "Images: ";
			el.innerHTML += (img_idx * 5);
			el.innerHTML += " - ";
			el.innerHTML += (img_idx * 5) + 5;
		}
	}
	displayImages();
}

function removeImage(val) {
	img_idx = 0;
	$.ajax({
		type: "DELETE",
		url: "images/" + val,
		success: function() {
			// TODO: Might be a good idea to move this into a function instead of copying it from
			// function called upon images page loading
			$.ajax({
				type: "POST",
				url: "images",
				success: function(data) {
					imgs = data.images;
					displayImages();
				},
				error: function(xhr, status, error) {
					err = JSON.parse(xhr.responseText);
					alert(err.message);
				},
				contentType: "application/json",
				dataType: "json"
			});
		},
		error: function(xhr, status, error) {
			err = JSON.parse(xhr.responseText);
			alert(err.message);
		}
	});
}


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
		success: function(data) {
			if (el) {
				el.innerHTML = "<span style='color:green'>Image successfully plotted!</span>";
			}
		},
		error: function(xhr, status, error) {
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
		error: function(xhr, status, error) {
			err = JSON.parse(xhr.responseText);
			alert(err.message);
		},
	});
}

// Get and display single image based on val (which is a filename string)
function getImage(val) {
	$.ajax({
		type: "GET",
		url: "images/" + val,
		success: function() {
			el = document.getElementById("img-list");
			if (el) {
				el.innerHTML = "<img style='width:100%;height:300px' src='display'/></br></br>";
				el.innerHTML += "<button type='button' class='btn btn-secondary' style='margin-right:5px' onClick='displayImages()'>Cancel</button>";
				el.innerHTML += "<button type='button' class='btn btn-danger' onClick='removeImage(\"" + val + "\")'>Delete</button>";
			}
		},
		error: function(xhr, status, error) {
			err = JSON.parse(xhr.responseText);
			alert(err.message);
		},
	});
}
