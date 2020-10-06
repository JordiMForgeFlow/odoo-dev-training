# -*- coding: utf-8 -*-
{
    'name': "Plant Nursery",

    'summary': "Plants and customers management",

    'author': "JordiMForgeFlow",

    'category': 'Tools',
    'version': '13.5.1.0.0',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/nursery_plant_views.xml',
        'views/nursery_customer_views.xml',
        'views/nursery_order_views.xml',
        'views/nursery_plant_category_views.xml',
        'views/nursery_plant_tag_views.xml',
        'data/ir_sequence_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
