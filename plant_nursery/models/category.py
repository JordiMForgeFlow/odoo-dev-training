
from odoo import models, fields


class Category(models.Model):
    _name = 'nursery.plant.category'
    _description = 'Plant Category'
    _order = 'name'

    name = fields.Char('Name', required=True)