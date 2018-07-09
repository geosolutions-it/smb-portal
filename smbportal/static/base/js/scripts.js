"use strict";
var plugin_path = 'assets/plugins/';

/** Load Script

 USAGE
 var pageInit = function() {}
 loadScript(plugin_path + "script.js", function);

 Load multiple scripts and call a final function
 loadScript(plugin_path + "script1.js", function(){
		loadScript(plugin_path + "script2.js", function(){
			loadScript(plugin_path + "script3.js", function(){
				loadScript(plugin_path + "script4.js", function);
			});
		});
	});
 **************************************************************** **/
var _arr = {};
var _arrstyle = {};

function loadScript(scriptName, callback) {
    if (!_arr[ scriptName ]) {
        _arr[ scriptName ] = true;
        var body = document.getElementsByTagName('body')[ 0 ];
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = scriptName;
        // then bind the event to the callback function
        // there are several events for cross browser compatibility
        // script.onreadystatechange = callback;
        script.onload = callback;
        // fire the loading
        body.appendChild(script);
    } else if (callback) {
        callback();
    }
};

function loadStyle(scriptName, callback) {
    if (!_arrstyle[ scriptName ]) {
        _arrstyle[ scriptName ] = true;
        var body = document.getElementById('mainStyles');
        var style = document.createElement('link');
        style.setAttribute('rel', 'stylesheet');
        style.setAttribute('href', scriptName);
        style.onload = callback;
        body.after(style);
    } else if (callback) {
        callback();
    }
};

var pvrWriteCopyrights = function () {
        "use strict";
        var year = new Date().getFullYear();
        $("#pvrWriteCopyrights").text(year);
}

var mainApplication = function () {
        jQuery(document).ready(function (a) {
            "use strict";
            var width = $(window).width();

            function b(b) {
                var c = a("body"), d = a(b.target).attr("href");
                a(d).addClass("active"), console.log(d), c.css("overflow", "hidden"), c.addClass("offcanvas-open"), b.preventDefault()
            }

            function c() {
                var b = a("body");
                b.removeClass("offcanvas-open"), setTimeout(function () {
                    b.css("overflow", "visible"), a(".offcanvas-container").removeClass("active")
                }, 450)
            }

            function d() {
                k.parent().removeClass("expanded")
            }

            function e(b) {
                var c = b.item.index, d = a(".owl-item").eq(c).find("[data-hash]").attr("data-hash");
                a(".product-thumbnails li").removeClass("active"), a('[href="#' + d + '"]').parent().addClass("active"), a(".gallery-wrapper .gallery-item").removeClass("active"), a('[data-hash="' + d + '"]').parent().addClass("active")
            }

            (function () {
                if ("number" == typeof window.innerWidth) return window.innerWidth > document.documentElement.clientWidth;
                var a, b = document.documentElement || document.body;
                void 0 !== b.currentStyle && (a = b.currentStyle.overflow), a = a || window.getComputedStyle(b, "").overflow;
                var c;
                void 0 !== b.currentStyle && (c = b.currentStyle.overflowY), c = c || window.getComputedStyle(b, "").overflowY;
                var d = b.scrollHeight > b.clientHeight, e = /^(visible|auto)$/.test(a) || /^(visible|auto)$/.test(c),
                    f = "scroll" === a || "scroll" === c;
                return d && e || f
            })() && a("body").addClass("hasScrollbar"), a('a[href="javascript:void(0)"]').on("click", function (a) {
                a.preventDefault()
            }), function () {
                var _container = jQuery(".topbar");
                if (_container.length > 0) {

                } else {
                    var b = a("body"), c = a(".navbar-sticky"), d = a(".topbar").outerHeight(), e = c.outerHeight();
                    c.length && a(window).on("scroll", function () {
                        a(this).scrollTop() > d ? (c.addClass("navbar-stuck"), c.hasClass("navbar-ghost") || b.css("padding-top", e)) : (c.removeClass("navbar-stuck"), b.css("padding-top", 0))
                    })
                }
            }(), function (b, c, d, e) {
                a(b).on("click", function () {
                    a(e).addClass("search-visible"), setTimeout(function () {
                        a(e + " > input").focus()
                    }, 200)
                }), a(c).on("click", function () {
                    a(e).removeClass("search-visible")
                }), a(d).on("click", function () {
                    a(e + " > input").val(""), setTimeout(function () {
                        a(e + " > input").focus()
                    }, 200)
                })
            }(".toolbar .tools .search", ".close-search", ".clear-search", ".site-search"), a(".lang-currency-switcher").on("click", function () {
                a(this).parent().addClass("show"), a(this).parent().find(".dropdown-menu").addClass("show")
            }), a(document).on("click", function (b) {
                a(b.target).closest(".lang-currency-switcher-wrap").length || (a(".lang-currency-switcher-wrap").removeClass("show"), a(".lang-currency-switcher-wrap .dropdown-menu").removeClass("show"))
            }), a('[data-toggle="offcanvas"]').on("click", b), a(".site-backdrop").on("click", c);
            var f = a(".offcanvas-menu .menu").height();
            a(".offcanvas-menu .offcanvas-submenu").each(function () {
                a(this).prepend('<li class="back-btn"><a href="javascript:void(0)">Back</a></li>')
            });
            var g = a(".has-children .sub-menu-toggle");
            a(".offcanvas-menu .offcanvas-submenu .back-btn").on("click", function (b) {
                var c = this, d = a(c).parent(), e = a(c).parent().parent().siblings().parent(),
                    g = a(c).parents(".menu");
                d.removeClass("in-view"), e.removeClass("off-view"), "menu" === e.attr("class") ? g.css("height", f) : g.css("height", e.height()), b.preventDefault()
            }), g.on("click", function (b) {
                var c = this, d = a(c).parent().parent().parent(), e = a(c).parents(".menu");
                return d.addClass("off-view"), a(c).parent().parent().find("> .offcanvas-submenu").addClass("in-view"), e.css("height", a(c).parent().parent().find("> .offcanvas-submenu").height()), b.preventDefault(), !1
            });
            var h = a(".scroll-to-top-btn");
            if (h.length > 0 && (a(window).on("scroll", function () {
                    a(this).scrollTop() > 600 ? h.addClass("visible") : h.removeClass("visible")
                }), h.on("click", function (b) {
                    b.preventDefault(), a("html").velocity("scroll", {
                        offset  : 0,
                        duration: 1200,
                        easing  : "easeOutExpo",
                        mobileHA: !1
                    })
                })), a(document).on("click", ".scroll-to", function (b) {
                    var c = a(this).attr("href");
                    if ("#" === c) return !1;
                    var d = a(c);
                    if (d.length > 0) {
                        var e = d.data("offset-top") || 70;
                        a("html").velocity("scroll", {
                            offset  : a(this.hash).offset().top - e,
                            duration: 1e3,
                            easing  : "easeOutExpo",
                            mobileHA: !1
                        })
                    }
                    b.preventDefault()
                }), function (b) {
                    b.each(function () {
                        var b = a(this), c = b.data("filter-list"), d = b.find("input[type=text]"),
                            e = b.find("input[type=radio]"), f = a(c).find(".list-group-item");
                        d.keyup(function () {
                            var b = d.val();
                            f.each(function () {
                                0 == a(this).text().toLowerCase().indexOf(b.toLowerCase()) ? a(this).show() : a(this).hide()
                            })
                        }), e.on("click", function (b) {
                            var c = a(this).val();
                            "all" !== c ? (f.hide(), a("[data-filter-item=" + c + "]").show()) : f.show()
                        })
                    })
                }(a("[data-filter-list]")), function (b, c) {
                    b.each(function () {
                        var b = a(this), d = a(this).data("date-time");
                        (c || b).downCount({date: d, offset: 10})
                    })
                }(a(".countdown")), a("[data-toast]").on("click", function () {
                    var b = a(this), c = b.data("toast-type"), d = b.data("toast-icon"), e = b.data("toast-position"),
                        f = b.data("toast-title"), g = b.data("toast-message"), h = "";
                    switch (e) {
                        case"topRight":
                            h = {
                                class              : "iziToast-" + c || "",
                                title              : f || "Title",
                                message            : g || "toast message",
                                animateInside      : !1,
                                position           : "topRight",
                                progressBar        : !1,
                                icon               : d,
                                timeout            : 3200,
                                transitionIn       : "fadeInLeft",
                                transitionOut      : "fadeOut",
                                transitionInMobile : "fadeIn",
                                transitionOutMobile: "fadeOut"
                            };
                            break;
                        case"bottomRight":
                            h = {
                                class              : "iziToast-" + c || "",
                                title              : f || "Title",
                                message            : g || "toast message",
                                animateInside      : !1,
                                position           : "bottomRight",
                                progressBar        : !1,
                                icon               : d,
                                timeout            : 3200,
                                transitionIn       : "fadeInLeft",
                                transitionOut      : "fadeOut",
                                transitionInMobile : "fadeIn",
                                transitionOutMobile: "fadeOut"
                            };
                            break;
                        case"topLeft":
                            h = {
                                class              : "iziToast-" + c || "",
                                title              : f || "Title",
                                message            : g || "toast message",
                                animateInside      : !1,
                                position           : "topLeft",
                                progressBar        : !1,
                                icon               : d,
                                timeout            : 3200,
                                transitionIn       : "fadeInRight",
                                transitionOut      : "fadeOut",
                                transitionInMobile : "fadeIn",
                                transitionOutMobile: "fadeOut"
                            };
                            break;
                        case"bottomLeft":
                            h = {
                                class              : "iziToast-" + c || "",
                                title              : f || "Title",
                                message            : g || "toast message",
                                animateInside      : !1,
                                position           : "bottomLeft",
                                progressBar        : !1,
                                icon               : d,
                                timeout            : 3200,
                                transitionIn       : "fadeInRight",
                                transitionOut      : "fadeOut",
                                transitionInMobile : "fadeIn",
                                transitionOutMobile: "fadeOut"
                            };
                            break;
                        case"topCenter":
                            h = {
                                class              : "iziToast-" + c || "",
                                title              : f || "Title",
                                message            : g || "toast message",
                                animateInside      : !1,
                                position           : "topCenter",
                                progressBar        : !1,
                                icon               : d,
                                timeout            : 3200,
                                transitionIn       : "fadeInDown",
                                transitionOut      : "fadeOut",
                                transitionInMobile : "fadeIn",
                                transitionOutMobile: "fadeOut"
                            };
                            break;
                        case"bottomCenter":
                            h = {
                                class              : "iziToast-" + c || "",
                                title              : f || "Title",
                                message            : g || "toast message",
                                animateInside      : !1,
                                position           : "bottomCenter",
                                progressBar        : !1,
                                icon               : d,
                                timeout            : 3200,
                                transitionIn       : "fadeInUp",
                                transitionOut      : "fadeOut",
                                transitionInMobile : "fadeIn",
                                transitionOutMobile: "fadeOut"
                            };
                            break;
                        default:
                            h = {
                                class              : "iziToast-" + c || "",
                                title              : f || "Title",
                                message            : g || "toast message",
                                animateInside      : !1,
                                position           : "topRight",
                                progressBar        : !1,
                                icon               : d,
                                timeout            : 3200,
                                transitionIn       : "fadeInLeft",
                                transitionOut      : "fadeOut",
                                transitionInMobile : "fadeIn",
                                transitionOutMobile: "fadeOut"
                            }
                    }
                    iziToast.show(h)
                }), a(".btn-wishlist").on("click", function () {
                    var b = a(this).data("iteration") || 1, c = {
                        title              : "Product",
                        animateInside      : !1,
                        position           : "topRight",
                        progressBar        : !1,
                        timeout            : 3200,
                        transitionIn       : "fadeInLeft",
                        transitionOut      : "fadeOut",
                        transitionInMobile : "fadeIn",
                        transitionOutMobile: "fadeOut"
                    };
                    switch (b) {
                        case 1:
                            a(this).addClass("active"), c.class = "iziToast-info", c.message = "added to your wishlist!", c.icon = "icon-bell";
                            break;
                        case 2:
                            a(this).removeClass("active"), c.class = "iziToast-danger", c.message = "removed from your wishlist!", c.icon = "icon-ban"
                    }
                    iziToast.show(c), b++, b > 2 && (b = 1), a(this).data("iteration", b)
                }), a(".isotope-grid").length) var i = a(".isotope-grid").imagesLoaded(function () {
                i.isotope({
                    itemSelector      : ".grid-item",
                    transitionDuration: "0.7s",
                    masonry           : {columnWidth: ".grid-sizer", gutter: ".gutter-sizer"}
                })
            });
            if (a(".filter-grid").length > 0) {
                var j = a(".filter-grid");
                a(".nav-pills").on("click", "a", function (b) {
                    b.preventDefault(), a(".nav-pills a").removeClass("active"), a(this).addClass("active");
                    var c = a(this).attr("data-filter");
                    j.isotope({filter: c})
                })
            }
            var k = a(".widget-categories .has-children > a");
            k.on("click", function (b) {
                a(b.target).parent().is(".expanded") ? d() : (d(), a(this).parent().addClass("expanded"))
            }), a('[data-toggle="tooltip"]').tooltip(), a('[data-toggle="popover"]').popover();
            var l = document.querySelector(".ui-range-slider");
            if (void 0 !== l && null !== l) {
                var m = parseInt(l.parentNode.getAttribute("data-start-min"), 10),
                    n = parseInt(l.parentNode.getAttribute("data-start-max"), 10),
                    o = parseInt(l.parentNode.getAttribute("data-min"), 10),
                    p = parseInt(l.parentNode.getAttribute("data-max"), 10),
                    q = parseInt(l.parentNode.getAttribute("data-step"), 10),
                    r = document.querySelector(".ui-range-value-min span"),
                    s = document.querySelector(".ui-range-value-max span"),
                    t = document.querySelector(".ui-range-value-min input"),
                    u = document.querySelector(".ui-range-value-max input");
                noUiSlider.create(l, {
                    start  : [ m, n ],
                    connect: !0,
                    step   : q,
                    range  : {min: o, max: p}
                }), l.noUiSlider.on("update", function (a, b) {
                    var c = a[ b ];
                    b ? (s.innerHTML = Math.round(c), u.value = Math.round(c)) : (r.innerHTML = Math.round(c), t.value = Math.round(c))
                })
            }
            var v = a(".interactive-credit-card");
            if (v.length && v.card({
                    form     : ".interactive-credit-card",
                    container: ".card-wrapper"
                }), a(".gallery-wrapper").length) {
                !function (b) {
                    function c(a, b) {
                        return (" " + a.className + " ").indexOf(" " + b + " ") > -1
                    }

                    for (var d = function (b) {
                        for (var c, d, e, f, g = a(b).find(".gallery-item:not(.isotope-hidden)").get(), h = g.length, i = [], j = 0; j < h; j++) c = g[ j ], 1 === c.nodeType && (d = c.children[ 0 ], "video" == a(d).data("type") ? f = {html: a(d).data("video")} : (e = d.getAttribute("data-size").split("x"), f = {
                            src: d.getAttribute("href"),
                            w  : parseInt(e[ 0 ], 10),
                            h  : parseInt(e[ 1 ], 10)
                        }), c.children.length > 1 && (f.title = a(c).find(".caption").html()), d.children.length > 0 && (f.msrc = d.children[ 0 ].getAttribute("src")), f.el = c, i.push(f));
                        return i
                    }, e = function a(b, c) {
                        return b && (c(b) ? b : a(b.parentNode, c))
                    }, f = function (b) {
                        b = b || window.event, b.preventDefault ? b.preventDefault() : b.returnValue = !1;
                        var d = b.target || b.srcElement, f = e(d, function (a) {
                            return c(a, "gallery-item")
                        });
                        if (f) {
                            for (var h, i = f.closest(".gallery-wrapper"), j = a(f.closest(".gallery-wrapper")).find(".gallery-item:not(.isotope-hidden)").get(), k = j.length, l = 0, m = 0; m < k; m++) if (1 === j[ m ].nodeType) {
                                if (j[ m ] === f) {
                                    h = l;
                                    break
                                }
                                l++
                            }
                            return h >= 0 && g(h, i), !1
                        }
                    }, g = function (b, c, e, f) {
                        var g, h, i, j = document.querySelectorAll(".pswp")[ 0 ];
                        if (i = d(c), h = {
                                closeOnScroll   : !1,
                                galleryUID      : c.getAttribute("data-pswp-uid"),
                                getThumbBoundsFn: function (b) {
                                    var c = i[ b ].el.getElementsByTagName("img")[ 0 ];
                                    if (a(c).length > 0) {
                                        var d = window.pageYOffset || document.documentElement.scrollTop,
                                            e = c.getBoundingClientRect();
                                        return {x: e.left, y: e.top + d, w: e.width}
                                    }
                                }
                            }, f) if (h.galleryPIDs) {
                            for (var k = 0; k < i.length; k++) if (i[ k ].pid == b) {
                                h.index = k;
                                break
                            }
                        } else h.index = parseInt(b, 10) - 1; else h.index = parseInt(b, 10);
                        isNaN(h.index) || (e && (h.showAnimationDuration = 0), g = new PhotoSwipe(j, PhotoSwipeUI_Default, i, h), g.init(), g.listen("beforeChange", function () {
                            var b = a(g.currItem.container);
                            a(".pswp__video").removeClass("active");
                            b.find(".pswp__video").addClass("active");
                            a(".pswp__video").each(function () {
                                a(this).hasClass("active") || a(this).attr("src", a(this).attr("src"))
                            })
                        }), g.listen("close", function () {
                            a(".pswp__video").each(function () {
                                a(this).attr("src", a(this).attr("src"))
                            })
                        }))
                    }, h = document.querySelectorAll(b), i = 0, j = h.length; i < j; i++) h[ i ].setAttribute("data-pswp-uid", i + 1), h[ i ].onclick = f;
                    var k = function () {
                        var a = window.location.hash.substring(1), b = {};
                        if (a.length < 5) return b;
                        for (var c = a.split("&"), d = 0; d < c.length; d++) if (c[ d ]) {
                            var e = c[ d ].split("=");
                            e.length < 2 || (b[ e[ 0 ] ] = e[ 1 ])
                        }
                        return b.gid && (b.gid = parseInt(b.gid, 10)), b
                    }();
                    k.pid && k.gid && g(k.pid, h[ k.gid - 1 ], !0, !0)
                }(".gallery-wrapper")
            }
            var w = a(".product-carousel");
            w.length && w.owlCarousel({
                items          : 1,
                loop           : !1,
                dots           : !1,
                URLhashListener: !0,
                startPosition  : "URLHash",
                onTranslate    : e
            });
            var x = a(".google-map");
            x.length && x.each(function () {
                var b = a(this).data("height"), c = a(this).data("address"), d = a(this).data("zoom"),
                    e = a(this).data("disable-controls"), f = a(this).data("scrollwheel"), g = a(this).data("marker"),
                    h = a(this).data("marker-title"), i = a(this).data("styles");
                a(this).height(b), a(this).gmap3({
                    marker: {
                        address: c,
                        data   : h,
                        options: {icon: g},
                        events : {
                            mouseover  : function (b, c, d) {
                                var e = a(this).gmap3("get"), f = a(this).gmap3({get: {name: "infowindow"}});
                                f ? (f.open(e, b), f.setContent(d.data)) : a(this).gmap3({
                                    infowindow: {
                                        anchor : b,
                                        options: {content: d.data}
                                    }
                                })
                            }, mouseout: function () {
                                var b = a(this).gmap3({get: {name: "infowindow"}});
                                b && b.close()
                            }
                        }
                    }, map: {options: {zoom: d, disableDefaultUI: e, scrollwheel: f, styles: i}}
                })
            })
        });
    },
    pvrCountJS = function () {
        "use strict";
        $("[data-count=true]").each(function () {
            generateCount($(this))
        })
    },
    generateCount = function (e) {
        "use strict";
        if (!$(e).attr("data-init")) {
            var a = $(e).attr("data-number");
            var id = $(e).attr("id");
            var options = {
                useEasing  : true,
                useGrouping: true,
                separator  : ',',
                decimal    : '.',
            };
            var demo = new CountUp(id, 0, parseInt(a, 10), 0, 2.5, options);
            if (!demo.error) {
                demo.start();
            } else {
                console.error(demo.error);
            }
        }
    },
    pvrTypeitJS = function () {
        "use strict";
        $("[data-typeit=true]").each(function () {
            generateTypeit($(this))
        })
    },
    generateTypeit = function (e) {
        "use strict";
        if ("[data-typeit=true]".length !== 0) {
            var a = $.trim($(e).text());
            var id = $(e).attr("id");
            $('#' + id).typeIt({
                whatToType: a,
                typeSpeed : 100,
                cursor    : true,
            });
        }
    },
    _chat_popup = function () {

        var _container = jQuery(".perfect_scrollbar");
        if (_container.length > 0) {
            loadStyle(plugin_path + 'perfect-scrollbar/css/perfect-scrollbar.min.css');
            loadScript(plugin_path + 'perfect-scrollbar/js/perfect-scrollbar.jquery.min.js', function () {

                var count = 0;
                var classes = [ "theme_1", "theme_2", "theme_3", "theme_4" ];
                var length = classes.length;
                $(function () {
                    $('.app_chat_w').toggleClass('active');

                    $('.app_chat_button, .app_chat_w .chat-close').on('click', function () {
                        $('.app_chat_w').toggleClass('active');
                        return false;
                    });

                    $('.message-input').on('keypress', function (e) {
                        if (e.which == 13) {
                            var val = ($(this).val() !== '') ? $(this).val() : "Lorem Ipsum is simply dummy text of the printing.";
                            $('.chat-messages').append('<div class="message self"><div class="message-content">' + val + '</div></div>');
                            $(this).val('');
                            setTimeout(function () {
                                $('.chat-messages').append('<div class="message"><div class="message-content">' + val + '</div></div>');
                                $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                                $messages_w.perfectScrollbar('update');
                            }, 200)
                            var $messages_w = $('.app_chat_w .chat-messages');
                            $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                            $messages_w.perfectScrollbar('update');
                            return false;
                        }
                    });

                    $('.app_chat_w .chat-messages').perfectScrollbar();

                    $(".change_chat_theme").on('click', function () {
                        $(".chat-messages").removeAttr("class").addClass("chat-messages " + classes[ count ]);
                        if (parseInt(count, 10) === parseInt(length, 10) - 1) {
                            count = 0;
                        } else {
                            count = parseInt(count, 10) + 1;
                        }
                        var $messages_w = $('.app_chat_w .chat-messages');
                        $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                        $messages_w.perfectScrollbar('update');
                    })
                });
            });
        }
    },
    _live_customizer = function () {

        var _container = jQuery("#live_customizer");
        if (_container.length > 0) {
            (function () {
                var bodyEl = document.body,
                    content = document.getElementById('container'),
                    openbtn = document.getElementById('live_customizer'),
                    closebtn = document.getElementById('close-button'),
                    isOpen = false;

                function init() {
                    initEvents();
                }

                function initEvents() {
                    openbtn.addEventListener('click', toggleMenu);
                    if (closebtn) {
                        closebtn.addEventListener('click', toggleMenu);
                    }
                    content.addEventListener('click', function (ev) {
                        var target = ev.target;
                        if (isOpen && target !== openbtn) {
                            toggleMenu();
                        }
                    });
                }

                function toggleMenu() {
                    if (isOpen) {
                        classie.remove(bodyEl, 'show-menu');
                    }
                    else {
                        classie.add(bodyEl, 'show-menu');
                    }
                    isOpen = !isOpen;
                }

                init();

                var elem = document.querySelector('.color_dark_settings');
                var switchery = new Switchery(elem, {color: '#0da9ef', size: 'small'});
                var elem_2 = document.querySelector('.minified_switch_settings');
                var switchery_2 = new Switchery(elem_2, {color: '#0da9ef', size: 'small'});
                var elem_3 = document.querySelector('.minified_switch_nav_sticky');
                var switchery_3 = new Switchery(elem_3, {color: '#0da9ef', size: 'small'});
                elem.onchange = function () {
                    if (elem.checked) {
                        $("body").addClass("dark_version");
                        iziToast.success({
                            title: 'Dark Layout',
                            message: 'Dark Layout update will receive soon!',
                            position:"topRight"
                        });
                    } else {
                        $("body").removeClass("dark_version");
                    }
                };
                elem_2.onchange = function () {
                    if (elem_2.checked) {
                        $("#menu-categories, .cats-toggle").removeClass("hide");
                    } else {
                        $("#menu-categories, .cats-toggle").addClass("hide");
                    }
                };
                elem_3.onchange = function () {
                    if ($("header.navbar").length) {
                        if (elem_3.checked) {
                            $("header.navbar").removeClass("navbar-stuck").addClass("navbar-sticky");
                        } else {
                            $("header.navbar").removeClass("navbar-sticky").addClass("navbar-stuck");
                        }
                    }
                };

            })();
        }
    },
    _url_parameters_ui_elements = function () {
        var _container = jQuery("#ui_elements_nav");
        if (_container.length > 0) {
            var newURL = window.location.protocol + "//" + window.location.host + "" + window.location.pathname;
            var string = window.location.pathname;
            var array = string.split('/');
            var lastEl = array[ array.length - 1 ];
            $.each($(_container).find('a'), function (i, d) {
                var href = $(this).attr("href")
                if (lastEl == href) {
                    $(this).addClass("active")
                }
            })
        }
    },
    _UI_elements = function () {
        var _container = jQuery("#close_other_accordion");
        if (_container.length > 0) {
            var $myGroup = $('#close_other_accordion');
            $($myGroup).on('show.bs.collapse', function () {
                $myGroup.find('.collapse.show').collapse('hide');
            })
        }
    },
    _showSwal = function (type) {
        var _container = jQuery(".sweet_alert");
        if (_container.length > 0) {
            loadStyle(plugin_path + 'sweet_alert/sweetalert.css');
            loadScript(plugin_path + 'sweet_alert/sweetalert.min.js', function () {
                $("#basic_alert").on("click", function () {
                    swal("Here's a message!");
                });
                $("#title-and-text").on("click", function () {
                    swal("Here's a message!", "It's pretty, isn't it?");
                });
                $("#success-message").on("click", function () {
                    swal("Good job!", "You clicked the button!", "success");
                });
                $("#warning-message-and-confirmation").on("click", function () {
                    swal({
                        title             : "Are you sure?",
                        text              : "You will not be able to recover this imaginary file!",
                        type              : "warning",
                        showCancelButton  : true,
                        confirmButtonClass: "btn btn-info btn-fill",
                        confirmButtonText : "Yes, delete it!",
                        cancelButtonClass : "btn btn-danger btn-fill",
                        closeOnConfirm    : false,
                    }, function () {
                        swal("Deleted!", "Your imaginary file has been deleted.", "success");
                    });
                });
                $("#warning-message-and-cancel").on("click", function () {
                    swal({
                        title            : "Are you sure?",
                        text             : "You will not be able to recover this imaginary file!",
                        type             : "warning",
                        showCancelButton : true,
                        confirmButtonText: "Yes, delete it!",
                        cancelButtonText : "No, cancel plx!",
                        closeOnConfirm   : false,
                        closeOnCancel    : false
                    }, function (isConfirm) {
                        if (isConfirm) {
                            swal("Deleted!", "Your imaginary file has been deleted.", "success");
                        } else {
                            swal("Cancelled", "Your imaginary file is safe :)", "error");
                        }
                    });
                });
                $("#custom-html").on("click", function () {
                    swal({
                        title: 'HTML example',
                        html : 'You can use <b>bold text</b>, ' +
                        '<a href="javascript:;">links</a> ' +
                        'and other HTML tags'
                    });
                });
                $("#auto-close").on("click", function () {
                    swal({
                        title            : "Auto close alert!",
                        text             : "I will close in 2 seconds.",
                        timer            : 2000,
                        showConfirmButton: false
                    });
                });
            });
        }
    },
    _MultiLevelMenu = function (type) {
        var _container = jQuery("#ml-menu");
        if (_container.length > 0) {
            loadStyle(plugin_path + 'sidebar/component.css');
            loadScript(plugin_path + 'sidebar/modernizr-custom.js');
            loadScript(plugin_path + 'sidebar/main.js', function () {
                setTimeout(function () {
                    (function () {
                        var menuEl = document.getElementById('ml-menu'),
                            mlmenu = new MLMenu(menuEl, {
                                // breadcrumbsCtrl : true, // show breadcrumbs
                                // initialBreadcrumb : 'all', // initial breadcrumb text
                                backCtrl   : false, // show back button
                                // itemsDelayInterval : 60, // delay between each menu item sliding animation
                                onItemClick: loadDummyData // callback: item that doesn´t have a submenu gets clicked - onItemClick([event], [inner HTML of the clicked item])
                            });

                        // mobile menu toggle
                        var openMenuCtrl = document.querySelector('.action--open'),
                            closeMenuCtrl = document.querySelector('.action--close');

                        //openMenuCtrl.addEventListener('click', openMenu);
                        closeMenuCtrl.addEventListener('click', closeMenu);

                        function openMenu() {
                            classie.add(menuEl, 'menu--open');
                            closeMenuCtrl.focus();
                        }

                        function closeMenu() {
                            classie.remove(menuEl, 'menu--open');
                            openMenuCtrl.focus();
                        }

                        // simulate grid content loading
                        var gridWrapper = document.querySelector('.content');

                        function loadDummyData(ev, itemName) {
                            ev.preventDefault();

                            closeMenu();
                            gridWrapper.innerHTML = '';
                            classie.add(gridWrapper, 'content--loading');
                            setTimeout(function () {
                                classie.remove(gridWrapper, 'content--loading');
                                gridWrapper.innerHTML = '<ul class="products">' + dummyData[ itemName ] + '<ul>';
                            }, 700);
                        }
                    })();
                }, 200)
            });
        }
    },
    _cookie_bar = function () {
        var _container = jQuery(".mt-cookie-consent-btn");
        if (_container.length > 0) {
            $(".mt-cookie-consent-btn").on("click", function () {
                $(".pvr-cookie-consent-bar").addClass("animated fadeOutDown")
            });
        }
    },
    _instafeed = function () {
        var _container = jQuery(".instafeed");
        if (_container.length > 0) {
            loadStyle(plugin_path + 'fancybox/css/jquery.fancybox.min.css');
            loadScript(plugin_path + 'fancybox/js/jquery.fancybox.min.js');
            loadScript(plugin_path + 'instafeed/instafeed.js', function () {
                $('.instafeed').each(function () {
                    var $this = $(this);
                    var target = $this.attr('id');
                    var userId = $this.data('user-id');
                    var limit = $this.data('limit');
                    var col = $this.data('col');
                    var template;
                    var classes = $this.data('classes') ? $this.data('classes') : '';
                    var lightbox = $this.data('lightbox') ? ' data-fancybox ' : '';

                    // Fill with the data from Instagram API
                    var clientID = '19f36b839e614c8c9986cb5b629db006';
                    var accessToken = '4841496280.19f36b8.9e528e3ba8fe4433a07f8d1ffc4f8bf8';

                    var instafeed = new Instafeed({
                        target     : target,
                        clientId   : clientID,
                        accessToken: accessToken,
                        get        : 'user',
                        userId     : userId,
                        limit      : limit,
                        resolution : 'thumbnail',
                        template   : '<a href="{{link}}"' + lightbox + '><img src="{{image}}" class="rounded-circle w-50 m-r-10 m-t-10 img-fluid ' + classes + '" /></a>'
                    });
                    instafeed.run();

                });
            });
        }
    },
    _email_page = function () {
        var _container = jQuery(".email_page");
        if (_container.length > 0) {
            loadScript(plugin_path + 'ckeditor/ckeditor.js', function () {
                $(document).ready(function () {
                    // CKEDITOR ACTIVATION FOR MAIL REPLY
                    if ($('#ckeditorEmail').length) {
                        CKEDITOR.config.uiColor = '#ffffff';
                        CKEDITOR.config.toolbar = [ [ 'Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink', '-', 'About' ] ];
                        CKEDITOR.config.height = 110;
                        CKEDITOR.replace('ckeditor1');
                    }

                    // EMAIL MOBILE SHOW MESSAGE
                    $('.pvr-item').on('click', function () {
                        $('.pvr-email-w').addClass('forse-show-content');
                    });

                    if ($('.pvr-email-w').length) {
                        if (is_display_type('phone') || is_display_type('tablet')) {
                            $('.pvr-email-w').addClass('compact-side-menu');
                        }
                    }
                });
            });
        }

        function is_display_type(display_type) {
            return $('.display-type').css('content') == display_type || $('.display-type').css('content') == '"' + display_type + '"';
        }

        function not_display_type(display_type) {
            return $('.display-type').css('content') != display_type && $('.display-type').css('content') != '"' + display_type + '"';
        }
    },
    _validation = function () {
        var _container = jQuery(".validation");
        if (_container.length > 0) {
            loadScript(plugin_path + 'jquery-validate/jquery.validate.min.js');
            loadScript(plugin_path + 'jquery-validate/additional-methods.min.js');
            loadScript(plugin_path + 'jquery-validate/jquery-validate.bootstrap-tooltip.min.js', function () {

                iziToast.settings({
                    timeout      : 10000,
                    resetOnHover : true,
                    transitionIn : 'flipInX',
                    transitionOut: 'flipOutX',
                    onOpening    : function () {

                    },
                    onClosing    : function () {

                    }
                });

                $(".validate_1").validate({
                    submitHandler : function (form) { // for demo
                        alert('valid form');
                        return false;
                    },
                    invalidHandler: function (event, validator) {
                        $.each(validator.currentElements, function () {
                            $(this).closest(".form-group").addClass("has-danger")
                        });
                        // 'this' refers to the form
                        var errors = validator.numberOfInvalids();
                        if (errors) {
                            var message = errors == 1
                                ? 'You missed 1 field. It has been highlighted'
                                : 'You missed ' + errors + ' fields. They have been highlighted';
                            //$("div.error span").html(message);
                            iziToast.error({
                                class  : "iziToast-" + "icon-circle-check",
                                title  : 'Error',
                                message: message,
                            });

                        } else {
                            $("div.error").hide();
                        }
                    },
                    rules         : {
                        eamil           : {
                            required: true
                        },
                        password        : {
                            required: true
                        },
                        confirm_password: {
                            required: true
                        },
                        regular_selst   : {
                            required: true
                        }
                    }
                });

                $(".validate_2").validate({
                    submitHandler : function (form) { // for demo
                        alert('valid form');
                        return false;
                    },
                    invalidHandler: function (event, validator) {
                        $.each(validator.currentElements, function () {
                            $(this).closest(".form-group").addClass("has-danger")
                        });
                        // 'this' refers to the form
                        var errors = validator.numberOfInvalids();
                        if (errors) {
                            var message = errors == 1
                                ? 'You missed 1 field. It has been highlighted'
                                : 'You missed ' + errors + ' fields. They have been highlighted';
                            //$("div.error span").html(message);
                            iziToast.error({
                                class  : "iziToast-" + "icon-circle-check",
                                title  : 'Error',
                                message: message,
                            });

                        } else {
                            $("div.error").hide();
                        }
                    },
                    rules         : {
                        eamil_2           : {
                            required: true
                        },
                        password_2        : {
                            required: true
                        },
                        confirm_password_2: {
                            required: true
                        },
                        regular_selst_2   : {
                            required: true
                        }
                    }
                });

            });
        }
    },
    _date_time = function () {
        var _container = jQuery(".date_picker");
        if (_container.length > 0) {
            loadStyle(plugin_path + 'bootstrap-datepicker/css/bootstrap-datepicker3.css');
            loadScript(plugin_path + 'bootstrap-datepicker/js/bootstrap-datepicker.js', function () {
                $.fn._datepicker = function () {
                    $('.date_picker').datepicker({
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    });
                };
                $.fn._daterange_picker = function () {
                    $(".daterange_picker").datepicker({
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    })
                };
                $.fn._format_date_picker = function () {
                    $(".format_date_picker").datepicker({
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        format        : "dd/mm/yyyy",
                        orientation   : "bottom right",
                    })
                };
                $.fn._date_picker_disable_future = function () {
                    var EndDate = new Date();
                    $('.date_picker_disable_future').datepicker({
                        endDate       : EndDate,
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    });
                };
                $.fn._date_picker_disable_past = function () {
                    var StartDate = new Date();
                    $('.date_picker_disable_past').datepicker({
                        startDate     : StartDate,
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    });
                };
                $.fn._date_picker_start_view = function () {
                    $('.date_picker_start_view').datepicker({
                        startView     : 2,
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    });
                };
                $.fn._date_picker_clear = function () {
                    $('.date_picker_clear').datepicker({
                        clearBtn      : true,
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    });
                };
                $.fn._date_picker_multidate = function () {
                    $('.date_picker_multidate').datepicker({
                        multidate     : true,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    });
                };
                $.fn._date_picker_calendarweeks = function () {
                    $('.date_picker_calendarweeks').datepicker({
                        calendarWeeks : true,
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    });
                };
                $.fn._date_inline = function () {
                    $('.date_inline').datepicker({
                        calendarWeeks : true,
                        autoclose     : !0,
                        todayBtn      : true,
                        todayHighlight: true,
                        orientation   : "bottom right",
                    });
                };

                if ($(".date_picker").length > 0) {
                    $()._datepicker();
                }
                if ($(".daterange_picker").length > 0) {
                    $()._daterange_picker();
                }
                if ($(".format_date_picker").length > 0) {
                    $()._format_date_picker();
                }
                if ($(".date_picker_disable_future").length > 0) {
                    $()._date_picker_disable_future();
                }
                if ($(".date_picker_disable_past").length > 0) {
                    $()._date_picker_disable_past();
                }
                if ($(".date_picker_start_view").length > 0) {
                    $()._date_picker_start_view();
                }
                if ($(".date_picker_clear").length > 0) {
                    $()._date_picker_clear();
                }
                if ($(".date_picker_multidate").length > 0) {
                    $()._date_picker_multidate();
                }
                if ($(".date_picker_calendarweeks").length > 0) {
                    $()._date_picker_calendarweeks();
                }
                if ($(".date_inline").length > 0) {
                    $()._date_inline();
                }
            });
        }

        var _container = jQuery(".time_picker");
        if (_container.length > 0) {
            loadStyle(plugin_path + 'bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css');
            loadScript(plugin_path + 'bootstrap-datetimepicker/js/bootstrap-datetimepicker.js', function () {
                $.fn._date_time_picker = function () {
                    $('.date_time_picker').datetimepicker({
                        autoclose     : !0,
                        pickerPosition: "bottom-right",
                        fontAwesome   : true,
                    });
                };
                $.fn._time_picker = function () {
                    $('.time_picker').datetimepicker({
                        format      : "HH:ii P",
                        showMeridian: true,
                        autoclose   : true,
                        startView   : 1,
                        fontAwesome : true,
                    });
                };
                $.fn._date_time_mirror_field = function () {
                    $('.date_time_mirror_field').datetimepicker({
                        format     : "dd MM yyyy - hh:ii",
                        linkField  : "mirror_field",
                        linkFormat : "yyyy-mm-dd hh:ii",
                        autoclose  : true,
                        fontAwesome: true,
                    });
                };
                $.fn._date_time_inline = function () {
                    $('.date_time_inline').datetimepicker({
                        format     : "dd MM yyyy - hh:ii",
                        linkFormat : "yyyy-mm-dd hh:ii",
                        fontAwesome: true,
                    });
                };

                if ($(".date_time_picker").length > 0) {
                    $()._date_time_picker();
                }
                if ($(".time_picker").length > 0) {
                    $()._time_picker();
                }
                if ($(".date_time_mirror_field").length > 0) {
                    $()._date_time_mirror_field();
                }
                if ($(".date_time_inline").length > 0) {
                    $()._date_time_inline();
                }
            });
        }

        var _container = jQuery(".select_2");
        if (_container.length > 0) {
            loadStyle(plugin_path + 'select2/css/select2.min.css');
            loadScript(plugin_path + 'select2/js/select2.min.js', function () {
                $.fn._select2 = function () {
                    $(".select_2").select2();
                };
                $.fn._select_2_multiple = function () {
                    $(".select_2_multiple").select2({
                        placeholder: "Multiple Select"
                    });
                };
                $.fn._select_2_search_starts = function () {
                    $(".select_2_search_starts").select2({
                        placeholder: "Search from Starting letter",
                        matcher    : function (params, data) {
                            if ($.trim(params.term) === '') {
                                return data;
                            }
                            if (data.text.toLowerCase().startsWith(params.term.toLowerCase())) {
                                var modifiedData = $.extend({}, data, true);
                                return modifiedData;
                            }
                            return null;
                        }
                    });
                };
                $.fn._select_2_limit = function () {
                    $(".select_2_limit").select2({
                        placeholder           : "Limit Selection",
                        maximumSelectionLength: 2
                    });
                };
                $.fn._select_2_clear = function () {
                    $(".select_2_clear").select2({
                        placeholder: 'Clearable Select',
                        allowClear : true
                    });
                };
                $.fn._select_2_hide_search = function () {
                    $(".select_2_hide_search").select2({
                        minimumResultsForSearch: Infinity
                    });
                };

                if ($(".select_2").length > 0) {
                    $()._select2();
                }
                if ($(".select_2_multiple").length > 0) {
                    $()._select_2_multiple();
                }
                if ($(".select_2_search_starts").length > 0) {
                    $()._select_2_search_starts();
                }
                if ($(".select_2_limit").length > 0) {
                    $()._select_2_limit();
                }
                if ($(".select_2_clear").length > 0) {
                    $()._select_2_clear();
                }
                if ($(".select_2_hide_search").length > 0) {
                    $()._select_2_hide_search();
                }
            });
        }

        var _container = jQuery(".clipboard");
        if (_container.length > 0) {
            loadScript(plugin_path + 'clipboard/clipboard.min.js', function () {
                $.fn._clipboard = function () {
                    new Clipboard(".btn").on("success", function (e) {
                        $(e.trigger).tooltip({
                            title    : "Copied",
                            placement: "top"
                        }), $(e.trigger).tooltip("show"), setTimeout(function () {
                            $(e.trigger).tooltip("dispose")
                        }, 500)
                    })
                };
                if ($(".clipboard").length > 0) {
                    $()._clipboard();
                }
            });
        }

        var _container = jQuery(".sessionTimeout");
        if (_container.length > 0) {
            loadScript(plugin_path + 'jquery.sessionTimeout/jquery.sessionTimeout.js', function () {
                $.sessionTimeout({
                    title             : "Session Timeout Notification",
                    message           : "Your session is about to expire.",
                    //keepAliveUrl      : "../demo/timeout-keep-alive.php",
                    redirUrl          : "index.html",
                    logoutUrl         : "index.html",
                    warnAfter         : 5e3,
                    redirAfter        : 15e3,
                    ignoreUserActivity: !0,
                    countdownMessage  : "Redirecting in {timer} seconds.",
                    countdownBar      : !0
                });

                var now = new Date(),
                    hourDeg = now.getHours() / 12 * 360 + now.getMinutes() / 60 * 30,
                    minuteDeg = now.getMinutes() / 60 * 360 + now.getSeconds() / 60 * 6,
                    secondDeg = now.getSeconds() / 60 * 360,
                    stylesDeg = [
                        "@-webkit-keyframes rotate-hour{from{transform:rotate(" + hourDeg + "deg);}to{transform:rotate(" + (hourDeg + 360) + "deg);}}",
                        "@-webkit-keyframes rotate-minute{from{transform:rotate(" + minuteDeg + "deg);}to{transform:rotate(" + (minuteDeg + 360) + "deg);}}",
                        "@-webkit-keyframes rotate-second{from{transform:rotate(" + secondDeg + "deg);}to{transform:rotate(" + (secondDeg + 360) + "deg);}}",
                        "@-moz-keyframes rotate-hour{from{transform:rotate(" + hourDeg + "deg);}to{transform:rotate(" + (hourDeg + 360) + "deg);}}",
                        "@-moz-keyframes rotate-minute{from{transform:rotate(" + minuteDeg + "deg);}to{transform:rotate(" + (minuteDeg + 360) + "deg);}}",
                        "@-moz-keyframes rotate-second{from{transform:rotate(" + secondDeg + "deg);}to{transform:rotate(" + (secondDeg + 360) + "deg);}}"
                    ].join("");
                document.getElementById("clock-animations").innerHTML = stylesDeg;
            });
        }

        var _container = jQuery("#editor");
        if (_container.length > 0) {
            loadScript(plugin_path + 'ckeditor/ckeditor.js', function () {
                if (CKEDITOR.env.ie && CKEDITOR.env.version < 9) {
                    CKEDITOR.tools.enableHtml5Elements(document);
                }
                CKEDITOR.config.height = 350;
                CKEDITOR.config.width = 'auto';
                var initSample = (function () {
                    var wysiwygareaAvailable = isWysiwygareaAvailable(), isBBCodeBuiltIn = !!CKEDITOR.plugins.get('bbcode');
                    return function () {
                        var editorElement = CKEDITOR.document.getById('editor');
                        if (isBBCodeBuiltIn) {
                            editorElement.setHtml('Hello world!\n\n' + 'I\'m an instance of [url=https://ckeditor.com]CKEditor[/url].');
                        }
                        if (wysiwygareaAvailable) {
                            CKEDITOR.replace('editor');
                        } else {
                            editorElement.setAttribute('contenteditable', 'true');
                            CKEDITOR.inline('editor');
                        }
                    };

                    function isWysiwygareaAvailable() {
                        if (CKEDITOR.revision == ('%RE' + 'V%')) {
                            return true;
                        }
                        return !!CKEDITOR.plugins.get('wysiwygarea');
                    }
                })();
                initSample();
            });
        }
    }

var App = function () {
  "use strict"
  return {
    init: function () {
        this.initComponent()
    },
    BeforeDocumentReady: function () {
      pvrWriteCopyrights()
    },
    initComponent: function () {
      pvrWriteCopyrights();
      mainApplication();
      pvrCountJS();
      pvrTypeitJS();
      // _chat_popup();
      // _live_customizer();
      _url_parameters_ui_elements();
      _UI_elements();
      _showSwal();
      _MultiLevelMenu();
      _cookie_bar();
      _instafeed();
      _email_page();
      _validation();
      _date_time();
    }
  }
}();

App.BeforeDocumentReady();

$(function () {
    App.init();
});