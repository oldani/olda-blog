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

// Panel toolbox Edit, Enable/Disable, Deletexff3
var $ajaxFun= function(data, successFun=null, before= null){
    console.log(before);
    $.ajax({
        url: "/dashboard",
        method: "POST",
        data: data,
        beforeSend: before,
        success: function(){
            successFun;
        }

    })
};

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

        $ajaxFun(data, successFun);
    });
};

var deleteAjaxFun= {
    beforeSend: function(){

    },
    successFun: function(){

    }
};

var deletePost= function(){
    $(".x_panel").on("click",".delete-post",function(){
        var $this= $(this);
        var $postRow= $this.closest(".x_panel");
        var postId= $postRow.find("h2>a").attr("href");
        var row
        var post= $postRow.fadeOut(function(){
            row= $(this).children().detach();
            $(this).hide().html(confirmDelete).fadeIn();
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
                    $(this).hide().html(row).fadeIn();
                });
                
            };
        });

    });
};