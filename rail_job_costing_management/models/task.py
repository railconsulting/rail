# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaterialPlanning(models.Model):
    _name = 'material.plan'
    _description = 'Material Plan'

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        self.description = self.product_id.name
    
    product_id = fields.Many2one(
        'product.product',
        string='Product'
    )
    description = fields.Char(
        string='Description'
    )
    product_uom_qty = fields.Integer(
        'Quantity',
        default=1.0
    )
    product_uom = fields.Many2one(
        'uom.uom',
        'Unit of Measure'
    )
    material_task_id = fields.Many2one(
        'project.task',
        'Material Plan Task'
    )


class ConsumedMaterial(models.Model):
    _name = 'consumed.material'
    _description = 'Consumed Material'

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        self.description = self.product_id.name

    product_id = fields.Many2one(
        'product.product',
        string='Product'
    )
    description = fields.Char(
        string='Description'
    )
    product_uom_qty = fields.Integer(
        'Quantity',
        default=1.0
    )
    product_uom = fields.Many2one(
        'uom.uom',
        'Unit of Measure'
    )
    consumed_task_material_id = fields.Many2one(
        'project.task',
        string='Consumed Material Plan Task'
    )

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('picking_ids.requisition_line_ids')
    def _compute_stock_picking_moves(self):
        for rec in self:
            rec.ensure_one()
            rec.move_ids = self.env['material.purchase.requisition.line']
            for picking in rec.picking_ids:
                rec.move_ids = picking.requisition_line_ids.ids

    def total_stock_moves_count(self):
        for task in self:
            task.stock_moves_count = len(task.move_ids)
    
    def _compute_notes_count(self):
        for task in self:
            task.notes_count = len(task.notes_ids)

    picking_ids = fields.One2many(
        'material.purchase.requisition',
        'task_id',
        string='Stock Pickings'
    )
    move_ids = fields.Many2many(
        'material.purchase.requisition.line',
        compute='_compute_stock_picking_moves',
        store=True,
    )
    material_plan_ids = fields.One2many(
        'material.plan',
        'material_task_id',
        string='Material Plannings'
    )
    consumed_material_ids = fields.One2many(
        'consumed.material',
        'consumed_task_material_id',
        string='Consumed Materials'
    )
    stock_moves_count = fields.Integer(
        compute='total_stock_moves_count', 
        string='# of Stock Moves',
        store=True,
    )
    parent_task_id = fields.Many2one(
        'project.task', 
        string='Project Parent Task', 
        readonly=True
    )
    child_task_ids = fields.One2many(
        'project.task', 
        'parent_task_id', 
        string='Child Tasks'
    )
    notes_ids = fields.One2many(
        'note.note', 
        'task_id', 
        string='Notes Id',
    )
    notes_count = fields.Integer(
        compute='_compute_notes_count', 
        string="Notes"
    )
    job_number = fields.Char(
        string = "Job Number",
        copy = False,
    )

    @api.model
    def create(self,vals):
        number = self.env['ir.sequence'].next_by_code('project.task')
        vals.update({
            'job_number': number,
        })
        return super(ProjectTask, self).create(vals) 

    def view_stock_moves(self):
        for rec in self:
            stock_move_list = []
            for move in rec.move_ids:
                stock_move_list += move.requisition_id.delivery_picking_id.move_lines.ids
        result = self.env["ir.actions.actions"]._for_xml_id("stock.stock_move_action")
        result['domain'] = str([('id', 'in', stock_move_list)])
        return result

    def view_notes(self):
        for rec in self:
            res = self.env["ir.actions.actions"]._for_xml_id("rail_job_costing_management.action_task_note_note")
            res['domain'] = str([('task_id','in',rec.ids)])
        return res

    def action_subtask(self):#ODOO 13
        res = super(ProjectTask, self).action_subtask()
        res['context'].update({
            'default_parent_task_id': self.id, 
        })
        return res
