
from odoo import models, fields
from odoo.exceptions import UserError


class Order(models.Model):
    _name = 'nursery.order'
    _description = 'Nursery Order'

    name = fields.Datetime(default=fields.Datetime.now)
    plant_id = fields.Many2one('nursery.plant', required=True)
    customer_id = fields.Many2one('nursery.customer')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')
    ], 'State', default='draft', group_expand="_expand_states")
    last_modification = fields.Datetime(readonly=True)

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def write(self, values):
        values['last_modification'] = fields.Datetime.now()
        return super(Order, self).write(values)

    def unlink(self):
        for order in self:
            if order.state == 'confirm':
                raise UserError('You can not delete confirmed orders')
        return super(Order, self).unlink()