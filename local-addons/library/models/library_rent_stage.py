
from odoo import models, fields


class LibraryRentStage(models.Model):
    _name = 'library.rent.stage'
    _description = 'Library Rent Stage'
    _order = 'sequence, name'

    name = fields.Char()
    sequence = fields.Integer()
    fold = fields.Boolean()
    book_state = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')
    ], 'State', default='available')