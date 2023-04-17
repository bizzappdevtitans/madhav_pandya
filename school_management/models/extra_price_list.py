from odoo import fields,api, models


class ExtraPriceList(models.Model):
    _name = "extra.price.list"
    _description = "Extrs Price List"


    name=fields.Char(string="Name")
    price= fields.Float("Price")
