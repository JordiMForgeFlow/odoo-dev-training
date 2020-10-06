# -*- coding: utf-8 -*-
{
    'name': "Simple Library",  # Module title
    'summary': "Manage books easily",  # Module subtitle phrase
    'description': """Long description""",  # You can also rst format
    'author': "JordiMForgeFlow",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '13.5.1.0.0',
    'depends': ['base', 'web'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'views/simple_library_assets.xml'
    ],
}
