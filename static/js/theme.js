(function($) {
    'use strict';
	
	// Mobile Menu
    $('.mobile-menu nav').meanmenu({
        meanScreenWidth: "991",
        meanMenuContainer: ".mobile-menu",
        meanMenuOpen: "<span></span> <span></span> <span></span>",
        onePage: false,
    });	

        //======< Accordion Tab >======
            $(".accordion > li:eq(0) a").addClass("active").next().slideDown();

            $(".accordion a").click(function (j) {
                var dropDown = $(this).closest("li").find("p");

                $(this).closest(".accordion").find("p").not(dropDown).slideUp();

                if ($(this).hasClass("active")) {
                    $(this).removeClass("active");
                } else {
                    $(this).closest(".accordion").find("a.active").removeClass("active");
                    $(this).addClass("active");
                }

                dropDown.stop(false, true).slideToggle();

                j.preventDefault();
            });
    // sticky
    var wind = $(window);
    var sticky = $('#sticky-header');
    wind.on('scroll', function () {
        var scroll = wind.scrollTop();
        if (scroll < 100) {
            sticky.removeClass('sticky');
        } else {
            sticky.addClass('sticky');
        }
    });

    var stickyHeaderText1 = $('#sticky-header-text1');
    wind.on('scroll', function () {
        var scroll = wind.scrollTop();
        if (scroll < 100) {
            stickyHeaderText1.removeClass('sticky-header-text');
        } else {
            stickyHeaderText1.addClass('sticky-header-text');
        }
    });

    var stickyHeaderText2 = $('#sticky-header-text2');
    wind.on('scroll', function () {
        var scroll = wind.scrollTop();
        if (scroll < 100) {
            stickyHeaderText2.removeClass('sticky-header-text');
        } else {
            stickyHeaderText2.addClass('sticky-header-text');
        }
    });

    var stickyHeaderText3 = $('#sticky-header-text3');
    wind.on('scroll', function () {
        var scroll = wind.scrollTop();
        if (scroll < 100) {
            stickyHeaderText3.removeClass('sticky-header-text');
        } else {
            stickyHeaderText3.addClass('sticky-header-text');
        }
    });

    var stickyHeaderText4 = $('#sticky-header-text4');
    wind.on('scroll', function () {
        var scroll = wind.scrollTop();
        if (scroll < 100) {
            stickyHeaderText4.removeClass('sticky-header-text');
        } else {
            stickyHeaderText4.addClass('sticky-header-text');
        }
    });
     //Header Search
    if($('.search-box-outer').length) {
        $('.search-box-outer').on('click', function() {
            $('body').addClass('search-active');
        });
        $('.close-search').on('click', function() {
            $('body').removeClass('search-active');
        });
    }
    // animate
    new WOW().init();

    // Loder  //
    $(function () {
      $('body').addClass('loaded');
    });

         // slider_list 
    $('.slider_list').owlCarousel({
        loop: true,
        autoplay: true,
        autoplayTimeout: 10000,
        dots: false,
        nav: false,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 1
            },
            1000: {
                items: 1
            },
            1920: {
                items: 1
            }
        }
    }) 

     // Case Study Active
    $('.testi_list1').owlCarousel({
        loop: true,
        autoplay: true,
        autoplayTimeout: 10000,
        dots: false,
        nav: false,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 2
            },
            1000: {
                items: 2
            },
            1920: {
                items: 2
            }
        }
    }) 

    // testimonial Active
    $('.testi-list2').owlCarousel({
         animateOut: 'slideOutDown',
         animateIn: 'zoomIn',
         smartSpeed: 50,
        loop: true,
        autoplay:true,
        autoplayTimeout:2000,
        dots: false,
        nav: false,
        navText: ["<i class='fas fa-angle-double-left''></i>", "<i class='fas fa-angle-double-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 1
            },
            1000: {
                items: 1
            },
            1920: {
                items: 1
            }
        }
    })  

    // testimonial Active
    $('.testi-list3').owlCarousel({
        loop: true,
        autoplay: true,
        autoplayTimeout: 10000,
        dots: false,
        nav: false,
        navText: ["<i class='fas fa-angle-double-left''></i>", "<i class='fa fa-long-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            992: {
                items: 2
            },
            1000: {
                items: 2
            },
             1500: {
                items: 2
            },
            1920: {
                items: 2
            }
        }
    })  

    // Brand list
    $('.brand-list').owlCarousel({
        loop: true,
        autoplay: true,
        autoplayTimeout: 10000,
        dots: false,
        nav:false,
        navText: ["<i class='bi bi-arrow-left''></i>", "<i class='bi bi-arrow-right''></i>"],
        responsive: {
            0: {
                items: 1
            },
            480: {
                items:2
            },
            600: {
                items: 3
            },
            768: {
                items: 4
            },
             992: {
                items: 5
            },
            1920: {
                items: 5
            }
        }
    })  

	/*---------------------
    WOW active js 
    --------------------- */
    new WOW().init();

    // counterUp
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });

    /* Product-load Isotope  */
    $('.image_load').imagesLoaded(function() {

        if ($.fn.isotope) {

            var $product = $('.image_load');

            $product.isotope({

                itemSelector: '.grid-item',

                filter: '*',

                resizesContainer: true,

                layoutMode: 'masonry',

                transitionDuration: '0.8s'

            });
            $('.menu-filtering li').on('click', function() {

                $('.menu-filtering li').removeClass('current_menu_item');

                $(this).addClass('current_menu_item');

                var selector = $(this).attr('data-filter');

                $product.isotope({

                    filter: selector,

                });

            });

        };

    });
	
	 // Venubox

    $('.venobox').venobox({

        numeratio: true,

        infinigall: true

    });
	/*--------------------------
     scrollUp
    ---------------------------- */
    $.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    })

        $(".skills").addClass("active")
        $(".skills .skill .skill-bar span").each(function() {
           $(this).animate({
              "width": $(this).parent().attr("data-bar") + "%"
           }, 1000);
           $(this).append('<b>' + $(this).parent().attr("data-bar") + '%</b>');
        });
        setTimeout(function() {
           $(".skills .skill .skill-bar span b").animate({"opacity":"1"},1000);
        }, 2000);


        <!--jave script -->
        
        $(window).on('scroll', function () {
            var scrolled = $(window).scrollTop();
            if (scrolled > 300) $('.go-top').addClass('active');
            if (scrolled < 300) $('.go-top').removeClass('active');
        });

        $('.go-top').on('click', function () {
            $("html, body").animate({
                scrollTop: "0"
            }, 1200);
        });
        
        <!-- quantity js--> 
            const plus= document.querySelector(".plus"),
            minus= document.querySelector(".minus"),
            num= document.querySelector(".num");
            let a = 1;
            plus.addEventListener("click", ()=>{
                a++;
                a = (a <10 )? "0" + a : a;
                num.innerText = a;
                console.log("a")
            });
            minus.addEventListener("click", ()=>{
                if(a > 1){
                    a--;
                    a = (a <10 )? "0" + a : a;
                     num.innerText = a;
                }
            });

    
})(jQuery);