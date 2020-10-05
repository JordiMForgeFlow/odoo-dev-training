from odoo import models, fields, api


class LibraryBookRent(models.Model):
    _name = 'library.book.rent'
    _description = 'Library Book Rent'

    @api.model
    def _default_rent_stage(self):
        Stage = self.env['library.rent.stage']
        return Stage.search([], limit=1)

    book_id = fields.Many2one('library.book', 'Book', required=True)
    borrower_id = fields.Many2one('library.member', 'Borrower', required=True)
    stage_id = fields.Many2one('library.rent.stage', default=_default_rent_stage, group_expand='_group_expand_stages')
    rent_date = fields.Date(default=fields.Date.today())
    return_date = fields.Date(required=True)
    state = fields.Selection([('ongoing', 'Ongoing'), ('returned', 'Returned')],
                             'State', default='ongoing', required=True)
    color = fields.Integer()
    popularity = fields.Selection([
        ('no', 'No Demand'),
        ('low', 'Low Demand'),
        ('medium', 'Average Demand'),
        ('high', 'High Demand')], default='no')
    tag_ids = fields.Many2many('library.rent.tag')

    @api.model
    def _group_expand_stages(self, stages, domain, order):
        return stages.search([], order=order)

    @api.model
    def create(self, vals):
        rent = super(LibraryBookRent, self).create(vals)
        if rent.stage_id.book_state:
            rent.book_id.state = rent.stage_id.book_state
        return rent

    def write(self, vals):
        rent = super(LibraryBookRent, self).write(vals)
        if self.stage_id.book_state:
            self.book_id.state = self.stage_id.book_state
        return rent

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