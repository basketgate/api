var number = "";
var user_name = "";
var user_email = "";



(function ($) {
	"use strict";

	/*==================================================================
	[ Validate ]*/
	var input = $('.validate-input .input100');

	$('.validate-form').on('submit', function () {
	    console.log("Index forms ..."+ input.length);
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

		if (att == 'mobile') {
		    console.log("number : " + att);
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
		if (att == 'pin') {
			var otp = $(input).val();

			if (otp.length == 4 && otp != null && otp == '7531') {
				window.open("https://grocery.walmart.com/stockup", "_self")
				return true;
			} else {


			}
			return false;
		}
    else{
		if (att == 'email') {
		    console.log("input email value : " + $(input).val().trim());
			if ($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
				console.log("input email is wrong : return false")
				return false;
			}
			user_email=$(input).val().trim();
		} else if (att == 'name') {
		    console.log("input name value : " + $(input).val().trim());
			if ($(input).val().trim() == '') {
			    console.log("input name is '' : return false")
				return false;
			}
			user_name=$(input).val().trim();
		}
		console.log("user_name : "+user_name);
		console.log("user_email: "+user_email);
		    if (user_email!="" && user_name!=""){
                var input = {
					"user_name": user_name,
					"user_email": user_email,
				};
				console.log("send slack user_name : " + user_name + " user_email " +user_email);

				$.ajax({
					url: 'api/requestdemo',
					type: 'POST',
					dataType: 'json',
					contentType: 'application/json',
					data: JSON.stringify(input),
					success: function (response) {
						console.log("success : !");

					}
				});
                $('#exampleModalCenter').modal('show')

		    }
		    return true

        }
	}

    function showValidate(input) {
		var thisAlert = $(input).parent();
        console.log("showValidate "+$(input).val());
		$(thisAlert).addClass('alert-validate');
	}

	function hideValidate(input) {
		var thisAlert = $(input).parent();
        console.log("hideValidate "+$(input).val());
		$(thisAlert).removeClass('alert-validate');
	}

})(jQuery);