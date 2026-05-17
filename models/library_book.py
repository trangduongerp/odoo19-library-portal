from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(required=True)
    author = fields.Char()
    isbn = fields.Char()
    quantity = fields.Integer(default=1)
    description = fields.Text()
    image = fields.Binary()

    state = fields.Selection([
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock')
    ], default='available')