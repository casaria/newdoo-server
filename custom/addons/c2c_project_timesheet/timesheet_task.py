# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################
#
# ChriCar Beteiligungs- und Beratungs- GmbH
# Copyright (C) ChriCar Beteiligungs- und Beratungs- GmbH
# all rights reserved
# created 2009-08-18 23:44:30+02
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################
from osv import fields,osv
import logging

class project_work(osv.osv):
    _inherit = "project.task.work"
    _logger = logging.getLogger(__name__)
    
    def _update_project_id(self, cr, uid, ids, context=None):
        task_work_obj = self.pool.get('project.task.work')
        task_work_ids = task_work_obj.search(cr, uid, [('task_id','in',ids)])
        self._logger.debug('update project `%s` `%s`', ids, task_work_ids)
        return task_work_ids

    _columns = {
        'date': fields.datetime('Date', select="1"),
        'task_id': fields.many2one('project.task', 'Task', ondelete='cascade', required=True, select="1"),
        'user_id': fields.many2one('res.users', 'Done by', required=True, select="1"),
        'project_id' : fields.related('task_id', 'project_id', type='many2one', relation="project.project", string='Project',
        store = True
        # FIXME activation of this function causes project_id not be stored on normal entry 
        #          store =  { 'project.task' :
        #                   ( _update_project_id, ['project_id'],
        #                    10)}
),
    }


    def write(self, cr, uid, ids, vals, context=None):
        if 'user_id' not in vals:
            for task in self.browse(cr, uid, ids, context=context):
                vals['user_id'] = task.user_id.id
        return super(project_work,self).write(cr, uid, ids, vals, context)

project_work()

#class hr_timesheet_sheet(osv.osv):
#    _name = "hr_timesheet_sheet.sheet"

#    _columns = {
#        'work_ids': fields.one2many('project.task.work', 'hr_timesheet_sheet_id2', 'Work done'),
#    }

#hr_timesheet_sheet()
