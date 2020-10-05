
from odoo import models, fields

class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_date_release = fields.Boolean('Manage book release dates', group='base.group_user',
                                        implied_group='library.group_date_release')
    module_note = fields.Boolean('Note')