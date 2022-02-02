// All scripts responsible for uploading images to the server
$(document).ready(function() {
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
			success: function() {
				if (el) {
					el.innerHTML = "<span style='color:green'>File uploaded successfully.</span>";
				}
			},
			error: function(xhr, _, _) {
				var el = document.getElementById("upload-resp");
				if (el) {
					el.innerHTML = "<span style='color:red'>" + JSON.parse(xhr.responseText).message + "</span>";
				}
			}
		});
	});
});
