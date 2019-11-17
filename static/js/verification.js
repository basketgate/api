function sendOTP() {
	$(".error").html("").hide();
	var number = $("#mobile").val();
	if (number.length == 10 && number != null) {
		var input = {
			"mobile_number" : number,
		};
		$.ajax({
			url : 'api/sendsms',
			type : 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data : JSON.stringify(input),
			success : function(response) {
				//$(".container").html(response);
				$(".container").load('verification-form.html')
			}
		});
	} else {
		$(".error").html('Please enter a valid number!')
		$(".error").show();
	}
}

function verifyOTP() {
	$(".error").html("").hide();
	$(".success").html("").hide();
	var otp = $("#mobileOtp").val();

	if (otp.length == 4 && otp != null && otp=='7531') {
		window.open("https://grocery.walmart.com/","_self")
	} else {

		$(".error").html('You have entered wrong OTP.')
		$(".error").show();
	}
}