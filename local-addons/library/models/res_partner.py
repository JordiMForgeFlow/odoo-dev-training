from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    published_book_ids = fields.One2many('library.book', 'publisher_id', string="Published books")
    authored_book_ids = fields.Many2many('library.book', string="Authored books")
    count_books = fields.Integer('Number of authored books', compute='_compute_count_books')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for record in self:
            record.count_books = len(self.authored_book_ids)
