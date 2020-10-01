
from odoo import models, fields


class Customer(models.Model):
    _name = 'nursery.customer'
    _description = 'Nursery Customer'

    name = fields.Char('Customer Name', required=True)
    email = fields.Char(help='To receive the newsletter')