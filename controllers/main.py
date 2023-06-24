from datetime import datetime

from odoo import http
from odoo.http import request


class PortalCustomer(http.Controller):
    @http.route([
        '''/my/home''',
        '''/my/orders''',
        '''/my/offer''',
    ], type='http', auth="public", website=True)
    def portal_dashboard(self):
        values = {
            'user': {'name': request.env.user.name,
                     'email': request.env.user.email
                     }
        }
        current_url = request.httprequest.path
        if current_url == '/my/home' or current_url == '/my/orders':

            sale_orders = request.env['sale.order'].search([('user_id', '=', request.env.user.id)])

            orders = []
            for sale_order in sale_orders:
                order_lines = sale_order.order_line.filtered(
                    lambda line: not line.is_delivery)  # Retrieve the order lines associated with the sale order
                products = []
                #
                for order_line in order_lines:
                    product = {
                        'name': order_line.product_id.name,
                        # 'image': order_line.product_id.image_128, #TODO
                        'author': order_line.product_id.author_name,
                        'price': order_line.price_unit,
                        'quantity': order_line.product_uom_qty,
                    }
                    products.append(product)
                created_date = sale_order.create_date.strftime('%d %b, %Y')
                order = {
                    'reference': sale_order.reference,
                    'status': sale_order.delivery_status,
                    'products': products,
                    'created_date': created_date,
                    'amount_total': sale_order.amount_total,
                }
                orders.append(order)

            # print("orders >>>>> ????????????????????")
            # print(orders)
            values['orders'] = orders
        return request.render("custom_website_sale.bs_portal_layout", values)
