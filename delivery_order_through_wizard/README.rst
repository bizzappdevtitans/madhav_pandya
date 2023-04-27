===================================
**Delivery Order Mapping**
===================================

**Description**
***************

* Technical Name:- delivery_order_through_wizard

* Delivery Order is created through delivery_payload and products get fetched on the
  basis of barcode and shown in move_lines.


**Author**
**********

* BizzAppDev


**Used by**
***********

* #N/A


**Installation**
****************

* #N/A


**Configuration**
*****************

* Just click on menu item "Delivery Order Management" of Inventory model and delivery order will get created.


**Usage**
*********

* By pressing the menu item "Delivery Order Management" of Inventory model wizard will get open and by clicking
  "Create Delivery Order" button new delivery order will get created and the products
  will get fetched on the basis of barcode and shown in movelines, if barcode doesn't
  get match with any product it will raise ValidationError.


**Known issues/Roadmap**
************************

* #N/A


**Changelog**
*************

* #N/A
