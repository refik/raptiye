 // raptiye
 // Copyright (C) 2009  Alper KANAT <alperkanat@raptiye.org>
 // 
 // This program is free software: you can redistribute it and/or modify
 // it under the terms of the GNU General Public License as published by
 // the Free Software Foundation, either version 3 of the License, or
 // (at your option) any later version.
 // 
 // This program is distributed in the hope that it will be useful,
 // but WITHOUT ANY WARRANTY; without even the implied warranty of
 // MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 // GNU General Public License for more details.
 // 
 // You should have received a copy of the GNU General Public License
 // along with this program. If not, see <http://www.gnu.org/licenses/>.
 //

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
	// all links are styled with jquery tooltip
	$("a").tooltip({
		positionLeft: true,
		track: true,
		fade: 250,
		fixPNG: true,
		showURL: false
	})
	// this part is for styling the colorized code boxes
	$(".code[id]").css({
		"padding": "8px 5px 8px 5px",
		"border-top": "1px solid #CCCCCC",
		"border-bottom": "1px solid #CCCCCC"
	})
});

