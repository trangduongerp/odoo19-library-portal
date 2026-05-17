from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    """Model quản lý sách thư viện."""

    _name = 'library.book'
    _description = 'Library Book'
    _order = 'name asc'

    name = fields.Char(
        string='Tên sách',
        required=True
    )

    author = fields.Char(
        string='Tác giả'
    )

    isbn = fields.Char(
        string='Mã ISBN'
    )

    quantity = fields.Integer(
        string='Số lượng',
        default=1
    )

    description = fields.Text(
        string='Mô tả'
    )

    image = fields.Image(
        string='Ảnh bìa'
    )

    state = fields.Selection(
        [
            ('available', 'Available'),
            ('out_of_stock', 'Out of Stock')
        ],
        string='Trạng thái',
        compute='_compute_state',
        store=True
    )

    _sql_constraints = [
        (
            'isbn_unique',
            'UNIQUE(isbn)',
            'Mã ISBN phải là duy nhất!'
        )
    ]

    @api.depends('quantity')
    def _compute_state(self):
        """Tự động cập nhật trạng thái sách."""
        for rec in self:
            rec.state = (
                'available'
                if rec.quantity > 0
                else 'out_of_stock'
            )

    @api.constrains('quantity')
    def _check_quantity(self):
        """Không cho phép số lượng âm."""
        for rec in self:
            if rec.quantity < 0:
                raise ValidationError(
                    'Số lượng không được âm!'
                )