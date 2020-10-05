
from odoo import models, exceptions, http
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_group_librarian(self):
        self._auth_method_user()
        if not request.env.user.has_group('library.group_librarian'):
            raise exceptions.AccessDenied()