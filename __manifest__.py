{
    'name': 'Website sale Customization',
    'version': '1.0',
    'category': 'Ecommerce',
    'license': 'LGPL-3',
    'author': 'ITscholar',
    'website': 'https://www.itscholarbd.com',
    'depends': ['website_sale','sale'],
    'data': [
        'views/templates.xml'
    ],
    'assets': {
            'web.assets_frontend': [
                'custom_website_sale/static/style.scss',
            ]
    }
}
