from odoo import models, fields


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Library Member'

    _sql_constraints = [
        ('member_number_unique',
         'UNIQUE (member_number)',
         'Member number must be unique')
    ]

    # partner_id = fields.Many2one('res.partner', ondelete='cascade', delegate=True) -> _inherits is not needed
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char(required=True)
    date_of_birth = fields.Date('Date of birth')
