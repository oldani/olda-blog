/**
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

// Sidebar
$(function () {
    var $BODY = $('body'),
        $SIDEBAR_MENU = $('#sidebar-menu'),
        $MENU_TOGGLE = $('#menu_toggle');
        
        $LEFT_COL = $('.left_col');

    

    $SIDEBAR_MENU.find('li').on('click', function(ev) {
        
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');

        } else {
            $SIDEBAR_MENU.find('li').removeClass('active');
            
            $(this).addClass('active');
           
        }

    });

    $MENU_TOGGLE.on('click', function() {
        if ($BODY.hasClass('nav-md')) {
            $BODY.removeClass('nav-md').addClass('nav-sm');
            $LEFT_COL.removeClass('scroll-view').removeAttr('style');
            
        } else {
            $BODY.removeClass('nav-sm').addClass('nav-md');
        }
    });

    
});


// Right column height
$(".right_col").css("min-height", $(window).height());
$(window).resize(function () {
    $(".right_col").css("min-height", $(window).height());
});

// Sidebar finish

//Post Page
// Panel toolbox Edit, Enable/Disable, Deletexff3
var $ajaxFun= function(opciones){
    $.ajax({
        url: opciones.url,
        method: opciones.metodo,
        data: opciones.data,
        dataType: "json",
        beforeSend:function(){
            opciones.before;
        },
        success: function(data){
            opciones.successFun(data);
        }

    })
};

//Habilitar y Deshabilitar Post
var successStatus= {
    habilitarPost: function($postRow, $this){
        $postRow.removeClass("deshabilitar");
        $this
            .removeClass("habilitar-post")
            .children("span").text("Disable");
    },
    deshabilitarPost: function($postRow, $this){
        $postRow.addClass("deshabilitar");
        $this
            .addClass("habilitar-post")
            .children("span").text("Enable");
    }
}

var cambiarStatus= function(){
    
    $(".x_panel").on("click",".status", function(){
        var $this, $postRow, postId, successFun, data,
            $habilitarPostClass;

        $this= $(this);
        $postRow= $this.closest(".x_panel")
        postId= $postRow.find("h2>a").attr("href");
        $habilitarPostClass= $this.hasClass("habilitar-post");
        data= "accion=cambiarEstado&postid="+postId;

        if ($habilitarPostClass){
            successFun= successStatus.habilitarPost($postRow, $this)
            data= data + "&status=true";

        } else {
            successFun= successStatus.deshabilitarPost($postRow, $this);
            data= data + "&status=false";
        }

        var opciones= {data:data, successFun:successFun, url:"/dashboard",
                        metodo:"POST"}
        $ajaxFun(opciones);
    });
};

//Eliminar un post
var deletePost= function(){
    $(".x_panel").on("click",".delete-post",function(){
        var $this= $(this);
        var $postRow= $this.closest(".x_panel");
        var postId= $postRow.find("h2>a").attr("href");
        var row
        var post= $postRow.slideUp("fast", function(){
            row= $(this).children().detach();
            $(this).hide().html(confirmDelete).slideDown("fast");
            return row
        });


        $($postRow).on("click", "button", function(){
            if ($(this).hasClass("btn-danger")){
                var data= "accion=delete&postid="+postId;
                $ajaxFun(data);
                $postRow.closest(".row").fadeOut(function(){
                    $(this).remove();
                });
            } else {
                $postRow.fadeOut(function(){
                    $(this).hide().html(row).slideDown("fast");
                });
                
            };
        });

    });
};

//Editar un post
var editarPost= function(){
    $(".x_panel").on("click",".editar",function(){
        console.log("hi");
        var $this= $(this);
        var $postRow= $this.closest(".x_panel");
        var postId= $postRow.find("h2>a").attr("href");
        var opciones= {url: "/edit/"+postId, method:"GET",
            before:ajaxObjs.before(), successFun:ajaxObjs.successFun};
        $ajaxFun(opciones)
    });

};

var submitChange= function(){
    $("#formEditar").submit(function(e){
        e.preventDefault();
        tinyMCE.triggerSave();
        var $this, $field;
        $this= $(this);
        data= $this.serialize();
        $field= $this.closest("fieldset");

        $.ajax({
            url: $this.attr("action"),
            method: "POST",
            data:data,
            dataType: "json",
            beforeSend: function(){
                ajaxObjs.before();
            },
            success: function(data){
                window.location.reload();
            }
        });
    });
};


//SideBar page via ajax, ya sea post, tables o charts
var ajaxObjs= {
    before: function(){
        $(".right_col")
                    .addClass("cargando")
                    .children().remove();
    },
    successFun: function(data){
        $(".right_col")
                    .removeClass("cargando")
                    .hide().html(data).fadeIn();
    }
};

var sideBar= function(){

    $("#sidebar-menu").on("click",".sideBar-ajax", function(){
        var $this, data, opciones;
        $this= $(this);
        data= "page="+ $this.data("request");
        opciones= {url:"/estadisticas", metodo:"GET", data:data,
                    before:ajaxObjs.before(), successFun:ajaxObjs.successFun}
        
        $ajaxFun(opciones);
    });
};