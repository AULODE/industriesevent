# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, timedelta

class CalendarEvent(models.Model):
	_inherit="calendar.event"

	STATE_SELECTION = [
		('needsAction', 'Needs Action'),
		('tentative', 'Uncertain'),
		('declined', 'Declined'),
		('accepted', 'Accepted'),
	]

	event_reg_id = fields.Many2one('event.registration',string="Event registration")
	event_id = fields.Many2one('event.event',string='Event')
	completed = fields.Boolean(string='Completed')
	other_attendee_status = fields.Selection(STATE_SELECTION, string='Other Attendee Status',compute='_compute_attendee_status')
	other_attendee = fields.Many2one('res.partner',string='Other Attendee',compute='_compute_attendee_status')

	@api.depends('attendee_ids')
	def _compute_attendee_status(self):
		for rec in self:
			rec.other_attendee_status = 'needsAction'
			rec.other_attendee = False
			if rec.event_id:
				for att in rec.attendee_ids :
					if att.partner_id.id != rec.user_id.partner_id.id :
						rec.other_attendee = att.partner_id
						rec.other_attendee_status = att.state
				


class AttendeeMeeting(models.Model):
	_name = 'attendee.meeting'
	_description = "Attendee Meetingss"
	_rec_name = 'partner_id'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

	partner_id = fields.Many2one('res.partner',string="Partner")
	subject = fields.Text(string="Subject")
	time = fields.Datetime(string="Time")
	state = fields.Selection([('draft','New'),('accept','Accept'),('decline','Decline'),('rescheduled','Rescheduled')],string="State",default='draft')
	parent_id = fields.Many2one('attendee.meeting',string="Previous proposal")
	event_reg_id = fields.Many2one('event.registration',string="Event registration")
	event_id = fields.Many2one('event.event',string='Event',related="event_reg_id.event_id")
	sender_id = fields.Many2one('res.partner',string="Sender ")



class EventRegistation(models.Model):
	_inherit = 'event.registration'

	meeting_count = fields.Float(string='Meetings', compute='_compute_meetings')

	def _compute_meetings(self):
		for rec in self:
			rec.meeting_count = self.env['calendar.event'].search_count([('event_reg_id', '=', rec.id)])

	def action_view_meetings(self):
		return {
			'name': _('View  Meetings'),
			'type': 'ir.actions.act_window',
			'view_mode': 'tree,form',
			'res_model': 'calendar.event',
			'domain': [('event_reg_id', '=', self.id)],
		}
	
class EventEvent(models.Model):
	_inherit = 'event.event'

	meeting_count = fields.Float(string='Meetings', compute='_compute_event_meetings')

	def _compute_event_meetings(self):
		for rec in self:
			rec.meeting_count = self.env['calendar.event'].search_count([('event_id', '=', rec.id)])

	def action_view_event_meetings(self):
		return {
			'name': _('View  Meetings'),
			'type': 'ir.actions.act_window',
			'view_mode': 'tree,form',
			'res_model': 'calendar.event',
			'domain': [('event_id', '=', self.id)],
		}