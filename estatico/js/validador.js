var opciones= {
	framework: "bootstrap",
	excluido: ":disabled",
	iconos: {
		valid: 'glyphicon glyphicon-ok',
		invalid: 'glyphicon glyphicon-remove',
		validating: 'glyphicon glyphicon-refresh'
	},
	vacioUsername: {
				message:"Please enter a username"
	},
	vacioPw: {
		message:"Please enter a password"
	},

};

var submitEvent = {
	successSign: function(data, modal) {
		if ("user" in data) {
			$("#wating").remove()
			modal.append(error+data.user+cerrarError);

		} else if ("badData" in data) {
			var built= $.map(data.errores, function(valor){
				var errores= " "+valor
				return errores
			});
			$("#wating").remove()
			modal.append(error+valid+built+ cerrarError);	
		} else {
			modal.html(success+data.username+"!"+cerrarSuccess);
			window.location.reload();
		};
	},

	successLog: function(data, modal){
		if ("error" in data) {
			$("#wating").remove();
			modal.append(error+data.error+cerrarError);
		} else {
			modal.html(success+data.username+cerrarSuccess);
			window.location.reload();
		};
	},
	ajaxObj: function(obj, e){
		e.preventDefault();
		
		var $form= $(e.target);
		var modal= $form.children(".modal-body");
		var datos= $form.serialize();
		var modalRows= modal.children(".row");

		$.ajax({
			url: $form.attr("action"),
			method: "POST",
			beforeSend: function(){
				modalRows.hide();
				modal.append(wating);
				makeBlink.blinker();
				intervalo;
			},
			data: datos,
			dataType: "json",
			success: function(data){
				
				if (obj=="login") {
					submitEvent.successLog(data, modal);
				} else {
					submitEvent.successSign(data, modal);
				};
			}
		});
		$form.on("click", "button", function(){
			$("#error").remove();
			modalRows.show();
			$form.find("#submitLogin")
								.removeClass("disabled")
								.prop("disabled", false);
		});
	},


}

var validarForms= function(){
	$("#signupForm")
				
				.formValidation({
					framework:opciones.framework,
					excluded: opciones.excluido,

					icon: opciones.iconos,
					fields: {
						username: {
							validators: {
								notEmpty: opciones.vacioUsername,
								regexp: {
									regexp:/^[\w\-\.]{4,12}$/,
									message: "The username most be more than 4 and less than 12 characters long"
								}
							}
						},
						password: {
							validators: {
								notEmpty: opciones.vacioPw,
								regexp: {
									regexp:/(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])\S{6,}$/,
									message:"Your Password must have at least of 1 Lowercase, 1 Uppercase letters and 1 number"
								}
							}
						},
						verify: {
							validators: {
								notEmpty:{
									message:"Please verify your password"
								},
								identical: {
									field: "password",
									message: "Your password did not match"
								}
							}
						},
						correo: {
							validators: {
								notEmpty:{
									message:"An email is required"
								},
								regexp: {
									regexp: /^[\S]+@[\S]+\.[\S]+$/,
									message:"Please enter a valid Email"
								}
							}
						}	
					}	
				})
				.on("success.form.fv", function(e){
					submitEvent.ajaxObj("sign", e);	
				});
	$("#loginForm")
				.formValidation({
					framework: opciones.framework,
					icon: opciones.iconos,
					excluded: opciones.excluido,
					fields:{
						username:{
							validators:{
								notEmpty:opciones.vacioUsername
							}
						},
						password:{
							validators:{
								notEmpty:opciones.vacioPw
							}
						}
					}
				})
				.on("success.form.fv", function(e){
					submitEvent.ajaxObj("login", e);
				});				
}