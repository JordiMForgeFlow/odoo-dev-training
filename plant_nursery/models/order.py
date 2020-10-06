
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Order(models.Model):
    _name = 'nursery.order'
    _description = 'Nursery Order'

    name = fields.Char('Reference', default=lambda self:_('New'), required=True, states={'draft': [('readonly', False)]})
    user_id = fields.Many2one('res.users', string='Responsible', index=True, required=True,
                              default=lambda self: self.env.user)
    date_open = fields.Date('Confirmation date', readonly=True)
    customer_id = fields.Many2one('nursery.customer', string='Customer', index=True, required=True)
    line_ids = fields.One2many('nursery.order.line', 'order_id', string='Order Lines')
    amount_total = fields.Float('Amount', compute='_compute_amount_total', store=True)
    company_id = fields.Many2one('res.company', string='Company', related='user_id.company_id',
                                 readonly=True, store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id',
                                  readonly=True, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Opened'),
        ('done', 'Done'),
        ('cancel', 'Canceled')
    ], default='draft', index=True, group_expand="_expand_states")
    last_modification = fields.Datetime(readonly=True)

    @api.depends('line_ids.price')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.mapped('line_ids.price'))

    def action_confirm(self):
        if self.state != 'draft':
            return
        for line in self.line_ids:
            line.plant_id.number_in_stock -= 1
        return self.write({
            'state': 'open',
            'date_open': fields.Datetime.now()
        })

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code('plant.order') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('plant.order') or _('New')
        return super(Order, self).create(vals)

    def write(self, values):
        values['last_modification'] = fields.Datetime.now()
        return super(Order, self).write(values)

    def unlink(self):
        for order in self:
            if order.state == 'confirm':
                raise UserError('You can not delete confirmed orders')
        return super(Order, self).unlink()