var wating= '<div class="row" id="wating"><img class="img-responsive center-block"src="estatico/img/default.gif">\
<p class="blinking text-center">Loging in...</p></div>'

var error= '<div id="error"><div class="row">\
				<div class="text-center">\
					<i class="fa fa-close fa-5x fa-error"></i>\
				</div>\
				<p class="text-center text-danger">Error!</p>\
			</div>\
			<div class="row">\
				<div class="col-xs-8 col-sm-6 col-xs-offset-2 col-sm-offset-3">\
					<div class="alert alert-danger">\
						<p class="text-center">';

var cerrarError= ".</p></div></div></div>\
				  <div class='row'>\
					 <button type='button' class='btn btn-info center-block'>\
					 Try Again</button>\
				  </div></div>";

var valid= "Please enter a valid ";

var success= '<div class="row">\
				<div class="text-center">\
					<i class="fa fa-check fa-5x fa-success"></i>\
				</div>\
				<p class="text-center text-success">Success!</p>\
			</div>\
			<div class="row">\
				<div class="col-xs-8 col-sm-6 col-xs-offset-2 col-sm-offset-3">\
					<div class="alert alert-success">\
						<p class="text-center">Welcome, ';

var cerrarSuccess= '</p></div></div></div>';

var makeBlink={
	blinker: function() {
		var $watingDom= $(".blinking");
		$watingDom.fadeOut(300);
		$watingDom.fadeIn(300);
	}

};
var intervalo= setInterval(makeBlink.blinker, 1000);

// error para comentarios
var errorComentario, cerrarComentario
errorComentario= //'<div class="row">\
					//'<div class="col-xs-10 col-sm-5 col-md-4 col-lg-4">\
						'<div class="alert alert-danger alert-dismissible" role=" alert" \
							style="margin-top:10px">\
							<button type="button" class="close" data-dismiss="alert" aria-label="Close">\
								<span aria-hidden="true">&times;</span>\
							</button>';
cerrarComentario='</div>';//</div>';//</div>';

// comfirm delte message

var confirmDelete= '<div class="row" style="padding: 40px 20px;">\
    					<div class="col-xs-12">\
      						<h5 class="text-center">\
      							Are you sure you want to delete this post?\
      						</h5>\
    					</div>\
  						<div class="col-xs-12 text-center">\
      						<button class="btn btn-danger btn-circle">Yes\
      						</button>\
      						<button class="btn btn-default btn-circle">No\
      						</button>\
    					</div>\
  					</div>'