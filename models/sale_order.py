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
    customer_phone = fields.Char('Customer Phone', compute='_compute_customer_phone', store="False")

    def _compute_customer_phone(self):
        for record in self:
            record.customer_phone = record.partner_id.phone

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        return order

    def action_confirmed(self):
        for record in self:
            if record.delivery_status != 'pending':
                raise exceptions.UserError("Status of all parcel must be 'Pending'")
        for record in self:
            record.delivery_status = 'confirmed'

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
