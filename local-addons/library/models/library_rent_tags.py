
from odoo import models, fields


class LibraryRentTags(models.Model):
    _name = 'library.rent.tag'
    _description = 'Library Rent Tag'

    name = fields.Char()
    color = fields.Integer()