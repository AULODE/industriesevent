# -*- coding: utf-8 -*-
{
	"name" : "Event's Attendee Meeting Management",
	"version" : "13.19.1.2020",
	"depends" : ['base','web','event','calendar','website_event','website_event_sale'],
	"author": "Kiran",
	"website" : "",
	"category" : "",
	"description": """ Event's Attendee Meeting Management""",
	'summary': "Event's Attendee Meeting Management",
	"currency": 'EUR',
	"data": [
		'security/ir.model.access.csv',
		'data/data.xml',
		'views/events.xml',
		'views/template.xml',
	],
	"auto_install": False,
	"installable": True,
}
