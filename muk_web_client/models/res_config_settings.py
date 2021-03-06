###################################################################################
#
#    Copyright (C) 2017 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from flectra import fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    module_muk_web_client_refresh = fields.Boolean(
        string="Web Refresh",
        help="Define action rules to automatically refresh views.")
    
    module_muk_web_client_notification = fields.Boolean(
        string="Web Notification",
        help="Send instant messages to users in real time.")
     