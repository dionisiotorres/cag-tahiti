# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_event.controllers.main import WebsiteEventController

class WebsiteEventController(WebsiteEventController):

	def _process_registration_details(self, details):
		''' Process data posted from the attendee details form. '''
		registrations = {}
		global_values = {}
		for key, value in details.iteritems():
			if "ticket_id" in key:
				counter, field_name, rest = key.split('-', 2)
			else:
				rest = ""
				counter, field_name = key.split('-', 1)
			if counter == '0':
				global_values[field_name] = value
			else:
				if "ticket_id" in field_name: #Identifie que le champ traité est les tickets
					if (counter in registrations) and ("ticket_id" in registrations.get(counter)):
						ticket_ids = registrations.get(counter)[field_name]
					else:
						registrations.setdefault(counter, dict())[field_name] = []
						ticket_ids = registrations.get(counter)[field_name]
					ticket_ids.append(value)
				else:
					registrations.setdefault(counter, dict())[field_name] = value
		for key, value in global_values.iteritems():
			for registration in registrations.values():
				registration[key] = value

		result = self._process_ticket_ids(registrations)
		return result.values()

	def _process_ticket_ids(self, registrations):
		result = {}
		i = 0
		for key, values in registrations.iteritems():
			if 'ticket_id' in values:
				for ticket_id in values['ticket_id']:
					i = i + 1
					for field_name, value in values.iteritems():
						if "ticket_id" in field_name:
							result.setdefault(i, dict())[field_name] = ticket_id
						else:
							result.setdefault(i, dict())[field_name] = value
		return result
