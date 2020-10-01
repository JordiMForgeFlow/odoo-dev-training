# -*- coding: utf-8 -*-
# from odoo import http


# class PlantNursery(http.Controller):
#     @http.route('/plant_nursery/plant_nursery/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/plant_nursery/plant_nursery/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('plant_nursery.listing', {
#             'root': '/plant_nursery/plant_nursery',
#             'objects': http.request.env['plant_nursery.plant_nursery'].search([]),
#         })

#     @http.route('/plant_nursery/plant_nursery/objects/<model("plant_nursery.plant_nursery"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('plant_nursery.object', {
#             'object': obj
#         })
