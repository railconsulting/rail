# -*- coding: utf-8 -*-
# Copyright 2012 - 2013 Daniel Reis
# Copyright 2015 - Antiun Ingeniería S.L. - Sergio Teruel
# Copyright 2016 - Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Employee(models.Model):
    _inherit = "hr.employee"
    
    no_empleado = fields.Char(_('Número de empleado'))
    tipo_pago = fields.Selection(selection=[('transferencia', 'Transferencia'),('efectivo', 'Efectivo'),
                                         ('cheque', 'Cheque')],
        string=_('Tipo de Pago'),
    )
    banco = fields.Many2one('res.bank','Banco empleado')
    no_cuenta = fields.Char(_('No. cuenta empleado'))
    rfc = fields.Char(_('RFC'))
    curp = fields.Char(_('CURP'))
    zip = fields.Char(_('Codigo Postal'))
    segurosocial = fields.Char(_('Seguro social'))
    correo_electronico = fields.Char(_('Correo electrónico'))	
    tipo_cuenta = fields.Selection(selection=[('t_debido', 'Tarjeta de débito'),('cheques', 'Cheques'),
                                         ('c_ahorro', 'Cuenta de ahorro'),('t_credito', 'Tarjeta de crédito')],
        string=_('Tipo de cuenta'),
    )
    diario_pago = fields.Many2one('account.journal', string='Cuenta de pago', domain=[('type', 'in', ('bank', 'cash'))])

    registro_patronal = fields.Char(string=_('Registro patronal'))
    
    tipo_regimen = fields.Selection(
        selection=[
            ('02','02 - Sueldos'),
            ('03','03 - Jubilados'),
            ('04','04 - Pensionados'),
            ('05','05 - Asimilados Miembros Sociedades Cooperativas Produccion'),
            ('06','06 - Asimilados Integrantes Sociedades Asociaciones Civiles'),
            ('07','07 - Asimilados Miembros consejos'),
            ('08','08 - Asimilados comisionistas'),
            ('09','09 - Asimilados Honorarios'),
            ('10','10 - Asimilados acciones'),
            ('11','11 - Asimilados otros'),
            ('12','12 - Jubilados o Pensionados'),
            ('13','13 - Indemnización o Separación'),
            ('99','99 - Otro Regimen')
        ]
    )
    tipo_contrato = fields.Selection(
        selection=[('01', '01 - Contrato de trabajo por tiempo indeterminado'), 
                   ('02', '02 - Contrato de trabajo para obra determinada'), 
                   ('03', '03 - Contrato de trabajo por tiempo determinado'),
                   ('04', '04 - Contrato de trabajo por temporada'), 
                   ('05', '05 - Contrato de trabajo sujeto a prueba'),
                   ('06', '06 - Contrato de trabajo con capacitación inicial'), 
                   ('07', '07 - Modalidad de contratación por pago de hora laborada'), 
                   ('08', '08 - Modalidad de trabajo por comisión laboral'), 
                   ('09', '09 - Modalidades de contratación donde no existe relación de trabajo'), 
                   ('10', '10 - Jubilación, pensión, retiro'), 
                   ('99', '99 - Otro contrato'),],
        string=_('Contrato'),
    )
    regimen = fields.Selection(
        selection=[
            ('601', 'General de Ley Personas Morales'),
            ('603', 'Personas Morales con Fines no Lucrativos'),
            ('605', 'Sueldos y Salarios e Ingresos Asimilados a Salarios'),
            ('606', 'Arrendamiento'),
            ('607', 'Régimen de Enajenación o Adquisición de Bienes'),
            ('608', 'Demás ingresos'),
            ('609', 'Consolidación'),
            ('610', 'Residentes en el Extranjero sin Establecimiento Permanente en México'),
            ('611', 'Ingresos por Dividendos (socios y accionistas)'),
            ('612', 'Personas Físicas con Actividades Empresariales y Profesionales'),
            ('614', 'Ingresos por intereses'),
            ('615', 'Régimen de los ingresos por obtención de premios'),
            ('616', 'Sin obligaciones fiscales'),
            ('620', 'Sociedades Cooperativas de Producción que optan por diferir sus ingresos'),
            ('621', 'Incorporación Fiscal'),
            ('622', 'Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras'),
            ('623', 'Opcional para Grupos de Sociedades'),
            ('624', 'Coordinados'),
            ('625', 'Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas'),
            ('626', 'Régimen Simplificado de Confianza - RESICO'),
            ('628', 'Hidrocarburos'),
            ('629', 'De los Regímenes Fiscales Preferentes y de las Empresas Multinacionales'),
            ('630', 'Enajenación de acciones en bolsa de valores')],
        string=_('Régimen'), default='605'
    )
  
    jornada = fields.Selection(
        selection=[('01', '01 - Diurna'), 
                   ('02', '02 - Nocturna'), 
                   ('03', '03 - Mixta'),
                   ('04', '04 - Por hora'), 
                   ('05', '05 - Reducida'),
                   ('06', '06 - Continuada'), 
                   ('07', '07 - Partida'), 
                   ('08', '08 - Por turnos'), 
                   ('99', '99 - Otra Jornada'),],
        string=_('Jornada'),
    )
    estado = fields.Many2one('res.country.state','Lugar donde labora (estado)')
    fondo_ahorro  = fields.Float(string=_('Fondo de ahorro'), readonly=True)
    dias_utilidad =  fields.Float(string=_('Dias para cálculo de Utilidad'))
    sueldo_utilidad =  fields.Float(string=_('Sueldo para cálculo de Utilidad'))
    fecha_utilidad_inicio = fields.Date(readonly=True)
    fecha_utilidad_fin = fields.Date(readonly=True)

    @api.onchange('registro_patronal')
    def _check_registro_length(self):
        if self.registro_patronal:
            if len(self.registro_patronal) != 11:
                raise UserError(_('La longitud del registro patronal es incorrecto'))

    @api.onchange('segurosocial')
    def _check_nss_length(self):
        if self.segurosocial:
            if len(self.segurosocial) != 11:
                raise UserError(_('La longitud del número de seguro social es incorrecto'))

    @api.onchange('rfc')
    def _check_rfc_length(self):
        if self.rfc:
            if len(self.rfc) != 12 and len(self.rfc) != 13:
                raise UserError(_('La longitud del RFC es incorrecto'))