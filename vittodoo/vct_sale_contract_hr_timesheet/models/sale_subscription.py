# -*- coding: utf-8 -*-

'''
Created on 24 juin 2017

@author: heifara
'''

import logging

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from time import sleep

_logger = logging.getLogger(__name__)

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    recurring_next_total_amount = fields.Float(string='Total Amount of Next Invoice', compute="compute_recurring_next_total_amount", store=True)
    alert_niv1_sent = fields.Boolean(string="Alert niv 1 sent to customer", help="If checked, then the alert has been sent")
    alert_niv2_sent = fields.Boolean(string="Alert niv 2 sent to customer", help="If checked, then the alert has been sent")

    @api.multi
    def _prepare_invoice_data(self):
        resultat = super(SaleSubscription, self)._prepare_invoice_data()
        del resultat["user_id"]
        return resultat

    @api.one
    def compute_recurring_next_total_amount(self):
        recurring_next_date = self.recurring_next_date
        invoices = self._recurring_create_invoice()
        #self.recurring_invoice_with_timesheets(invoices, True)
        self._recurring_create_invoice()
        for invoice in invoices:
            self.recurring_next_total_amount = invoice.amount_total
            invoice.unlink()
        self.write({'recurring_next_date': recurring_next_date})

    @api.multi
    def alert(self):
        sale_subscriptions = self.env['sale.subscription'].search([('state', '=', 'open')])
        for sale_subscription in sale_subscriptions:
            sale_subscription.compute_recurring_next_total_amount()

        # Template for email sending
        template = self.env.ref('vct_sale_contract_hr_timesheet.sale_subscription_alert_mail_template')
        mail_template = self.env['mail.template'].browse(template.id)

        # Alert niv1
        sale_subscriptions = self.env['sale.subscription'].search([('state', '=', 'open'),
                                                                   ('template_id.enable_alert', '=', 'True'),
                                                                   ('recurring_next_total_amount', '>', 50000)])
        for sale_subscription in sale_subscriptions:
            if not sale_subscription.alert_niv1_sent:
                mail_template.send_mail(sale_subscription.id)
                sale_subscription.alert_niv1_sent = True
            else:
                _logger.info("Alert niv1 already sent for " + str(sale_subscription.display_name))

        # Alert niv2
        sale_subscriptions = self.env['sale.subscription'].search([('state', '=', 'open'),
                                                                   ('template_id.enable_alert', '=', 'True'),
                                                                   ('recurring_next_total_amount', '>', 90000)])
        for sale_subscription in sale_subscriptions:
            if not sale_subscription.alert_niv2_sent:
                mail_template.send_mail(sale_subscription.id)
                sale_subscription.alert_niv2_sent = True
            else:
                _logger.info("Alert niv2 already sent for " + str(sale_subscription.display_name))

    # @override SaleSubscription._cron_recurring_create_invoice
    @api.model
    def _cron_recurring_create_invoice(self):
        invoice_ids = self._recurring_create_invoice(automatic=True)
        self.recurring_invoice_with_timesheets(invoice_ids)

        for item in self:
            item.recurring_next_total_amount = 0.0
            item.alert_niv1_sent = False
            item.alert_niv2_sent = False
        return invoice_ids

    # @override SaleSubscription.recurring_invoice()
    # @see sale_contract.models.sale_subscription: SaleSubscription.recurring_invoice()
    @api.multi
    def recurring_invoice(self):
        invoice_ids = self._recurring_create_invoice()
        self.recurring_invoice_with_timesheets(invoice_ids)
        self.recurring_next_total_amount = 0.0
        self.alert_niv1_sent = False
        self.alert_niv2_sent = False
        return self.action_subscription_invoice()

    def recurring_invoice_with_timesheets(self, invoice_ids, simulation=False):
        for invoice_id in invoice_ids:
            invoice_lines = self.env['account.invoice.line'].search([('invoice_id', '=', invoice_id.id)])
            for invoice_line in invoice_lines:
                if invoice_line.product_id.invoice_policy == 'order':
                    _logger.info("nothing to do for now")

                elif invoice_line.product_id.invoice_policy == 'delivery':
                    _logger.info("is a delivery")
                    print("DELIVERY")

                    # Init variables
                    amount = 0.0
                    unit = self.env.ref('product.product_uom_hour')
                    invoice_line.quantity = 0;

                    # Run throught the billable timesheets
                    billable_timesheet_ids = self.env['account.analytic.line'].search([('project_id', '!=', False), ('account_id', '=', self.analytic_account_id.id), ('product_id', '=', invoice_line.product_id.id), ('invoice', '=', False)])
                    print("BILLABLE TIMESHEET: " + str(billable_timesheet_ids))
                    for billable_timesheet in billable_timesheet_ids:
                        if simulation:
                            amount += billable_timesheet.unit_amount
                        else:
                            billable_timesheet.invoice = invoice_id
                            billable_timesheet.billed_amount = billable_timesheet.unit_amount
                            if self.template_id.reset_timesheet_duration_on_invoice:
                                billable_timesheet.unit_amount = 0.0
                            amount += billable_timesheet.billed_amount

                    # Convert timesheet's amount in hour into invoice_line uom
                    invoice_line.quantity = unit._compute_quantity(amount, invoice_line.uom_id, False)

                else:
                    _logger.warn("Product is either not on order or delivery")

            invoice = self.env['account.invoice'].browse([invoice_id])
            #invoice.compute_taxes()
            #invoice._compute_amount()

        return self.action_subscription_invoice()


class SaleSubscriptionTemplate(models.Model):
    _inherit = "sale.subscription.template"

    reset_timesheet_duration_on_invoice = fields.Boolean(String='Reset timesheet duration on invoice', help='if checkd, when invoice is generated, the duration of all timesheet is set to 0', default=True)
    enable_alert = fields.Boolean(String='Enable Alert on Next Invoice', help='If checked, an alert will be generated', default=False)
