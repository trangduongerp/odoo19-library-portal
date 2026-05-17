from odoo import http
from odoo.http import request


class LibraryController(http.Controller):

    # =========================
    # BOOK LIST
    # =========================
    @http.route(
        '/library/books',
        type='http',
        auth='public',
        website=True
    )
    def book_list(self, **kwargs):

        books = request.env['library.book'].sudo().search([
            ('state', '=', 'available')
        ])

        return request.render(
            'library_portal.book_list_template',
            {
                'books': books
            }
        )

    # =========================
    # BOOK DETAIL
    # =========================
    @http.route(
        '/library/book/<int:book_id>',
        type='http',
        auth='public',
        website=True
    )
    def book_detail(self, book_id, **kwargs):

        book = request.env['library.book'].sudo().browse(book_id)

        if not book.exists():
            return request.not_found()

        return request.render(
            'library_portal.book_detail_template',
            {
                'book': book
            }
        )

    # =========================
    # BORROW FORM GET
    # =========================
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
                'error': '',
            }
        )

    # =========================
    # BORROW FORM POST
    # =========================
    @http.route(
        '/library/borrow/submit',
        type='http',
        auth='public',
        methods=['POST'],
        website=True,
        csrf=True
    )
    def submit_borrow(self, **post):

        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        book_id = int(post.get('book_id'))

        book = request.env['library.book'].sudo().browse(book_id)

        if not name:
            return request.render(
                'library_portal.borrow_form_template',
                {
                    'book': book,
                    'error': 'Name is required'
                }
            )

        if '@' not in email:
            return request.render(
                'library_portal.borrow_form_template',
                {
                    'book': book,
                    'error': 'Invalid email'
                }
            )

        borrow = request.env[
            'library.borrow.request'
        ].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
            'book_id': book_id,
        })

        return request.redirect(
            '/library/borrow/thank-you?id=%s'
            % borrow.id
        )

    # =========================
    # API BOOKS
    # =========================
    @http.route(
        '/api/library/books',
        type='json',
        auth='public'
    )
    def api_books(self):

        books = request.env['library.book'].sudo().search([
            ('state', '=', 'available')
        ])

        result = []

        for book in books:
            result.append({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'quantity': book.quantity,
            })

        return result

    # =========================
    # API BORROW
    # =========================
    @http.route(
        '/api/library/borrow',
        type='json',
        auth='public'
    )
    def api_borrow(
            self,
            name,
            email,
            phone,
            book_id
    ):

        book = request.env[
            'library.book'
        ].sudo().browse(book_id)

        if not book.exists():
            return {
                'success': False,
                'error': 'Book not found'
            }

        if book.quantity <= 0:
            return {
                'success': False,
                'error': 'Out of stock'
            }

        borrow = request.env[
            'library.borrow.request'
        ].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
            'book_id': book_id,
        })

        return {
            'success': True,
            'request_id': borrow.id
        }

    # =========================
    # MY REQUESTS
    # =========================
    @http.route(
        '/api/library/my-requests',
        type='json',
        auth='user'
    )
    def my_requests(self):

        email = request.env.user.email

        requests = request.env[
            'library.borrow.request'
        ].sudo().search([
            ('email', '=', email)
        ])

        result = []

        for r in requests:
            result.append({
                'id': r.id,
                'book': r.book_id.name,
                'state': r.state,
                'request_date': str(r.request_date)
            })

        return result