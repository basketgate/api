var number = "";
(function ($) {
	"use strict";

	/*==================================================================
	[ Validate ]*/
	var input = $('.validate-input .input100');

	$('.validate-form').on('submit', function () {
	console.log("Index forms ...");
		var check = true;

		for (var i = 0; i < input.length; i++) {
			if (validate(input[i]) == false) {
				showValidate(input[i]);
				check = false;
			}
		}

		return false;
	});


	$('.validate-form .input100').each(function () {
		$(this).focus(function () {
			hideValidate(this);
		});
	});

	function validate(input) {
	var att=$(input).attr('name')
	console.log("number : " + att);
		if ($(input).attr('name') == 'mobile') {
			number = $(input).val();

			if (number.length == 10 && number != null) {
				var input = {
					"mobile_number": number,
				};
				console.log("number : " + number);
				$.ajax({
					url: 'api/sendsms',
					type: 'POST',
					dataType: 'json',
					contentType: 'application/json',
					data: JSON.stringify(input),
					success: function (response) {
						console.log("success : !");

						//$(".container").html(response);
						$("#container").load('pin-form-new-skin')
					}
				});
				console.log("return true : !");
				return true;
			} else {
				console.log("return false2 : !");


			}
			return false;
		}
    else
		if ($(input).attr('name') == 'pin') {
			var otp = $(input).val();

			if (otp.length == 4 && otp != null && otp == '7531') {
				window.open("https://grocery.walmart.com/stockup", "_self")
				return true;
			} else {


			}
			return false;
		}
return false;
		if ($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
			if ($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
				return false;
			}
		} else {
			if ($(input).val().trim() == '') {
				return false;
			}
		}
	}

	function showValidate(input) {
		var thisAlert = $(input).parent();

		$(thisAlert).addClass('alert-validate');
	}

	function hideValidate(input) {
		var thisAlert = $(input).parent();

		$(thisAlert).removeClass('alert-validate');
	}

})(jQuery);