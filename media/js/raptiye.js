debugging = true;

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
		if (resp.status == "1") {
			showStatusMessage(resp);
		} else {
			// replace the captcha
			debug("replacing captcha with: " + resp.captcha);
			$("#captcha_image").attr("src", resp.captcha);
			$("#captcha_id").val($("#captcha_image").attr('src').split('/')[3].split('.')[0]);
		}
	}, "json");
}