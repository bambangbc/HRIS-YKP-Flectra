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

from flectra import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    refresh_delay = fields.Integer(
        string="Delay",
        help="""Delays the execution of refresh and thus prevents the view from being reloaded too often.
            For example, a delay of 1000 (ms) would mean that the view cannot be reloaded more than once a second. """)
        
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param("muk_web_client_refresh.refresh_delay", self.refresh_delay)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(refresh_delay=int(params.get_param("muk_web_client_refresh.refresh_delay", default=1000)))
        return res
