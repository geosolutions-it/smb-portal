"use strict";
var cal = function () {
    "use strict";
    var t = new Date,
        e = t.getFullYear(),
        a = t.getMonth() + 1;
    a = 10 > a ? "0" + a : a, $("#calendar").fullCalendar({
        header      : {
            left  : "month,agendaWeek,agendaDay",
            center: "title",
            right : "prev,today,next "
        },
        droppable   : !0,
        drop        : function () {
            $(this).remove()
        },
        selectable  : !0,
        selectHelper: !0,
        select      : function (t, e) {
            var a, r = swal({
                title           : "Title for " + moment(t._d).format('DD-MM-YYYY'),
                text            : "Write something interesting...",
                type            : "input",
                showCancelButton: true,
                closeOnConfirm  : false,
                inputPlaceholder: "Write something..."
            }, function (inputValue) {
                if (inputValue === false) return false;
                if (inputValue === "") {
                    swal.showInputError("You need to write something!");
                    return false
                }
                (a = {
                    title: inputValue,
                    start: t,
                    end  : e,
                    color: "#9368E9"
                });
                swal("Nice!", "You wrote: " + inputValue, "success");
                $("#calendar").fullCalendar("renderEvent", a, 1);
                $("#calendar").fullCalendar("unselect");
            });
        },
        editable    : !0,
        eventLimit  : !0,
        events      : [ {
            title: "Event 1",
            start: e + "-" + a + "-01",
            color: "#797979"
        }, {
            title: "Event 2",
            start: e + "-" + a + "-07",
            end  : e + "-" + a + "-07",
            color: "#447DF7"
        }, {
            id   : 999,
            title: "Event 3",
            start: e + "-" + a + "-09T16:00:00",
            color: "#23CCEF"
        }, {
            id   : 999,
            title: "Event 4",
            start: e + "-" + a + "-16T16:00:00",
            color: "#87CB16"
        }, {
            title: "Event 5",
            start: e + "-" + a + "-11",
            end  : e + "-" + a + "-11",
            color: "#9368E9"
        }, {
            title: "Event 6",
            start: e + "-" + a + "-12T10:30:00",
            color: "#FFA534"
        }, {
            title: "Event 7",
            start: e + "-" + a + "-25T12:00:00",
            color: "#FF5221"
        }, {
            title: "Event 8",
            start: e + "-" + a + "-05T14:30:00",
            color: "#23CCEF"
        }, {
            title: "Event 9",
            start: e + "-" + a + "-22T17:30:00",
            color: "#9368E9"
        }, {
            title: "Event 10",
            start: e + "-" + a + "-19T20:00:00",
            color: "#FF5221"
        }, {
            title: "Event 11",
            start: e + "-" + a + "-13T07:00:00",
            color: "#9368E9"
        }, {
            title: "Event 12 with URL",
            url  : "http://google.com/",
            start: e + "-" + a + "-03",
            color: "#FF5221"
        } ]
    });
};
var Calendar = function () {
    "use strict";
    return {
        init: function () {
            cal();
        }
    }
}();
$(function () {
    Calendar.init();
});