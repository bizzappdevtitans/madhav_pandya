from odoo import fields, models


class Canteen(models.Model):
    _name = "canteen"
    _description = "canteen"

    image1 = fields.Image("Our Canteen")
    image2 = fields.Image()
    image3 = fields.Image()
    image4 = fields.Image()


class Library(models.Model):
    _name = "library"
    _description = "library"


class Sports(models.Model):
    _name = "sports"
    _description = "sports"


class SmartClass(models.Model):
    _name = "smart_class"
    _description = "smart_class"


class CanteenMenu(models.Model):
    _name = "canteen_menu"
    _description = "canteen_menu"
    item = fields.Char("Item name")
    price = fields.Float("Price")
    image = fields.Image("Photo")

    _sql_constraints = [
        ("name_uniq", "UNIQUE(item)", "You cannot repeat same ITEM!")
    ]
