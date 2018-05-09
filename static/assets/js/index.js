"use strict";
var v1 = function () {
    "use strict";
    if ($("#pvrLineChart_1").length) {
        var ctx = document.getElementById("chartJsNewUsers");
        if (ctx === null) return;
        ctx = ctx.getContext('2d');

        var gradient = ctx.createLinearGradient(0, 20, 20, 270);
        gradient.addColorStop(0, 'rgba(13,169,239,0.6)');
        gradient.addColorStop(1, 'rgba(13,169,239,0.2)');

        var data = {
            labels  : [
                moment("2017-10-21").format("D MMM"),
                moment("2017-10-22").format("D MMM"),
                moment("2017-10-23").format("D MMM"),
                moment("2017-10-24").format("D MMM"),
                moment("2017-10-25").format("D MMM"),
                moment("2017-10-26").format("D MMM"),
                moment("2017-10-27").format("D MMM"),
            ],
            datasets: [
                {
                    label               : 'New Users',
                    lineTension         : 0,
                    data                : [ 32, 51, 44, 87, 125, 140, 173 ],
                    backgroundColor     : gradient,
                    hoverBackgroundColor: gradient,
                    borderColor         : '#0da9ef',
                    borderWidth         : 2,
                    pointRadius         : 4,
                    pointHoverRadius    : 4,
                    pointBackgroundColor: 'rgba(255,255,255,1)'
                }
            ]
        };

        var chart = new Chart(ctx, {
            type      : 'line',
            data      : data,
            responsive: true,
            options   : {
                maintainAspectRatio: false,
                legend             : {
                    display: false,
                },
                scales             : {
                    xAxes: [ {
                        display  : !1,
                        gridLines: {
                            display       : false,
                            drawBorder    : false,
                            tickMarkLength: 20,
                        },
                        ticks    : {
                            fontColor : "#bbb",
                            padding   : 10,
                            fontFamily: 'Roboto',
                        },
                    } ],
                    yAxes: [ {
                        display  : !1,
                        gridLines: {
                            color        : '#eef1f2',
                            drawBorder   : false,
                            zeroLineColor: '#eef1f2',
                        },
                        ticks    : {
                            fontColor : "#bbb",
                            stepSize  : 50,
                            padding   : 20,
                            fontFamily: 'Roboto',
                        }
                    } ]
                },
            },
        });

        $(window).on('resize', function () {
            chart.resize();
        });
    }

    if ($("#pvrLineChart_1").length) {
        var pvrLineChart = $("#pvrLineChart_1");
        var pvrLineGradient = pvrLineChart[ 0 ].getContext('2d').createLinearGradient(0, 0, 0, 200);
        pvrLineGradient.addColorStop(0, 'rgba(147,104,233,0.48)');
        pvrLineGradient.addColorStop(1, 'rgba(148, 59, 234, 0.7)');
        var liteLineData = {
            labels  : [ "January 1", "January 5", "January 10", "January 15", "January 20", "January 25" ],
            datasets: [ {
                label                    : "Sold",
                fill                     : true,
                lineTension              : 0.4,
                backgroundColor          : pvrLineGradient,
                borderColor              : "#8f1cad",
                borderCapStyle           : 'butt',
                borderDash               : [],
                borderDashOffset         : 0.0,
                borderJoinStyle          : 'miter',
                pointBorderColor         : "#fff",
                pointBackgroundColor     : "#2a2f37",
                pointBorderWidth         : 2,
                pointHoverRadius         : 6,
                pointHoverBackgroundColor: "#943BEA",
                pointHoverBorderColor    : "#fff",
                pointHoverBorderWidth    : 2,
                pointRadius              : 4,
                pointHitRadius           : 5,
                data                     : [ 13, 28, 19, 24, 43, 49 ],
                spanGaps                 : false
            } ]
        };
        var mypvrLineChart = new Chart(pvrLineChart, {
            type   : 'line',
            data   : liteLineData,
            options: {
                tooltips: {
                    enabled: false
                },
                legend  : {
                    display: false
                },
                scales  : {
                    xAxes: [ {
                        display  : false,
                        ticks    : {
                            fontSize : '11',
                            fontColor: '#969da5'
                        },
                        gridLines: {
                            color        : 'rgba(0,0,0,0.0)',
                            zeroLineColor: 'rgba(0,0,0,0.0)'
                        }
                    } ],
                    yAxes: [ {
                        display: false,
                        ticks  : {
                            beginAtZero: true,
                            max        : 55
                        }
                    } ]
                }
            }
        });
    }

    if ($("#pvrLineChart_2").length) {
        var pvrLineChart = $("#pvrLineChart_2");
        var pvrLineGradient = pvrLineChart[ 0 ].getContext('2d').createLinearGradient(0, 0, 0, 200);
        pvrLineGradient.addColorStop(0, 'rgba(255, 165, 52,0.48)');
        pvrLineGradient.addColorStop(1, 'rgba(255, 82, 33, 0.7)');
        var liteLineData = {
            labels  : [ "January 1", "January 5", "January 10", "January 15", "January 20", "January 25" ],
            datasets: [ {
                label                    : "Sold",
                fill                     : true,
                lineTension              : 0.4,
                backgroundColor          : pvrLineGradient,
                borderColor              : "#FFA534",
                borderCapStyle           : 'butt',
                borderDash               : [],
                borderDashOffset         : 0.0,
                borderJoinStyle          : 'miter',
                pointBorderColor         : "#fff",
                pointBackgroundColor     : "#2a2f37",
                pointBorderWidth         : 2,
                pointHoverRadius         : 6,
                pointHoverBackgroundColor: "#FF5221",
                pointHoverBorderColor    : "#fff",
                pointHoverBorderWidth    : 2,
                pointRadius              : 4,
                pointHitRadius           : 5,
                data                     : [ 13, 28, 39, 24, 43, 19 ],
                spanGaps                 : false
            } ]
        };
        var mypvrLineChart = new Chart(pvrLineChart, {
            type   : 'line',
            data   : liteLineData,
            options: {
                tooltips: {
                    enabled: false
                },
                legend  : {
                    display: false
                },
                scales  : {
                    xAxes: [ {
                        display  : false,
                        ticks    : {
                            fontSize : '11',
                            fontColor: '#969da5'
                        },
                        gridLines: {
                            color        : 'rgba(0,0,0,0.0)',
                            zeroLineColor: 'rgba(0,0,0,0.0)'
                        }
                    } ],
                    yAxes: [ {
                        display: false,
                        ticks  : {
                            beginAtZero: true,
                            max        : 55
                        }
                    } ]
                }
            }
        });
    }

    if ($("#pvrLineChart_3").length) {
        var pvrLineChart = $("#pvrLineChart_3");
        var pvrLineGradient = pvrLineChart[ 0 ].getContext('2d').createLinearGradient(0, 0, 0, 200);
        pvrLineGradient.addColorStop(0, 'rgba(135, 203, 22,0.48)');
        pvrLineGradient.addColorStop(1, 'rgba(109, 192, 48, 0.7)');
        var liteLineData = {
            labels  : [ "January 1", "January 5", "January 10", "January 15", "January 20", "January 25" ],
            datasets: [ {
                label                    : "Sold",
                fill                     : true,
                lineTension              : 0.4,
                backgroundColor          : pvrLineGradient,
                borderColor              : "#87CB16",
                borderCapStyle           : 'butt',
                borderDash               : [],
                borderDashOffset         : 0.0,
                borderJoinStyle          : 'miter',
                pointBorderColor         : "#fff",
                pointBackgroundColor     : "#2a2f37",
                pointBorderWidth         : 2,
                pointHoverRadius         : 6,
                pointHoverBackgroundColor: "#6DC030",
                pointHoverBorderColor    : "#fff",
                pointHoverBorderWidth    : 2,
                pointRadius              : 4,
                pointHitRadius           : 5,
                data                     : [ 13, 28, 39, 24, 43, 19 ],
                spanGaps                 : false
            } ]
        };
        var mypvrLineChart = new Chart(pvrLineChart, {
            type   : 'line',
            data   : liteLineData,
            options: {
                tooltips: {
                    enabled: false
                },
                legend  : {
                    display: false
                },
                scales  : {
                    xAxes: [ {
                        display  : false,
                        ticks    : {
                            fontSize : '11',
                            fontColor: '#969da5'
                        },
                        gridLines: {
                            color        : 'rgba(0,0,0,0.0)',
                            zeroLineColor: 'rgba(0,0,0,0.0)'
                        }
                    } ],
                    yAxes: [ {
                        display: false,
                        ticks  : {
                            beginAtZero: true,
                            max        : 55
                        }
                    } ]
                }
            }
        });
    }


    var count = 0;
    var classes = [ "theme_1", "theme_2", "theme_3", "theme_4" ];
    var length = classes.length;
    $(function () {
//        $('.app_chat_w').toggleClass('active');

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

    $('.jQueryEqualHeight').jQueryEqualHeight('.card');
};
var Dashboard = function () {
    "use strict";
    return {
        init: function () {
            v1();
        }
    }
}();
$(function () {
    Dashboard.init();
});