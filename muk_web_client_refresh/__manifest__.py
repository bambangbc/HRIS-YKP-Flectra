# -*- coding: utf-8 -*-
###################################################################################
# 
#    Copyright (C) 2018 MuK IT GmbH
#    Copyright (C) 2018 BetaPy
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

{
    "category": "Extra Tools", 
    "website": "https://betapy.com", 
    "name": "MuK Web Refresh", 
    "license": "AGPL-3", 
    "author": "Betapy, MuK IT", 
    "support": "incoming+betapy/support@incoming.gitlab.com", 
    "external_dependencies": {
        "python": [], 
        "bin": []
    }, 
    "summary": "Web Client Refresh", 
    "application": False,
    "depends": [
        "base_automation", 
        "muk_web_client"
    ], 
    "version": "3.0.0", 
    "contributors": [
        "Mathias Markl <mathias.markl@mukit.at>", 
        "BetaPy"
    ], 
    "images": [
        "static/description/banner.png"
    ], 
    "data": [
        "template/assets.xml", 
        "views/refresh_action_view.xml", 
        "views/res_config_settings_view.xml", 
        "data/refresh_actions.xml"
    ], 
    "qweb": [
        "static/src/xml/*.xml"
    ], 
    "installable": True
} 