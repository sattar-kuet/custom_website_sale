from odoo import models, fields, api, exceptions
import json
import requests


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    delivery_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('packaging_done', 'Packaging Done'),
        ('on_the_way', 'On the way'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ],
        default='pending',
        track_visibility='always'
    )
    customer_phone = fields.Char('Customer Phone', compute='_compute_customer_phone', store=False)

    @api.depends('partner_id')
    def _compute_customer_phone(self):
        for record in self:
            if record.partner_shipping_id:
                record.customer_phone = record.partner_shipping_id.phone
            else:
                record.customer_phone = False

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        return order

    def action_confirmed(self):
        # for record in self:
        #     # if record.delivery_status != 'pending':
        #     #     raise exceptions.UserError("Status of all parcel must be 'Pending'")
        for record in self:
            customer = record.partner_shipping_id
            print('*' * 100, customer.phone)
            message = f"প্রিয় {customer.name}, আপনার অর্ডার টি গ্রহন করা হয়েছে। nilkhet24.com এর সাথে থাকার জন্য ধন্যবাদ।"
            response = self.env['custom_website_sale.helper'].send_normal_sms(customer.phone, message)
            print(response.text)

    def action_packaging_done(self):
        for record in self:
            if record.delivery_status != 'confirmed':
                raise exceptions.UserError("Status of all parcel must be 'Confirmed'")
        for record in self:
            record.delivery_status = 'packaging_done'

    def action_on_the_way(self):
        for record in self:
            if record.delivery_status != 'packaging_done':
                raise exceptions.UserError("Status of all parcel must be 'Packaging Done'")
        for record in self:
            record.delivery_status = 'on_the_way'

    def action_delivered(self):
        for record in self:
            if record.delivery_status != 'on_the_way':
                raise exceptions.UserError("Status of all parcel must be 'On the way'")
        for record in self:
            record.delivery_status = 'delivered'
