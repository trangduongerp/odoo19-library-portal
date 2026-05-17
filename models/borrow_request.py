import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class LibraryBorrowRequest(models.Model):
    """Model quản lý yêu cầu mượn sách."""

    _name = 'library.borrow.request'
    _description = 'Borrow Request'
    _order = 'request_date desc'

    name = fields.Char(
        string='Tên người mượn',
        required=True
    )

    email = fields.Char(
        string='Email',
        required=True
    )

    phone = fields.Char(
        string='Số điện thoại'
    )

    book_id = fields.Many2one(
        'library.book',
        string='Sách mượn',
        required=True,
        ondelete='restrict'
    )

    request_date = fields.Datetime(
        string='Ngày yêu cầu',
        default=fields.Datetime.now
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('rejected', 'Rejected')
        ],
        string='Trạng thái',
        default='draft'
    )

    @api.constrains('email')
    def _check_email(self):
        """Validate email."""
        pattern = r'^[^@]+@[^@]+\.[^@]+$'

        for rec in self:
            if rec.email and not re.match(pattern, rec.email):
                raise ValidationError(
                    'Email không hợp lệ!'
                )

    def action_confirm(self):
        """Xác nhận yêu cầu mượn sách."""
        for rec in self:

            if rec.book_id.quantity <= 0:
                raise UserError(
                    'Sách đã hết, không thể xác nhận!'
                )

            rec.book_id.quantity -= 1
            rec.state = 'confirmed'

    def action_reject(self):
        """Từ chối yêu cầu."""
        self.state = 'rejected'