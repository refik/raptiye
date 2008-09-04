debugging = false;

function debug(msg) {
	if (debugging) {
		if (typeof console != "undefined") {
			console.log(msg);
		} else {
			alert(msg);
		}
	}
}

function toggleForm(layer) {
	if ($("#disableForm").val() == "0") {
		// form is enabled, disabling..
		$(layer + " :input").attr("disabled", true);
		$("#disableForm").val("1");
	} else {
		// form is disabled, enabling..
		$(layer + " :input").removeAttr("disabled");
		$("#disableForm").val("0");
	}
}

/**
 * creates a new captcha image and
 * returns its url
 */
function getNewCaptcha() {
	$.get("/comment/new_captcha/", "", function(resp) {
		if (resp.status) {
			showStatusMessage(resp);
		} else {
			// replace the captcha
			debug("replacing captcha with: " + resp.captcha);
			$("#captcha_image").attr("src", resp.captcha);
			$("#captcha_id").val($("#captcha_image").attr('src').split('/')[3].split('.')[0]);
		}
	}, "json");
}

$(function() {
	// fill search box
	$("#search_box").val("arama kutusu");
	$("#search_box").focus(function() {
		// clear the search box
		$("#search_box").val("");
		// set the font color to black
		$("#search_box").css("color", "black");
		// change the background
		$("#search").css("background", "transparent url(/media/images/search-active.png) top left no-repeat");
	});
	// blur = unfocus
	$("#search_box").blur(function() {
		// reinitialize the search box
		$("#search_box").val("arama kutusu");
		// set to font color to gray
		$("#search_box").css("color", "#b5b5b5");
		// change the background
		$("#search").css("background", "transparent url(/media/images/search.png) top left no-repeat");
	});
	$("#search_box").keydown(function(e) {
		if (e.keyCode == 13)
			$("#search_form").submit();
	});
});