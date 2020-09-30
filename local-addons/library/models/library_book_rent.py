from odoo import models, fields, api


class LibraryBookRent(models.Model):
    _name = 'library.book.rent'
    _description = 'Library Book Rent'

    book_id = fields.Many2one('library.book', 'Book', required=True)
    borrower_id = fields.Many2one('library.member', 'Borrower', required=True)
    state = fields.Selection([('ongoing', 'Ongoing'),
                              ('returned', 'Returned')], 'State', default='ongoing', required=True)
    rent_date = fields.Date(default=fields.Date.today())
    return_date = fields.Date(required=True)

    @api.model
    def create(self, vals):
        book_rec = self.env['library.book'].browse(vals['book_id'])  # returns record set for given id
        book_rec.make_borrowed()
        return super(LibraryBookRent, self).create(vals)

    def book_return(self):
        self.ensure_one()
        self.book_id.make_available()
        self.write({
            'state': 'returned',
            'return_date': fields.Date.today()
        })

    @api.constrains('return_date')
    def _check_release_date(self):
        for record in self:
            if record.return_date and record.return_date < record.rent_date:
                raise models.ValidationError('Return must be later than rent!')