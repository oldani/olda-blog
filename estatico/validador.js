var wating= '<div class="row"><img class="img-responsive center-block"src="estatico/default.gif">\
<p class="blinking text-center">Loging in...</p></div>'

var error= '<div class="row">\
				<div class="text-center">\
					<i class="fa fa-close fa-5x fa-error"></i>\
				</div>\
				<p class="text-center text-danger">Error!</p>\
			</div>\
			<div class="row">\
				<div class="col-xs-8 col-sm-6 col-xs-offset-2 col-sm-offset-3">\
					<div class="alert alert-danger">\
						<p class="text-center">'

var cerrarError= ".</p></div></div></div>\
				  <div class='row'>\
					 <button type='button' class='btn btn-info center-block'>\
					 Try Again</button>\
				  </div>"

var valid= "Please enter a valid "

var success= '<div class="row">\
				<div class="text-center">\
					<i class="fa fa-check fa-5x fa-success"></i>\
				</div>\
				<p class="text-center text-success">Success!</p>\
			</div>\
			<div class="row">\
				<div class="col-xs-8 col-sm-6 col-xs-offset-2 col-sm-offset-3">\
					<div class="alert alert-success">\
						<p class="text-center">Welcome, '

var cerrarSuccess= '</p></div></div></div>'


var makeBlink={
	blinker: function() {
		var $watingDom= $(".blinking");
		$watingDom.fadeOut(300);
		$watingDom.fadeIn(300);
	}

};
var intervalo= setInterval(makeBlink.blinker, 1000);

var validarSignUp= function(){
	$("#signupForm")
				
				.formValidation({
					framework:"bootstrap",
					err: {
						container: 'popover'
					},

					icon: {
						valid: 'glyphicon glyphicon-ok',
						invalid: 'glyphicon glyphicon-remove',
						validating: 'glyphicon glyphicon-refresh'
					},
					fields: {
						username: {
							validators: {
								notEmpty: {
									message:"Please enter a username"
								},
								regexp: {
									regexp:/^[\w\-\.]{4,12}$/,
									message: "The username most be more than 4 and less than 12 characters long"
								}
							}
						},
						password: {
							validators: {
								notEmpty: {
									message:"Please enter a password"
								},
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
					e.preventDefault();
					var $form= $(e.target);
					var modal= $form.children(".modal-body");
					var datos= $form.serialize();
					var modalClonado= modal.children(".row").clone();
					
					
					
					$.ajax({
						url: $form.attr("action"),
						method: "POST",
						beforeSend: function(){
							modal.html(wating);
							makeBlink.blinker();
							intervalo;
						},
						data: datos,
						dataType: "json",
						success: function(data) {
							if ("user" in data) {
								modal.html(error+data.user+cerrarError);

							} else if ("badData" in data) {
								var built= $.map(data.errores, function(valor){
									var errores= " "+valor
									return errores
								});
								modal.html(error+valid+built+ cerrarError);	
							} else {
								modal.html(success+data.username+"!"+cerrarSuccess);
								window.location.reload();
							};
						}
					});
					$form.on("click", "button", function(){
						modal.html(modalClonado);	
						$form.find("#submit")
								.removeClass("disabled")
								.prop("disabled", false);
					});	
				});
				
				
}