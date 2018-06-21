"use strict";
var v2 = function () {
    "use strict";
    var ch1 = new Rickshaw.Graph({
        element : document.querySelector('#ch1'),
        renderer: 'area',
        max     : 80,
        series  : [ {
            data : [
                {x: 0, y: 40},
                {x: 1, y: 49},
                {x: 2, y: 38},
                {x: 3, y: 30},
                {x: 4, y: 32},
                {x: 5, y: 40},
                {x: 6, y: 20},
                {x: 7, y: 10},
                {x: 8, y: 20},
                {x: 9, y: 25},
                {x: 10, y: 35},
                {x: 11, y: 20},
                {x: 12, y: 40}
            ],
            color: 'rgba(255,255,255,0.5)'
        } ]
    });
    ch1.render();

    // Responsive Mode
    new ResizeSensor($('.br-mainpanel'), function () {
        ch1.configure({
            width : $('#ch1').width(),
            height: $('#ch1').height()
        });
        ch1.render();
    });


    var ch2 = new Rickshaw.Graph({
        element : document.querySelector('#ch2'),
        renderer: 'area',
        max     : 80,
        series  : [ {
            data : [
                {x: 0, y: 40},
                {x: 1, y: 15},
                {x: 2, y: 38},
                {x: 3, y: 40},
                {x: 4, y: 32},
                {x: 5, y: 50},
                {x: 6, y: 65},
                {x: 7, y: 70},
                {x: 8, y: 45},
                {x: 9, y: 55},
                {x: 10, y: 60},
                {x: 11, y: 50},
                {x: 12, y: 40}
            ],
            color: 'rgba(255,255,255,0.5)'
        } ]
    });
    ch2.render();

    // Responsive Mode
    new ResizeSensor($('.br-mainpanel'), function () {
        ch2.configure({
            width : $('#ch2').width(),
            height: $('#ch2').height()
        });
        ch2.render();
    });


    var ch3 = new Rickshaw.Graph({
        element : document.querySelector('#ch3'),
        renderer: 'area',
        max     : 80,
        series  : [ {
            data : [
                {x: 0, y: 40},
                {x: 1, y: 45},
                {x: 2, y: 30},
                {x: 3, y: 40},
                {x: 4, y: 50},
                {x: 5, y: 40},
                {x: 6, y: 20},
                {x: 7, y: 10},
                {x: 8, y: 20},
                {x: 9, y: 25},
                {x: 10, y: 35},
                {x: 11, y: 20},
                {x: 12, y: 40}
            ],
            color: 'rgba(255,255,255,0.5)'
        } ]
    });
    ch3.render();

    // Responsive Mode
    new ResizeSensor($('.br-mainpanel'), function () {
        ch3.configure({
            width : $('#ch3').width(),
            height: $('#ch3').height()
        });
        ch3.render();
    });

    var ch4 = new Rickshaw.Graph({
        element : document.querySelector('#ch4'),
        renderer: 'area',
        max     : 80,
        series  : [ {
            data : [
                {x: 0, y: 40},
                {x: 1, y: 45},
                {x: 2, y: 30},
                {x: 3, y: 40},
                {x: 4, y: 50},
                {x: 5, y: 40},
                {x: 6, y: 20},
                {x: 7, y: 10},
                {x: 8, y: 20},
                {x: 9, y: 25},
                {x: 10, y: 35},
                {x: 11, y: 20},
                {x: 12, y: 40}
            ],
            color: 'rgba(255,255,255,0.5)'
        } ]
    });
    ch4.render();

    // Responsive Mode
    new ResizeSensor($('.br-mainpanel'), function () {
        ch4.configure({
            width : $('#ch4').width(),
            height: $('#ch4').height()
        });
        ch4.render();
    });

    $('#spark1').sparkline('html', {
        type         : 'bar',
        barWidth     : 8,
        height       : 30,
        barColor     : '#695bd8',
        chartRangeMax: 12
    });

    $('#spark2').sparkline('html', {
        type         : 'bar',
        barWidth     : 8,
        height       : 30,
        barColor     : '#19c4b8',
        chartRangeMax: 12
    });

    $('#spark3').sparkline('html', {
        type         : 'bar',
        barWidth     : 8,
        height       : 30,
        barColor     : '#b24ca8',
        chartRangeMax: 12
    });

    $('#spark4').sparkline('html', {
        type         : 'bar',
        barWidth     : 8,
        height       : 30,
        barColor     : '#fa740f',
        chartRangeMax: 12
    });

    if ($("#sales_chart").length) {
        var ctx = document.getElementById('sales_chart').getContext('2d');
        var myBarChart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'bar',

            // The data for our dataset
            data: {
                labels  : [ "Bitcoin", "Ethereum", "Ripple", "BTC Cash", "Litecoin" ],
                datasets: [ {
                    label               : "Bitcoin",
                    data                : [ 40, 90, 210, 160, 230 ],
                    backgroundColor     : '#ffa534',
                    borderColor         : '#ffa534',
                    pointBorderColor    : '#ffffff',
                    pointBackgroundColor: '#ffa534',
                    pointBorderWidth    : 2,
                    pointRadius         : 4

                }, {
                    label               : "My Second dataset",
                    data                : [ 160, 140, 20, 270, 110 ],
                    backgroundColor     : '#3d74f1',
                    borderColor         : '#3d74f1',
                    pointBorderColor    : '#ffffff',
                    pointBackgroundColor: '#3d74f1',
                    pointBorderWidth    : 2,
                    pointRadius         : 4
                } ]
            },

            // Configuration options go here
            options: {
                maintainAspectRatio: false,
                legend             : {
                    display: false
                },

                scales  : {
                    xAxes: [ {
                        display  : true,
                        gridLines: {
                            zeroLineColor     : '#e7ecf0',
                            color             : '#e7ecf0',
                            borderDash        : [ 5, 5, 5 ],
                            zeroLineBorderDash: [ 5, 5, 5 ],
                            drawBorder        : false
                        }
                    } ],
                    yAxes: [ {
                        display  : true,
                        gridLines: {
                            zeroLineColor     : '#e7ecf0',
                            color             : '#e7ecf0',
                            borderDash        : [ 5, 5, 5 ],
                            zeroLineBorderDash: [ 5, 5, 5 ],
                            drawBorder        : false
                        }
                    } ]

                },
                elements: {
                    line : {
                        tension    : 0.00001,
//              tension: 0.4,
                        borderWidth: 1
                    },
                    point: {
                        radius     : 2,
                        hitRadius  : 10,
                        hoverRadius: 6,
                        borderWidth: 4
                    }
                }
            }
        });
    }
};
var Dashboard = function () {
    "use strict";
    return {
        init: function () {
            v2();
        }
    }
}();
$(function () {
    Dashboard.init();
});