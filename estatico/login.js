
var regexPw= /(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])\S{6,}$/;

var validarN= function(){procesarSolicitud("#usernameS",/^[\w]{4,12}$/);
};

var validarPw = function(){procesarSolicitud("#passS", regexPw);
};

var confirmarPw= function() {procesarSolicitud("#passVs", regexPw);
};

var validarMail= function() {procesarSolicitud("#correo", /^[\S]+@[\S]+\.[\S]+$/);
};

var usernameWrong, pwWrong, pwNotMatch, mailWrong

usernameWrong= "<span class=help-block>Your Username must have at least of 4 caracters</span>";
pwWrong= "<span class=help-block>Your Password must have at least of 1 Lowercase, 1 Uppercase letters and 1 number</span>";
pwNotMatch="<span class=help-block>Your Password did not match</span>";
mailWrong="<span class=help-block>Please enter a valid Email</span>";

var campos=0;
console.log(campos);

function procesarSolicitud(sel, regex) {
	var formGroup= $(sel).closest(".form-group");
	$(sel).keyup(function() {
		var valor= $(this).val();
		var errorMsg= $(formGroup).find("span").hasClass("help-block");
		if (valor.match(regex)) {
			if (sel=="#passVs" && valor!= $("#passS").val()) {
				if (!errorMsg) {
					$(formGroup).addClass("has-error");
					$(this).parent().after(pwNotMatch);
				};
			} else {
				$(formGroup).removeClass("has-error");
				$(formGroup).children(".help-block").remove();
				$(formGroup).addClass("has-success");
			};
		} else if (sel!="#passVs") {
			$(formGroup).removeClass("has-success");
			$(formGroup).addClass("has-error");
			if (sel=="#usernameS" && !errorMsg) {
				$(this).parent().after(usernameWrong);
			} else if (sel=="#passS" && !errorMsg) {
				$(this).parent().after(pwWrong)
			} else if (sel=="#correo" && !errorMsg) {
				$(this).parent().after(mailWrong);
			};
		};

		// var valido= $(formGroup).hasClass("has-success");
		// if (valido) {
		// 	campos+=1;
		// 	if(valido && campos>4){
		// 		campos-=1;
		// 	}
		// 	console.log(campos);
		// };

		// if (campos>=4) {
		// 	$("#submit").prop("disabled", false);
		// };
		
		
	});
	


}



