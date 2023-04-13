# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Project(models.Model):
    _inherit = "project.project"

    def _compute_jobcost_count(self):
        jobcost = self.env['job.costing']
        job_cost_ids = self.mapped('job_cost_ids')
        for project in self:
            project.job_cost_count = jobcost.search_count([('id', 'in', job_cost_ids.ids)])
    
    
    job_cost_count = fields.Integer(
        compute='_compute_jobcost_count'
    )
    
    job_cost_ids = fields.One2many(
        'job.costing',
        'project_id',
    )

    def project_to_jobcost_action(self):
        job_cost = self.mapped('job_cost_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("rail_job_costing_management.action_job_costing")
        action['domain'] = [('id', 'in', job_cost.ids)]
        action['context'] = {'default_project_id':self.id,'default_analytic_id':self.analytic_account_id.id,'default_user_id':self.user_id.id}
        return action


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _compute_jobcost_count(self):
        jobcost = self.env['job.costing']
        job_cost_ids = self.mapped('job_cost_ids')
        for task in self:
            task.job_cost_count = jobcost.search_count([('id', 'in', job_cost_ids.ids)])

    job_cost_count = fields.Integer(
        compute='_compute_jobcost_count'
    )

    job_cost_ids = fields.One2many(
        'job.costing',
        'task_id',
    )

    def task_to_jobcost_action(self):
        job_cost = self.mapped('job_cost_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("rail_job_costing_management.action_job_costing")
        action['domain'] = [('id', 'in', job_cost.ids)]
        action['context'] = {'default_task_id':self.id,'default_project_id':self.project_id.id,'default_analytic_id':self.project_id.analytic_account_id.id,'default_user_id':self.env.user.id}
        return action 
        
        
