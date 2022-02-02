// ------------------------------------------------------------------------------------------
// Scripts shared between multiple components
// + general utility functions
// ------------------------------------------------------------------------------------------

// Global variables
// This could be done in React with state, but will work fine
// for this simple project
var imgs = [];
// Range of images to display, img_idx * 5 to img_ix * 5 + 5
img_idx = 0;

// Fetch images from the database
// type - Type of the view to create
// del - With delete button (when browsing images view)
// plt - With plot button (when plotting view)
function fetchImages(type) {
	$.ajax({
		type: "POST",
		url: "images",
		success: function(data) {
			img_idx = 0;
			imgs = data.images;
			displayImages(type);
		},
		error: function(xhr, _, _) {
			err = JSON.parse(xhr.responseText);
			alert(err.message);
		},
		contentType: "application/json",
		dataType: "json"
	});
}

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
