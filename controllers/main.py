from odoo import http
from odoo.http import request


class LibraryPortalController(http.Controller):

    @http.route(
        '/library/books',
        type='http',
        auth='public',
        website=True
    )
    def library_books(self, **kwargs):

        books = request.env['library.book'].sudo().search([
            ('state', '=', 'available')
        ])

        return request.render(
            'library_portal.library_books_template',
            {
                'books': books
            }
        )

    @http.route(
        '/library/book/<int:book_id>',
        type='http',
        auth='public',
        website=True
    )
    def library_book_detail(self, book_id, **kwargs):

        book = request.env['library.book'].sudo().browse(book_id)

        if not book.exists():
            return request.not_found()

        return request.render(
            'library_portal.library_book_detail_template',
            {
                'book': book
            }
        )

    @http.route(
        '/library/borrow/<int:book_id>',
        type='http',
        auth='public',
        website=True
    )
    def borrow_form(self, book_id, **kwargs):

        book = request.env['library.book'].sudo().browse(book_id)

        if not book.exists():
            return request.not_found()

        return request.render(
            'library_portal.borrow_form_template',
            {
                'book': book,
                'error': False
            }
        )

    @http.route(
        '/library/borrow/submit',
        type='http',
        auth='public',
        methods=['POST'],
        website=True,
        csrf=True
    )
    def borrow_submit(self, **post):

        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        book_id = post.get('book_id')

        book = request.env['library.book'].sudo().browse(
            int(book_id)
        )

        error = False

        if not name:
            error = 'Tên không được để trống!'

        elif '@' not in email:
            error = 'Email không hợp lệ!'

        elif not book.exists():
            error = 'Sách không tồn tại!'

        elif book.quantity <= 0:
            error = 'Sách đã hết!'

        if error:
            return request.render(
                'library_portal.borrow_form_template',
                {
                    'book': book,
                    'error': error,
                    'form_data': post
                }
            )

        borrow_request = request.env[
            'library.borrow.request'
        ].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
            'book_id': book.id
        })

        return request.redirect(
            '/library/borrow/thank-you?id=%s'
            % borrow_request.id
        )

    @http.route(
        '/library/borrow/thank-you',
        type='http',
        auth='public',
        website=True
    )
    def borrow_thank_you(self, **kwargs):

        request_id = kwargs.get('id')

        borrow_request = request.env[
            'library.borrow.request'
        ].sudo().browse(int(request_id))

        return request.render(
            'library_portal.borrow_thank_you_template',
            {
                'request_obj': borrow_request
            }
        )

    @http.route(
        '/api/library/books',
        type='json',
        auth='public'
    )
    def api_library_books(self):

        books = request.env['library.book'].sudo().search([
            ('state', '=', 'available')
        ])

        data = []

        for book in books:
            data.append({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'quantity': book.quantity
            })

        return data

    @http.route(
        '/api/library/borrow',
        type='json',
        auth='public'
    )
    def api_library_borrow(
        self,
        name,
        email,
        phone,
        book_id
    ):

        book = request.env['library.book'].sudo().browse(
            book_id
        )

        if not book.exists():
            return {
                'success': False,
                'error': 'Sách không tồn tại!'
            }

        if book.quantity <= 0:
            return {
                'success': False,
                'error': 'Sách đã hết!'
            }

        if '@' not in email:
            return {
                'success': False,
                'error': 'Email không hợp lệ!'
            }

        borrow_request = request.env[
            'library.borrow.request'
        ].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
            'book_id': book.id
        })

        return {
            'success': True,
            'request_id': borrow_request.id
        }

    @http.route(
        '/api/library/my-requests',
        type='json',
        auth='user'
    )
    def api_my_requests(self):

        user_email = request.env.user.email

        requests = request.env[
            'library.borrow.request'
        ].sudo().search([
            ('email', '=', user_email)
        ])

        data = []

        for rec in requests:
            data.append({
                'id': rec.id,
                'book_name': rec.book_id.name,
                'request_date': rec.request_date,
                'state': rec.state
            })

        return data