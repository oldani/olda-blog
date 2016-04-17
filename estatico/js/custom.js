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

