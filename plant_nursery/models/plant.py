
from odoo import models, fields, api
from odoo.exceptions import UserError


class Plant(models.Model):
    _name = 'nursery.plant'
    _description = 'Nursery Plant'

    name = fields.Char('Plant name', required=True)
    price = fields.Float()
    order_ids = fields.One2many('nursery.order', 'plant_id', string='Orders')
    order_count = fields.Integer(compute='_compute_order_count', store=True, string='Total orders')
    number_in_stock = fields.Integer()
    image = fields.Binary('Plant image', attachment=True)

    @api.depends('order_ids')
    def _compute_order_count(self):
        for plant in self:
            plant.order_count = len(plant.order_ids)

    @api.constrains('order_count', 'number_in_stock')
    def _check_available_in_stock(self):
        for plant in self:
            if plant.number_in_stock and plant.number_in_stock < plant.order_count:
                raise UserError('There is only %s %s in stock but %s were sold' % (plant.number_in_stock,
                                plant.name, plant.order_count))
