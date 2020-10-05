
from odoo import http
from odoo.http import request


class Main(http.Controller):
    @http.route('/library/books', type='http', auth='group_librarian')
    def books(self):
        books = request.env['library.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s %s </li>" % (book.name, book.id)
        html_result += '</ul></body></html>'
        return html_result

    @http.route('/library/books/json', type='json', auth='none')
    def books_json(self):
        records = request.env['library.book'].sudo().search([])
        return records.read(['name'])

    @http.route('/library/book_details', type='http', auth='none')
    def book_details(self, book_id):
        record = request.env['library.book'].sudo().browse(int(book_id))
        return u'<html><body><h1>%s</h1>Authors: %s' % (
            record.name,
            u', '.join(record.author_ids.mapped('name')) or 'none',
        )

    @http.route("/library/book_details/<int:book>", type='http', auth='none')
    def book_details_in_path(self, book):
        return self.book_details(book)