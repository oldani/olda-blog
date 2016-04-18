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

var $ajaxFun= function(data, successFun){
    $.ajax({
        url: "/dashboard",
        method: "POST",
        data: data,
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
    
    $(".status").on("click", function(){
        var $this, $postRow, postId, successFun, data,
            $habilitarPostClass;

        $this= $(this);
        $postRow= $this.closest(".x_panel")
        postId= $postRow.find("h2>a").attr("href");
        $habilitarPostClass= $this.hasClass("habilitar-post");

        if ($habilitarPostClass){
            successFun= successStatus.habilitarPost($postRow, $this)
            data= "status=true"+"&postid="+postId;

        } else {
            successFun= successStatus.deshabilitarPost($postRow, $this);
            data= "status=false"+"&postid="+postId;
        }

        $ajaxFun(data, successFun);
    });
};


