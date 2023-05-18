# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import time
import datetime
import xlwt
import base64
import io
import logging

class AsistenteKardex(models.TransientModel):
	_name = 'kardex.asistente_kardex'
	_description = 'Kardex'

	def _default_producto(self):
		if len(self.env.context.get('active_ids', [])) > 0:
			return self.env.context.get('active_ids')[0]
		else:
			return None

	ubicacion_id = fields.Many2one("stock.location", string="Ubicacion", required=True)
	producto_ids = fields.Many2many("product.product", string="Productos", required=True)
	fecha_desde = fields.Datetime(string="Fecha Inicial", required=True)
	fecha_hasta = fields.Datetime(string="Fecha Final", required=True)
	archivo_excel = fields.Binary('Archivo excel')
	name_excel = fields.Char('Nombre archivo', default='kardex.xls', size=32)

	def print_report(self):
		data = {
			 'ids': [],
			 'model': 'kardex.asistente_kardex',
			 'form': self.read()[0]
		}
		return self.env.ref('kardex.action_reporte_kardex').report_action(self, data=data)

	def reporte_excel(self):
		libro = xlwt.Workbook()
		hoja = libro.add_sheet('reporte')

		xlwt.add_palette_colour("custom_colour", 0x21)
		libro.set_colour_RGB(0x21, 200, 200, 200)
		estilo = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour')
		hoja.write(0, 0, 'KARDEX')

		datos = {}
		datos['fecha_desde'] = self.fecha_desde
		datos['fecha_hasta'] = self.fecha_hasta
		datos['ubicacion_id'] = []
		datos['ubicacion_id'].append(self.ubicacion_id.id)
		
		y = 2
		for producto in self.producto_ids:
#            datos['producto_id'] = producto.id
			resultado = self.env['report.kardex.reporte_kardex'].lineas(datos, producto.id)
			hoja.write(y, 0, 'Fecha desde:')
			hoja.write(y, 1, 'Fecha hasta:')
			hoja.write(y, 2, 'Ubicación:')
			hoja.write(y, 3, 'Producto:')
			y += 1
			hoja.write(y, 0, datetime.datetime.strftime(self.fecha_desde,'%d/%m/%Y'))
			hoja.write(y, 1, datetime.datetime.strftime(self.fecha_hasta,'%d/%m/%Y'))
			hoja.write(y, 2, self.ubicacion_id.display_name)
			hoja.write(y, 3, producto.name)
			y += 1
			hoja.write(y, 0, 'Inicial:')
			hoja.write(y, 1, 'Entradas:')
			hoja.write(y, 2, 'Salidas:')
			hoja.write(y, 3, 'Final:')
			y += 1
			hoja.write(y, 0, resultado['totales']['inicio'])
			hoja.write(y, 1, resultado['totales']['entrada'])
			hoja.write(y, 2, resultado['totales']['salida'])
			hoja.write(y, 3, resultado['totales']['inicio']+resultado['totales']['entrada']+resultado['totales']['salida'])
			y += 2
			hoja.write(y, 0, 'Fecha')
			hoja.write(y, 1, 'Documento')
			hoja.write(y, 2, '#Sale / #Purchase')
			hoja.write(y, 3, '# Invoice')
			hoja.write(y, 4, 'Empresa')
			hoja.write(y, 5, 'Tipo')
			hoja.write(y, 6, 'UOM')
			hoja.write(y, 7, 'Entradas')
			hoja.write(y, 8, 'Salidas')
			hoja.write(y, 9, 'Final')
			hoja.write(y, 10, 'Costo')
			hoja.write(y, 11, 'Total')
			y += 1
			for linea in resultado['lineas']:
				hoja.write(y, 0, datetime.datetime.strftime(linea['fecha'],'%d/%m/%Y'))
				hoja.write(y, 1, linea['documento'])
				hoja.write(y, 2, linea['order_id'])
				hoja.write(y, 3, linea['invoice_id'])
				hoja.write(y, 4, linea['empresa'])
				hoja.write(y, 5, linea['tipo'])
				hoja.write(y, 6, linea['unidad_medida'])
				hoja.write(y, 7, linea['entrada'])
				hoja.write(y, 8, abs(linea['salida']))
				hoja.write(y, 9, linea['saldo'])
				hoja.write(y, 10, linea['costo'])
				hoja.write(y, 11, linea['saldo'] + linea['costo'])
				y += 1
			y += 1

		f = io.BytesIO()
		libro.save(f)
		datos = base64.b64encode(f.getvalue())
		self.write({'archivo_excel':datos, 'name_excel':'kardex.xls'})

		return {
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'kardex.asistente_kardex',
			'res_id': self.id,
			'view_id': False,
			'type': 'ir.actions.act_window',
			'target': 'new',
		}

	def reporte_tree_view(self):
		self.env['kardex.asistente_kardex.custom.report'].search([]).unlink()
		datos = {}
		datos['fecha_desde'] = self.fecha_desde
		datos['fecha_hasta'] = self.fecha_hasta
		datos['ubicacion_id'] = []
		datos['ubicacion_id'].append(self.ubicacion_id.id)
		for producto in self.producto_ids:
			resultado = self.env['report.kardex.reporte_kardex'].lineas(datos, producto.id)
			for linea in resultado['lineas']:
				vals = {
					'date' : linea['fecha'],
					'documents' : linea['documento'],
					'order_ref' : linea['order_id'],
					'invoice_ref' : linea['invoice_id'],
					'partner_name' : linea['empresa'],
					'tipo' : linea['tipo'],
					'uom' : linea['unidad_medida'],
					'qty1' : linea['entrada'],
					'qty2' : abs(linea['salida']),
					'saldo' : linea['saldo'],
					'cost' : linea['costo'],
					'total' : linea['saldo'] + linea['costo'],
				}
				self.env['kardex.asistente_kardex.custom.report'].create(vals)
		return {
			'name': _('Kardex Report'),
			'view_mode': 'tree',
			'res_model': 'kardex.asistente_kardex.custom.report',
			'type': 'ir.actions.act_window',
		}

class AsistenteKardexCustomReport(models.TransientModel):
	_name = 'kardex.asistente_kardex.custom.report'
	_description = 'Kardex Custom Report'

	date = fields.Datetime(string="Fecha")
	documents = fields.Char(string="Documento")
	order_ref = fields.Char(string="#Sale / #Purchase")
	invoice_ref = fields.Char(string="# Invoice")
	partner_name = fields.Char(string="Empresa")
	tipo = fields.Char(string="Tipo")
	uom = fields.Char(string="UOM")
	qty1 = fields.Char(string="Entradas")
	qty2 = fields.Char(string="Salidas")
	saldo = fields.Char(string="Final")
	cost = fields.Char(string="Costo")
	total = fields.Char(string="Total")
