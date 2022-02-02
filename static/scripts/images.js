// All scripts called on image display view
$(document).ready(function() {
    // Call images API when user is on images page
	// Fetch all image names from database
	if (window.location.href.indexOf("images") != -1) { fetchImages("del"); }
});

// Remove image from the database and refresh the page
function removeImage(val) {
	img_idx = 0;
	$.ajax({
		type: "DELETE",
		url: "images/" + val,
		success: function() {
			fetchImages("del");
		},
		error: function(xhr, _, _) {
			err = JSON.parse(xhr.responseText);
			alert(err.message);
		}
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
		error: function(xhr, _, _) {
			err = JSON.parse(xhr.responseText);
			alert(err.message);
		},
	});
}
