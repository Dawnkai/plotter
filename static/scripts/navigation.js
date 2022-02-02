// Redirections to respective pages when the user clicks on buttons
// Allows for custom behavior more than just <a href=#/>
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
});
