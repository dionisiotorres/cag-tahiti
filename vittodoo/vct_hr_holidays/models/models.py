# -*- coding: utf-8 -*-

from odoo import models

class SchedulerHolidays(models.Model):
    _inherit = 'hr.holidays'
    
    def add_category_employee_holidays(self, name, holiday_status_id, number_of_days_temp, aEmployeeCategoryName, context=None):
        results = self.env['hr.holidays.status'].search([['id', '=', holiday_status_id]])
        if len(results) == 0:
            raise Exception("id de congés inexistant")
        
        iEmployeeCategory = self.resolvEmployeeCategoryByName(aEmployeeCategoryName, context)
        values = {
            'type': 'add',  # Demande de congés ou Attribution de congés.
            'name': name,
            'holiday_status_id': holiday_status_id,  # Type de congés(Congés payés, Congés non payés(sans solde))
            'number_of_days_temp': number_of_days_temp,  # Nombre de jours
            'holiday_type': "category",  # Mode d'attribution [category] ou [employee]
            'category_id': iEmployeeCategory.id,  # Id de la catégorie
            'employee_id': "",
        }
        self.create(values)
        
    def add_employee_holidays(self, name, holiday_status_id, number_of_days_temp, aEmployeeName, context=None):
        iEmployee = self.resolvEmployeeByName(aEmployeeName, context)
        values = {
            'type': 'add',  # Demande de congés ou Attribution de congés.
            'name': name,
            'holiday_status_id': holiday_status_id,  # Type de congés(Congés payés, Congés non payés(sans solde))
            'number_of_days_temp': number_of_days_temp,  # Nombre de jours
            'holiday_type': "employee",  # Mode d'attribution [category] ou [employee]
            'category_id': "",  # Id de la catégorie
            'empolyee_id': iEmployee.id,  # Id de la catégorie
        }
        self.create(values)
        
    def resolvEmployeeCategoryByName(self, aEmployeeCategoryName, context=None):
        results = self.env['hr.employee.category'].search([['name', '=', aEmployeeCategoryName]])
        if len(results) == 0:
            raise Exception("Catégorie " + str(aEmployeeCategoryName) + " introuvable !!")
        else:
            return results[0]
#         for result in results:  # Parcours la liste de tuple
#             item = model.browse(result[0])  # Récupère l'enregistrement
#             if item:
#                 return item
#             else:
#                 continue
        return 
    
    def resolvEmployeeByName(self, aEmployeeName, context=None):
        results = self.env['hr.employee'].search([['name', '=', aEmployeeName]])
        if len(results) == 0:
            raise Exception("Catégorie " + str(aEmployeeName) + " introuvable !!")
        else:
            return results[0]
