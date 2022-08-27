odoo.define('attendance_break.greeting_message_inherit', function (require) {
    "use strict";

    // var AbstractAction = require('web.AbstractAction');
    // var core = require('web.core');
    var time = require('web.time');

    // var _t = core._t;

    var greeting_message_inherit = require('hr_attendance.greeting_message');
    greeting_message_inherit.include({
        init: function (parent, action) {
            this.attendance = action.attendance;
            this.attendance.check_in_break = this.attendance.check_in_break && moment.utc(this.attendance.check_in_break).local();
            this.attendance.check_out_break = this.attendance.check_out_break && moment.utc(this.attendance.check_out_break).local();

            this.format_time = time.getLangTimeFormat();
            this.attendance.check_in_break_time = this.attendance.check_in_break && this.attendance.check_in_break.format(this.format_time);
            this.attendance.check_out_break_time = this.attendance.check_out_break && this.attendance.check_out_break.format(this.format_time);

            this._super(parent, action);

            // if (action.hours_break) {
            //     var duration = moment.duration(action.hours_break, "horas");
            //     this.hours_break = duration.hours() + ' horas, ' + duration.minutes() + ' minutos';
            // }

        },
    });
});
