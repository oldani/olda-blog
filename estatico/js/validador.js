


var validarForms= function(){
	$("#signupForm")
				
				.formValidation({
					framework:"bootstrap",
					err: {
						container: 'popover'
					},
					excluded: ":disabled, :hidden, :not(:visible)",

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
	$("#loginForm")
				.formValidation({
					framework: "bootstrap",
					icon:{
						valid: "glyphicon glyphicon-ok",
						invalid: "glyphicon glyphicon-remove"
					},
					excluded:":hidden, :not(:visible), :disabled",
					fields:{
						username:{
							validators:{
								notEmpty:{
									message:"Please enter a username"
								}
							}
						},
						password:{
							validators:{
								notEmpty:{
									message:"Please enter a password"
								}
							}
						}
					}
				})
				.on("success.form.fv", function(e){
					e.preventDefault();
					var $form= $(e.target);
					var modal= $form.children(".modal-body");
					var data= $form.serialize();
					var modalClonado= modal.children(".row").clone();
					// var footer= $form.children(".modal-footer");
					// var footerClonado= footer.children(".btn").detach();

					$.ajax({
						url: $form.attr("action"),
						method:"POST",
						beforeSend: function(){
							modal.html(wating);
							makeBlink.blinker();
							intervalo;
							//footer.html("");
						},
						data:data,
						dataType: "json",
						success: function(data){
							if ("error" in data) {
								modal.html(error+data.error+cerrarError);
							} else {
								modal.html(success+data.username+cerrarSuccess);
								window.location.reload();
							};
						}

					});
					$form.on("click", "button", function(){
						modal.html(modalClonado);
						// footer.html(footerClonado);
						$form.find("#submitLogin")
											.removeClass("disabled")
											.prop("disabled", false);
					});
				});

				
				
}