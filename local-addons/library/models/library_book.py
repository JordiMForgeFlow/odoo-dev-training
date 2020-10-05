from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import timedelta

import logging

_logger = logging.getLogger(__name__)


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Abstract Archive'

    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive']
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    _sql_constraints = [
        ('name_unique', 'UNIQUE (name)', 'Book title must be unique.'),
        ('positive_pages', 'CHECK (pages > 0)', 'Number of pages must be positive.')
    ]

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title', translate=True, index=True)
    isbn = fields.Char('ISBN')
    notes = fields.Text('Internal Notes')
    manager_remarks = fields.Text('Manager Remarks')
    state = fields.Selection([
        ('draft', 'Not Available'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')
    ], 'State', default="draft")
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    category_id = fields.Many2one('library.book.category')
    pages = fields.Integer('Number of Pages', groups='base.group_user', states={'lost': [('readonly', True)]},
                           help='Total book page count', company_dependent=False)
    out_of_print = fields.Boolean('Out of print?')
    date_release = fields.Date('Release Date', groups='library.group_date_release')
    date_updated = fields.Datetime('Last Updated', copy=False)
    days_since_release = fields.Float(string="Days Since Release", compute='_compute_days_since_release',
                                      inverse='_inverse_days_since_release', search='_search_days_since_release',
                                      store=False, compute_sudo=False)
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    publisher_city = fields.Char('Publisher City', related='publisher_id.city', readonly=True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    old_edition = fields.Many2one('library.book', string='Old Edition')
    reader_rating = fields.Float('Reader Average Rating', digits=(14,4))
    cost_price = fields.Float('Book Cost', digits='Book Price')

    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary('Retail Price', currency_field='currency_id')

    ref_doc_id = fields.Reference(selection='_referencable_models', string="Reference Document")

    def name_get(self):
        """ This method is used to customize display name of the record """
        result = []
        for record in self:
            authors = record.author_ids.mapped('name')
            rec_name = "%s (%s)" % (record.name, ', '.join(authors))
            result.append((record.id, rec_name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not(name == '' and operator == 'ilike'):
            args += ['|', '|',
                     ('name', operator, name),
                     ('isbn', operator, name),
                     ('author_ids.name', operator, name)]
        return super(LibraryBook, self)._name_search(name=name, args=args, operator=operator, limit=limit,
                                                     name_get_uid=name_get_uid)

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

    @api.depends('date_release')
    def _compute_days_since_release(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                diff = today - book.date_release
                book.days_since_release = diff.days
            else:
                book.days_since_release = 0

    def _inverse_days_since_release(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            diff = today - timedelta(days=book.days_since_release)
            book.date_release = diff

    def _search_days_since_release(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        operator_map = {
            '>': '<', '>=': '<=', '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    def average_book_occupation(self):
        sql_query = """
        SELECT lb.name, avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int
        FROM library_book_rent AS lbr
        JOIN library_book AS lb ON lb.id = lbr.book_id
        WHERE lbr.state = 'returned'
        GROUP BY lb.name;"""
        self.env.cr.execute(sql_query)
        result = self.env.cr.fetchall()
        _logger.info("Average book occupation: %s", result)

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (book.state, new_state)
                raise UserError(msg)

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])

    def change_update_date(self):
        self.ensure_one()
        self.date_updated = fields.Datetime.now()

    @api.model
    def get_author_names(self, books):
        return books.mapped('author_ids.name')

    @api.model
    def sort_books_by_date(self, books):
        return books.sorted(key='date_release')

    def grouped_data(self):
        data = self._get_average_cost()
        _logger.info("Groupped Data %s" % data)

    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            [('cost_price', "!=", False)], #domain
            ['category_id', 'cost_price:avg'], #fields to access
            ['category_id'] #group by
        )
        return grouped_result

    @api.model
    def _update_book_price(self):
        all_books = self.search([])
        for book in all_books:
            book.cost_price += 10

    @api.model
    def create(self, values):
        if not self.user_has_groups('library.group_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify manager remarks'
                )
        return super(LibraryBook, self).create(values)

    def write(self, values):
        if not self.user_has_groups('library.group_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify manager remarks'
                )
        return super(LibraryBook, self).write(values)

