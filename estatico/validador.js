var wating= '<div class="row"><img class="img-responsive center-block"src="estatico/default.gif">\
<p class="blinking text-center">Loging in...</p></div>'


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
					$.ajax({
						url: $form.attr("action"),
						method: "POST",
						beforeSend: function(){
							// var form= $('#signupForm').children(".modal-body");
							modal.children().remove();
							modal.html(wating);
							function blinker() {
								$('.blinking').fadeOut(300);
								$('.blinking').fadeIn(300);
							};
							setInterval(blinker, 1000);
			


						}

					});
				});	
				
}