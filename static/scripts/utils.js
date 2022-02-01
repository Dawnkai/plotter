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
				var el = document.getElementById("upload-resp");
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
			data: '{"start": 0, "end": 10}',
			success: function(data) {
				img_idx = 0;
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
	}
});

// Display images based on img_idx
// From (img_idx * 5) to (img_idx * 5 + 5) 
function displayImages() {
	html = "<ul class='list-group'>";
	for (var img of imgs.slice(img_idx * 5, (img_idx * 5) + 5)) {
		html += "<a class='list-group-item list-group-item-action' onClick='getImage(\"";
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

// Get and display single image based on val (which is a filename string)
function getImage(val) {
	$.ajax({
		type: "GET",
		url: "images/" + val,
		success: function() {
			el = document.getElementById("img-list");
			if (el) {
				el.innerHTML = "<img style='width:100%;height:300px' src='display'/></br></br>";
				el.innerHTML += "<button type='button' class='btn btn-secondary' onClick='displayImages()'>Back</button>"
			}
		},
		error: function(xhr, status, error) {
			err = JSON.parse(xhr.responseText);
			alert(err.message);
		},
	});
}
