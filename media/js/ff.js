// Copyright (C)  Alper KANAT  <alperkanat@raptiye.org>
// this site does not support internet explorer
// use better browsers like firefox, safari, opera
// and even chrome which is in beta status..

var normalMessage = "neden?"
var hoveredMessage = "tıkla!"
var whyFirefox = "neden firefox kullanmalısınız?"
var reasons = "<strong>1)</strong> Internet Explorer standartlara uymayıp kendi standartlarını empoze ediyor!<br><br>"
reasons += "<strong>2)</strong> Firefox, açık kaynak kodlu, özgür bir yazılım; dolayısıyla daha güvenli!<br><br>"
reasons += "<strong>3)</strong> Bellek kullanımı sebebiyle Firefox'u beğenmiyorsanız Safari, Opera, Google Chrome gibi alternatifleri kullanmaktan çekinmeyin. Yeter ki Internet Explorer kullanmayın..<br><br>"
reasons += "<strong>4)</strong> Yüzlerce, hatta binlerce eklentisiyle Firefox internet deneyiminizi sonsuza dek değiştirebilir..<br><br>"
reasons += "<strong>5)</strong> Geliştiriciler olarak; daha kaliteli yazılımlar üretmek için uğraşmak yerine standart dışı uygulamalar nedeniyle gereksiz yere uğraşmak ve kötü kod yazmak zorunda kalmak istemiyoruz!<br><br>"
reasons += "<strong>6)</strong> Alışkanlıklarınız zorunluluklarınızdır! Farklı alternatifleri tanımak ise zenginleştirir ve özgürleştirir.<br><br>"
reasons += "<strong>7)</strong> Internet Explorer 6.0, transparan PNG dosyalarını desteklemiyor!<br><br>"
reasons += "<strong>8)</strong> Microsoft bile Internet Explorer 6.0'dan desteğini çekti; siz neden çekmeyesiniz?<br><br>"
reasons += "<strong>9)</strong> Microsoft, Internet Explorer 8 Beta2 ile ağ standartlarını yakalamaya çalışıyor. Zaten bu teknolojileri kullanan tarayıcılar varken neden geriden gelesiniz ki?<br><br>"
reasons += "İşte tam da bu sebeplerden dolayı:<br><br>"
var footer = "Lütfen Internet Explorer kullanmayın ve kullandırtmayın!"

$(document).ready(function() {
	$("<div id='ff_ad_box'>").append(
		$("<h2>").text(whyFirefox)
	).css({
		"display": "none"
	}).append(
		$("<br>")
	).append(
		$("<span>").css({
			"font-size": "12px"
		}).html(reasons)
	).append(
		$("<div>").css({
			"text-align": "center",
			"font-size": "18px",
			"font-weight": "bold"
		}).text(footer)
	).appendTo($(document.body))
	
	$("<div id='ff_ad_container'>").append(
		$("<div id='ff_ad_container_left'>").css({
			"float": "left",
			"margin-top": "14px",
			"margin-right": "15px",
			"font-size": "22px",
			"font-weight": "bold"
		}).text(normalMessage)
	).append(
		$("<div id='ff_ad_container_right'>").css({
			"float": "right"
		}).append(
			$("<img>").attr({
				"src": "/media/images/ff_horizontal.png",
				"alt": "firefox logo",
				"title": "bilgi almak için tıklayın.."
			}).css("border", 0)
		)
	).css({
		"position": "absolute",
		"top": "20px",
		"right": "20px"
	}).mouseover(function() {
		$("#ff_ad_container_left").text(hoveredMessage)
	}).mouseout(function() {
		$("#ff_ad_container_left").text(normalMessage)
	}).click(function () {
		iBox.show($("#ff_ad_box").html(), "", {"width": "450", "height": "540"})
	}).appendTo($(document.body))
})