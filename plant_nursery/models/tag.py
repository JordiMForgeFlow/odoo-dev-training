
from odoo import models, fields


class Tag(models.Model):
    _name = 'nursery.plant.tag'
    _description = 'Plant tag'
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color Index', default=10)