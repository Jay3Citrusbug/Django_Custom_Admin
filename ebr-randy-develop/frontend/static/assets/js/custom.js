// document.querySelectorAll('a[href^="#"]').forEach(anchor => {
//     anchor.addEventListener('click', function (e) {
//         e.preventDefault();

//         document.querySelector(this.getAttribute('href')).scrollIntoView({
//             behavior: 'smooth'
//         });
//     });
// });
var $ = $.noConflict();
$('#youtubevideowrapper').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    dots: false,
    // navText: ["« Prev Video","Next Video »"],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        }
    }
});
$('#youtubevideowrappergallry').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    dots: false,
    // navText: ["« Prev Video","Next Video »"],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        }
    }
});
$('.product-card-item .owl-carousel.product-img-slider').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    dots: false,
    // mouseDrag: false,
    // touchDrag: false,
    // pullDrag: false,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        }
    }
});
// $(window).on('beforeunload', function(){
//   $(window).scrollTop(0);
// });
$(window).on('beforeunload', function() {
  $('body').hide();
  alert("ok");
  $(window).scrollTop(0);
  // $("html, body").animate({ scrollTop: 0 }); 
});

$(document).keydown(function(event) { 
  if (event.keyCode == 27) { 
    $('.modal').modal('hide');
    $('[data-toggle="popover"]').popover('hide');
    $("body").removeClass("body-dropdown-top");
    $("body").removeClass("body-dropdown-bottom");
    // $(this).popover('hide');
  }
});

// $(function() {
//   $(".editor-richText-box").on("click", function(a) {
//     $(this).addClass("focus");
//     a.stopPropagation()
//   });
//   $(document).on("click", function(a) {
//     if ($(a.target).is(".editor-richText-box") === false) {
//       $(".editor-richText-box").removeClass("focus");
//     }
//   });
// });


$(document).ready(function(){

    // $("iframe").load(function() {
    //     $("body").click(function() {
    //       $("iframe").css('border' , '#000 1px solid');
    //     });
    // });


    setTimeout(function(){
     $('.cookie_wrapper').show();
    },1000);
  
    $("html, body").animate({ scrollTop: 0 }); 
    
    // $("a.btn.theme-btn.helpfulbtn").click(function(){
    //   $(this).toggleClass("helpbtnactive");
    //   $(this).parents("ul.comment_btns").parent(".comment_inner").parent(".cm_right").parent(".comment_head").siblings(".download_box").find(".icon").toggleClass("active-icon");
    // });
    //  $(".download_box .icon svg").click(function(){
    //   $(this).parents(".icon").parents(".download_box").siblings(".comment_head").children(".cm_right").children(".comment_inner").children("ul.comment_btns").find("a.btn.theme-btn.helpfulbtn").toggleClass("helpbtnactive");
    //   $(this).parents(".icon").toggleClass("active-icon");
    // });   

    $(".rev_acc_title").click(function () {
      $(this).toggleClass("active");
    /* $(this).siblings(".acc_panel").toggleClass("panel_active"); */
      $(this).siblings(".acc_panel").slideToggle("panel_active");
    });  

    // $("#ebikes").popover({
    //   html: true, 
    //   content: function() {
    //           return $('#ebikes-content').html();
    //         }
    // }).data('bs.popover').addAttachmentClass('header-top-popover');

    $("#ebikes").popover({
      html: true, 
      content: function() {
              return $('#ebikes-content').html();
            }
    });

    $("#forums").popover({
      html: true, 
      content: function() {
              return $('#forums-content').html();
            }
    });

    $("#more").popover({
      html: true, 
      content: function() {
              return $('#more-content').html();
            }
    });


    $("#sorting").popover({
      html: true, 
      content: function() {
              return $('#sorting-content').html();
            }
    });

    $("#filter").popover({
      html: true, 
      content: function() {
              return $('#filter-content').html();
            }
    });
    $("#tooltip").popover({
      html: true, 
      content: function() {
              return $('#tooltip_content').html();
            }
    });
 $("#tooltip1").popover({
      html: true, 
      content: function() {
              return $('#tooltip_content1').html();
            }
    });

    // window.onscroll = function() {myFunction(), "slow"};

    // // Get the header
    // var header = document.getElementById("top");

    // // Get the offset position of the navbar
    // var sticky = header.offsetTop + 30;

    // // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
    // function myFunction() {
    //   if (window.pageYOffset > sticky) {
    //     header.classList.add("sticky");
    //   } else {
    //     header.classList.remove("sticky");
    //   }

    //   if ($(this).scrollTop() > 200) {
    //       $('#scrollToTop').fadeIn();
    //   } else {
    //       $('#scrollToTop').fadeOut();
    //   }
    // }

    window.onscroll = function() {myFunction(), "slow"};
    var header = document.getElementById("top");
    var sticky = header.offsetTop + 0;;
    function myFunction() {
      if (window.pageYOffset > sticky) {
        // header.classList.add("sticky");
      } else {
        header.classList.remove("hshow");
        header.classList.remove("hide");
      }

       if ($(this).scrollTop() > 200) {
           $('#scrollToTop').fadeIn();
       } else {
           $('#scrollToTop').fadeOut();
       }
    }
  
    $('#scrollToTop').click(function(){ 
        $("html, body").animate({ scrollTop: 0 }); 
        return false; 
    }); 

    $('.header-top .nav-item').on('show.bs.popover', function () {
        // alert("show");
        $(this).addClass("show");
        setTimeout(function() {
            $("body").addClass("body-dropdown-top");
        }, 5);
        $(".filter-data").removeClass("addlayer");

       // window.scrollTo(0, 0);
    });
    
    $('body').on('click', function (e) {
        $('[data-toggle="popover"]').each(function () {
            if (!$(this).is(e.target) && 
                 $(this).has(e.target).length === 0 && 
                 $('.popover').has(e.target).length === 0) {
                 $("body").removeClass("body-dropdown-top");
                $("body").removeClass("body-dropdown-bottom");
                $(this).popover('hide');
            }
        });
    });
    $('.header-top .nav-item').on('hidden.bs.popover', function () {
        // alert("hide");
        
          //$("body").removeClass("body-dropdown-top");
          $(this).removeClass("show");
       
    });
    $('.header-bottom .nav-item').on('show.bs.popover', function () {
        setTimeout(function() {
            $("body").addClass("body-dropdown-bottom");
        }, 5);
        $(".filter-data").removeClass("addlayer");
      // window.scrollTo(0, 0);
    })
    $('.header-bottom .nav-item').on('hidden.bs.popover', function () {
      // $("body").removeClass("body-dropdown-bottom");
    })

    // $("a").on('click', function(event) {

    // // Make sure this.hash has a value before overriding default behavior
    //     if (this.hash !== "") {
    //       // Prevent default anchor click behavior
    //       event.preventDefault();

    //       // Store hash
    //       var hash = this.hash;

    //       // Using jQuery's animate() method to add smooth page scroll
    //       // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
    //       $('html, body').animate({
    //         scrollTop: $(hash).offset().top - 110
    //       }, "10000", function(){

    //         // Add hash (#) to URL when done scrolling (default click behavior)
    //         window.location.hash = hash;
    //       });
    //     } // End if
    // });
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();

        var target = this.hash;
        var $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top - 110
        }, 1000, function () {
            window.location.hash = target;
        });
    });

    $("input.search.form-control").on('focus',function(){
        $(this).parents(".filter-data").addClass("fullwidth-search");
    });
    $("a.search-close").on('click',function(){
        $(this).parents(".filter-data").removeClass("fullwidth-search");
    });
//    $("input.search.form-control").on('keyup',function(){
//        // $(this).parents(".filter-data").addClass("addlayer");
//        var count1 = $(".suggestions li").length;
//        // alert(count1);
//        if (count1>0) {
//            $(".filter-data").addClass("addlayer");
//            $("body").addClass("body-dropdown-bottom");
//        }
//        else {
//            $(".filter-data").removeClass("addlayer");
//            $("body").removeClass("body-dropdown-bottom");
//        }
//    });
   
//    $(".cookie_close_btn").on("click", function () {
//      $(".cookie_wrapper").addClass("d-none");
//      $(".footer_wrapper").removeClass("cookie_pad");
//    });
   
    $(document).click(function(event) {
        if ( !$(event.target).hasClass('suggestions')) {
            $(".filter-data").removeClass("addlayer");
            $("body").removeClass("body-dropdown-bottom");
        }
    });

   

//    const endpoint = 'https://gist.githubusercontent.com/Miserlou/c5cd8364bf9b2420bb29/raw/2bf258763cdddd704f8ffd3ea9a3e81d25e2c6f6/cities.json';
//
//        const cities = [];
//
//        fetch(endpoint)
//          .then(raw => raw.json())
//          .then(data => cities.push(...data))
//
//        function findMatches(wordToMatch, cities) {
//          return cities.filter(place => {
//            const regex = new RegExp(wordToMatch, "gi");
//            return place.city.match(regex) || place.state.match(regex)
//          });
//        }
//
//        function numberWithCommas(x) {
//          return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
//        }
//
//        function displayMatches() {
//
//          const matchArray = findMatches(this.value, cities);
//          const html = matchArray.map(place => {
//            const regex = new RegExp(this.value, 'gi');
//            const cityName = place.city.replace(regex, `<span class="hl">${this.value}</span>`);
//            const stateName = place.state.replace(regex, `<span class="hl">${this.value}</span>`);
//            return `
//              <li>
//                <span class="name">${cityName}, ${stateName}</span>
//              </li>
//            `;
//          }).join('');
//          suggestions.innerHTML = html;
//        }
//
//        const searchInput = document.querySelector(".search");
//        const suggestions = document.querySelector(".suggestions");
//        searchInput.addEventListener("change", displayMatches);
//        searchInput.addEventListener("keyup", displayMatches);

        $(document).on('click.bs.dropdown.data-api', '.header-bottom-drops', function (e) {
          e.stopPropagation();
        });
//        $(".category-item").click(function(){
//            $(this).toggleClass("active_category");
//        })
//

});



        // Hide Header on on scroll down
// var didScroll;
// var lastScrollTop = 0;
// var delta = 5;
// var navbarHeight = $('header').outerHeight();

// $(window).scroll(function(event){
//     didScroll = true;
// });

// setInterval(function() {
//     if (didScroll) {
//         hasScrolled();
//         didScroll = false;
//     }
// }, 250);

// function hasScrolled() {
//     var st = $(this).scrollTop();
    
//     // Make sure they scroll more than delta
//     if(Math.abs(lastScrollTop - st) <= delta)
//         return;
    
//     // If they scrolled down and are past the navbar, add class .nav-up.
//     // This is necessary so you never see what is "behind" the navbar.
//     if (st > lastScrollTop && st > navbarHeight){
//         // Scroll Down
//         $('header').removeClass('nav-down').addClass('nav-up');
//     } else {
//         // Scroll Up
//         if(st + $(window).height() < $(document).height()) {
//             $('header').removeClass('nav-up').addClass('nav-down');
//         }
//     }
    
//     lastScrollTop = st;
// }
(function(){

  var doc = document.documentElement;
  var w = window;

  var prevScroll = w.scrollY || doc.scrollTop;
  var curScroll;
  var direction = 0;
  var prevDirection = 0;

  var header = document.getElementById('top');

  var checkScroll = function() {

    /*
    ** Find the direction of scroll
    ** 0 - initial, 1 - up, 2 - down
    */

    curScroll = w.scrollY || doc.scrollTop;
    if (curScroll > prevScroll) { 
      //scrolled up
      direction = 2;
    }
    else if (curScroll < prevScroll) { 
      //scrolled down
      direction = 1;
    }

    if (direction !== prevDirection) {
      toggleHeader(direction, curScroll);
    }
    
    prevScroll = curScroll;
  };

  var toggleHeader = function(direction, curScroll) {
    var element = document.getElementById('top');
    var headerHeight = element.offsetHeight;
    if (direction === 2 && curScroll > headerHeight) { 
      
      //replace 52 with the height of your header in px
      header.classList.remove('hshow');
      header.classList.add('hide');
      prevDirection = direction;
    }
    else if (direction === 1) {
      header.classList.remove('hide');
      header.classList.add('hshow');
      prevDirection = direction;
    }
    // else if (direction === 0){
    //     header.classList.remove('hide');
    //     header.classList.remove('hshow');
    //     prevDirection = direction;
    // }
  };
  
  window.addEventListener('scroll', checkScroll);

})();