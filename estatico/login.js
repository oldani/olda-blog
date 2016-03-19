
var regexPw= /(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])\S{6,}$/;

var validarN= function(){procesarSolicitud("#username",/^[\w]{4,12}$/);
};

var validarPw = function(){procesarSolicitud("#pass", regexPw);
};

var confirmarPw= function() {procesarSolicitud("#passV", regexPw);
};

var validarMail= function() {procesarSolicitud("#correo", /^[\S]+@[\S]+\.[\S]+$/);
};

function procesarSolicitud(sel, regex) {
	$(sel).blur(function(){
		var valor, formGroup 
		valor= $(this).val();
		formGroup= $(this).closest(".form-group");
		

		if (valor.match(regex)) {

			if (sel=="#passV" && valor!= $("#pass").val()) {
				$(formGroup).addClass("has-error");
			} else {
				$(formGroup).removeClass("has-error");
				$(formGroup).addClass("has-success");
			};
		} else {
			$(formGroup).addClass("has-error")
		};

	});
}

