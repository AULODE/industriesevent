# -*- coding: utf-8 -*-
from odoo.http import request
from datetime import datetime, timedelta, time
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController
from odoo.exceptions import UserError
import pytz
from pytz import timezone
from dateutil.relativedelta import relativedelta
from babel.dates import format_datetime, format_date
from werkzeug.urls import url_encode
from odoo import http, _, fields
from odoo.tools import html2plaintext, DEFAULT_SERVER_DATETIME_FORMAT as dtf
from odoo.tools.misc import get_lang

class WebsiteEventSaleController(WebsiteEventSaleController):

	@http.route(['/event/meetings/<model("event.event"):ev_id>'], type='http', auth="public", website=True)
	def meeting_list(self, ev_id, **post):
		events_meetings = request.env['calendar.event'].sudo().search([
			('event_id','=',ev_id.id),('partner_ids','in',[request.env.user.partner_id.id])])
		values = {'events_meetings' :events_meetings }
		return request.render("event_attendee_meeting.event_meetings", values)

	@http.route(['/meeting/completed/<model("calendar.event"):ev_id>'], type='http', auth="public", website=True)
	def meeting_done(self, ev_id, **post):
		ev_id.write({'completed':True})
		for partner in ev_id.partner_ids :
			template_id = request.env['ir.model.data'].get_object_reference('event_attendee_meeting', 'meeting_done_email_template')[1]
			email_template_obj = request.env['mail.template'].browse(template_id)
			values = email_template_obj.generate_email(ev_id.id)
			values['email_from'] =request.env.company.email or requests.env.user.email_formatted
			values['email_to'] = partner.email
			values['author_id'] = request.env.user.partner_id.id
			values['subject'] = 'FeedBack for : '+ev_id.name
			values['body_html'] = 'Hello :'+partner.name+' How is your experiance of meeting: '+ev_id.name
			mail_mail_obj = request.env['mail.mail']
			msg_id = mail_mail_obj.sudo().create(values)
			if msg_id:
				mail_mail_obj.send([msg_id])
		return request.render("event_attendee_meeting.complete_meeting_success")

	@http.route(['/event/attendees/<model("event.event"):ev_id>'], type='http', auth="public", website=True)
	def attendees_list(self, ev_id, **post):
		registrations = ev_id.registration_ids
		start_date = ev_id.date_begin.strftime('%Y-%m-%d')
		end_date = ev_id.date_end.strftime('%Y-%m-%d')
		values = {'registrations' :registrations,
				'start_date':start_date,
				'end_date':end_date,
		 }
		return request.render("event_attendee_meeting.attendees", values)

	@http.route(['/create/attendee/meeting'], type='http',methods=['POST'], auth="public", website=True)
	def attendees_meeting(self, **post):
		dt = post.get('reg_time')
		dt_end = post.get('reg_end_time')
		rec_id = post.get('reg_record')
		if dt and dt_end and rec_id:
			user_tz = request._context.get('tz')
			datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
			# timezone = request.session['timezone']
			tz_session = pytz.timezone(user_tz)
			date_start = tz_session.localize(fields.Datetime.from_string(dt)).astimezone(pytz.utc)
			date_end = tz_session.localize(fields.Datetime.from_string(dt_end)).astimezone(pytz.utc)
			reg_rec = request.env['event.registration'].sudo().browse(int(rec_id))
			
			request.env['calendar.event'].sudo().create({
				'name': 'meeting with :'+ str(request.env.user.partner_id.name),
				'description': post.get('meeting_desc'),
				'start': date_start.strftime(dtf),
				'start_date': date_start.strftime(dtf),
				'start_datetime': date_start.strftime(dtf),
				'stop': date_end.strftime(dtf),
				'stop_datetime': date_end.strftime(dtf),
				'allday': False,
				# 'start': fields.Datetime.to_string(datetime_object),
				# 'stop': fields.Datetime.to_string(datetime_object + timedelta(hours=1)),
				'user_id': request.env.user.id,
				'partner_ids': [(6,0,[request.env.user.partner_id.id,reg_rec.partner_id.id])],
				'event_reg_id' : reg_rec.id,
				'event_id' : reg_rec.event_id.id,
			})

			return request.render("event_attendee_meeting.created_meeting_success")