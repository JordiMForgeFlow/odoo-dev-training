from odoo import models, fields


class LibraryRentWizard(models.TransientModel):
    _name = 'library.rent.wizard'
    _description = 'Wizard: Quick Library Rent'

    borrower_id = fields.Many2one('library.member', string='Borrower', required=True)
    book_ids = fields.Many2many('library.book', string='Books')
    return_date = fields.Date(required=True)

    def add_book_rents(self):
        rentModel = self.env['library.book.rent']
        for wiz in self:
            for book in wiz.book_ids:
                rentModel.create({
                    'book_id': book.id,
                    'borrower_id': wiz.borrower_id.id,
                    'return_date': wiz.return_date
                })
        members = self.mapped('borrower_id')
        action = members.get_formview_action()
        if len(members) > 1:
            action['domain'] = [('id', 'in', tuple(members.ids))]
            action['view_mode'] = 'tree,form'
        return action
