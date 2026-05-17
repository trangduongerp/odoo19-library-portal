from odoo import models, fields


class LibraryBorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Borrow Request'

    name = fields.Char()
    email = fields.Char(required=True)
    phone = fields.Char()

    book_id = fields.Many2one(
        'library.book',
        required=True
    )

    request_date = fields.Datetime(
        default=fields.Datetime.now
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected')
    ], default='draft')