$(document).ready(function() {
	// popup login/register window
	$(".login_button").on("click", function(event) {
		console.log("jere");
		event.preventDefault();
		$(".login_arrow").toggle();
		$("#signin").toggle();
		$("input#login").val("");
		$("input#password").val("");
	});

	// sets last clicked section active 
	$("nav li.left a:not(.active)").on("click", function() {
		$("nav li.left").find("a.active").removeClass("active");
		$(this).addClass("active");
	});
	$("#new_post i.fa-camera").on("click", function(e) {
		e.stopPropagation();
		$("input.foto").click();
	});
	// $("#new_post textarea").focusin(function() {
	// 	new_post_rollout();
	// });
	// $("#new_post textarea").focusout(function(e) {
	// 	new_post_rollin();
	// });
	$("#new_post textarea").keyup(function() {
		char_count();
	});
	$("#new_post i.fa-pencil-square-o").on("click", create_post);
	// $("#recent p.author").on("mouseover", function() {
	// 	$(this).css({"color": "#1da1f2",
	//                  "text-decoration": "underline"});
	// });
});

var create_post = function() {
	var url = $("div.buttons_post input.send_post").attr("action");
	var data = $("#new_post textarea").val();
	$.ajax({
		method: "post",
		url: url,
		data: {data: data},
		success: function(response) {
			$("#recent").prepend("<div class='post'>" + "<p>" + response["user"] + "</p>" + response['body'] + "</div>");
		}
	})
	$("#new_post textarea").val("");
	// new_post_rollin();
	$("#new_post span.counter").html("140");
}

// var new_post_rollout = function() {
// 	$("#new_post").css({"height": "106px"});
// 	$("#new_post textarea").attr("rows", "4");
// 	$("div.buttons_post textarea").css({"height": "65px"});
// 	$("div.buttons_post").css({"display": "inline-block"});
// 	$("#recent").css({"top": "126px"});
// 	$("div.post").css({"top": "126px"});
// }
// var new_post_rollin = function() {
// 	if ($("#new_post textarea").val().length < 1) {
// 		$("#new_post").css({"height": "20px"});
// 		$("#new_post textarea").attr("rows", "1");
// 		$("#new_post textarea").val("");
// 		$("div.buttons_post textarea").css({"height": "auto"});
// 		$("div.buttons_post").css({"display": "none"});
// 		$("#recent").css({"top": "40px"});
// 		$("div.post").css({"top": "40px"});
// 	}
// }
var char_count = function() {
	var max = 140;
	var counter = $("#new_post span.counter");
	var len = $("#new_post textarea").val().length;
	counter.html(max - len);
	if (len > 0) {
		$("#new_post i.fa-pencil-square-o").css({"opacity": "1",
												 "cursor": "pointer"});
	}
	
	else { 
		$("#new_post i.fa-pencil-square-o").css({"opacity": "0.5",
												 "cursor": "default"});
		$(this).blur();
	}
	if (max >= len) {
	 	counter.css({"color": "#666"});
	}
	if (max < len) {
		counter.css({"color": "red"});
		$("#new_post i.fa-pencil-square-o").css({"opacity": "0.5",
												 "cursor": "default"});
		var overflow = $("#new_post textarea").val().slice(max, len);
		$(this).blur();
	}
}