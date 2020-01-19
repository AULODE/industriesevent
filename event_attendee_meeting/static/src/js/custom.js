odoo.define('event_attendee_meeting.events', function(require) {
	"use strict";
	require('web.dom_ready');
	var core = require('web.core');
	var time = require('web.time');
	var ajax = require('web.ajax');

	var _t = core._t;

	$(document).ready(function() {
		$(document).on("click", ".open-meeting", function () {
			$(".modal-body .attendee_name").text($(this).parent().parent().find('.a_name').text() );
			// $(".modal-body .attendee_email").text($(this).parent().parent().find('.a_email').text() );
			$('.reg_record').val( $(this).attr('id'));
			var st_date = $('.start_date').text().split('-');
			var end_date = $('.end_date').text().split('-');
			var datetimepickerFormat = time.getLangDatetimeFormat();
			$('#raghav' ).datetimepicker({
				minDate: new Date(parseInt(st_date[0]), parseInt(st_date[1])-1, parseInt(st_date[2])),
				maxDate: new Date(parseInt(end_date[0]), parseInt(end_date[1])-1, parseInt(end_date[2])),
				// setDate: new Date(2014, 10, 30)
				// format : datetimepickerFormat,
				// disabledDates: disabledDates,
				useCurrent: false,
				format: 'YYYY-MM-DD HH:mm:ss',
				viewDate: moment(new Date()).hours(0).minutes(0).seconds(0).milliseconds(0),
				calendarWeeks: true,
				icons: {
					time: 'fa fa-clock-o',
					date: 'fa fa-calendar',
					next: 'fa fa-chevron-right',
					previous: 'fa fa-chevron-left',
					up: 'fa fa-chevron-up',
					down: 'fa fa-chevron-down',
				},
				locale : moment.locale(),
				allowInputToggle: true,
				keyBinds: null,
			});

			$('#end_date_pck' ).datetimepicker({
				minDate: new Date(parseInt(st_date[0]), parseInt(st_date[1])-1, parseInt(st_date[2])),
				maxDate: new Date(parseInt(end_date[0]), parseInt(end_date[1])-1, parseInt(end_date[2])),
				// setDate: new Date(2014, 10, 30)
				// format : datetimepickerFormat,
				// disabledDates: disabledDates,
				useCurrent: false,
				format: 'YYYY-MM-DD HH:mm:ss',
				viewDate: moment(new Date()).hours(0).minutes(0).seconds(0).milliseconds(0),
				calendarWeeks: true,
				icons: {
					time: 'fa fa-clock-o',
					date: 'fa fa-calendar',
					next: 'fa fa-chevron-right',
					previous: 'fa fa-chevron-left',
					up: 'fa fa-chevron-up',
					down: 'fa fa-chevron-down',
				},
				locale : moment.locale(),
				allowInputToggle: true,
				keyBinds: null,
			});

		});


		
		$( ".meeting_time" ).focusout(function() {
			$('.reg_time').val($('.meeting_time').val());		
		})
		$( ".meeting_end_time" ).focusout(function() {
			$('.reg_end_time').val($('.meeting_end_time').val());		
		})

		$(document).on("click", ".create_meeting", function () {
			if($('.datetimepicker-input').val() == '')
			{
				alert('Please select date and time to schedule meeting')
			}
			else if($('.meeting_desc').val() == '')
			{
				alert('Please add subject for which you want to schedule meeting')
			}
			else{

			}
		});
	});
}); 
