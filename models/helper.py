import requests
from odoo import models


class Helper(models.AbstractModel):
    _name = 'custom_website_sale.helper'

    def send_normal_sms(self, phone, message):
        pay_load = {
            'token': 'OJfnlVSqaAzgg61dQWOH',
            'phone': phone,
            'message': message
        }
        end_point = 'https://client.itscholarbd.com/sendsms';
        response = requests.post(end_point, data=pay_load)
        return response

    def send_instant_sms(self, phone, message):
        pay_load = {
            'api_key': 'C200874164d372dc69bd12.25597146',
            'type': 'text',
            'contacts': phone,
            'senderid': '8809601011284',
            'msg': message
        }
        end_point = 'https://msg.elitbuzz-bd.com/smsapi';
        response = requests.post(end_point, data=pay_load)
        return response

