
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Plant(models.Model):
    _name = 'nursery.plant'
    _description = 'Nursery Plant'

    name = fields.Char('Plant name', required=True)
    description = fields.Html('Description')
    price = fields.Float()
    category_id = fields.Many2one('nursery.plant.category', string='Category')
    tag_ids = fields.Many2many('nursery.plant.tag', string='Tags')
    order_count = fields.Integer(compute='_compute_order_count', string='Total orders')
    number_in_stock = fields.Integer()
    image = fields.Binary('Plant image', attachment=True)
    user_id = fields.Many2one('res.users', string='Responsible', index=True, required=True,
                              default=lambda self: self.env.user)

    def _compute_order_count(self):
        for plant in self:
            plant.order_count = len(self.env['nursery.order.line'].search(['plant_id', '=', plant.id]))

    @api.constrains('number_in_stock')
    def _check_available_in_stock(self):
        for plant in self:
            if plant.number_in_stock < 0:
                raise UserError(_('Stock cannot be negative'))
