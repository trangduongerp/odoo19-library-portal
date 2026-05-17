{
    'name': 'Library Portal',
    'version': '1.0',
    'summary': 'Website Library Portal Management',
    'description': """
Library Portal Module
=====================

Features:
---------
- Manage library books
- Borrow request management
- Website book list
- Book detail page
- Borrow form
- JSON API for mobile/frontend
""",

    'author': 'Trang Duong',
    'website': 'http://localhost:8069',

    'category': 'Website',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'website',
    ],

    'data': [

        # Security
        'security/ir.model.access.csv',

        # Backend Views
        'views/book_views.xml',
        'views/borrow_request_views.xml',

        # Website Templates
        'views/templates.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}