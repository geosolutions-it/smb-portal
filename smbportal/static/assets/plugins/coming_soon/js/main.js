"use strict";
$(window).load(function () {
    $('.preloader').fadeOut('slow');
});

/**	INIT Function
 *************************************************** **/
function initializeSite() {
    "use strict";
    //OUTLINE DIMENSION AND CENTER
    (function () {
        function centerInit() {

            var sphereContent = $('.sphere'),
                sphereHeight = sphereContent.height(),
                parentHeight = $(window).height(),
                topMargin = (parentHeight - sphereHeight) / 2;

            sphereContent.css({
                "margin-top": topMargin + "px"
            });

            var heroContent = $('.hero'),
                heroHeight = heroContent.height(),
                heroTopMargin = (parentHeight - heroHeight) / 2;

            heroContent.css({
                "margin-top": heroTopMargin + "px"
            });

        }

        $(document).ready(centerInit);
        $(window).resize(centerInit);
    })();

    // Init effect
    $('#scene').parallax();

};

/**	Document Ready Trigger
 *************************************************** **/
$(window).on("load", function () {
    initializeSite();
    (function () {
        setTimeout(function () {
            window.scrollTo(0, 0);
        }, 0);
    })();

});

Date.prototype.addDays = function(days) {
    this.setDate(this.getDate() + parseInt(days));
    return this;
};

var currentDate = new Date();
/**	Countdown
 *************************************************** **/
$('#countdown').countdown({
    date  : currentDate.addDays(3),
    render: function (data) {
        var el = $(this.el);
        if (data.years !== 0) {
            el.empty().append("<div>" + this.leadingZeros(data.years, 2) + "<span>years</span></div>")
                .append("<div>" + this.leadingZeros(data.days, 2) + " <span>days</span></div>")
                .append("<div>" + this.leadingZeros(data.hours, 2) + " <span>hrs</span></div>")
                .append("<div>" + this.leadingZeros(data.min, 2) + " <span>min</span></div>")
                .append("<div>" + this.leadingZeros(data.sec, 2) + " <span>sec</span></div>");
        } else {
            el.empty().append("<div>" + this.leadingZeros(data.days, 2) + " <span>days</span></div>")
                .append("<div>" + this.leadingZeros(data.hours, 2) + " <span>hrs</span></div>")
                .append("<div>" + this.leadingZeros(data.min, 2) + " <span>min</span></div>")
                .append("<div>" + this.leadingZeros(data.sec, 2) + " <span>sec</span></div>");
        }

    }
});