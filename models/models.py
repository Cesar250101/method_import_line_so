# -*- coding: utf-8 -*-
# Part of Konos. See LICENSE file for full copyright and licensing details.

from calendar import month
from cmath import e
import tempfile
import binascii
import logging
from datetime import datetime
from odoo.exceptions import Warning
from odoo import models, fields, api, exceptions, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

_logger = logging.getLogger(__name__)
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')



try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    file = fields.Binary('File')

    @api.multi
    def import_file(self):
        #if not file:
        #    raise Warning('Please Select File')
        fp = tempfile.NamedTemporaryFile(suffix=".xls")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        values = {}
        #workbook = xlrd.open_workbook(fp.name)
        workbook = xlrd.open_workbook('C://Users//cesar//Downloads//VentasArtículos.xls')
        sheet = workbook.sheet_by_index(0)
        order_id=self.id
        contador = 0
        for row_no in range(sheet.nrows):
            line = list(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
            if row_no>=1:            
                product=line[0].decode("utf-8").replace('.0','')
                if product:
                    precio_unitario=int(line[2].replace('.0',''))                    
                    product_id=self.env['product.product'].search([('default_code','=',product)],limit=1)
                    if product_id:
                        val={
                                'name':product_id.name,
                                'order_id':order_id,
                                'product_id':product_id.id,
                                'product_qty':line[1],
                                'product_uom':product_id.uom_id.id,
                                'price_unit':precio_unitario,
                                'date_planned':self.date_order
                            }   
                        stock_move_id=self.env['purchase.order.line'].sudo().create(val)                
                    else:
                        raise Warning("El SKU "+product+" no existe, debe crear el producto primero")

    @api.multi
    def _create_statement_lines(self,val):
        company=self.env.user.company_id.id
        cartola_id=self._context.get('active_id')
        journal_id=self.env['account.bank.statement'].search([('id','=',cartola_id)],limit=1).journal_id.id
        partner_id = self._find_partner(val.get('partner'))
        if not val.get('date'):
            raise Warning('Please Provide Date Field Value')
        if not val.get('memo'):
            raise Warning('Please Provide Memo Field Value')
        aaa = self._cr.execute("insert into account_bank_statement_line (date,ref,partner_id,name,amount,statement_id,journal_id,company_id) values (%s,%s,%s,%s,%s,%s,%s,%s)",(val.get('date'),val.get('ref'), partner_id,val.get('memo'),val.get('amount'),self._context.get('active_id'),journal_id,company))
        return True
#
    def _find_partner(self,name):
        partner_id = self.env['res.partner'].search([('name','=',name)])
        if partner_id:
            return partner_id.id
        else:
            return



