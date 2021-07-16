# -*- coding: utf-8 -*-
import logging
from flectra import models, api

_logger = logging.getLogger(__name__)

MODULE = '_debranding'


class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.model
    def _create_debranding_views(self):

        self._create_view('webclient_bootstrap_enterprise_title', 'web.webclient_bootstrap', '''
       <xpath expr="//title" position="replace"></xpath>''')
        

    @api.model
    def _create_view(self, name, inherit_id, arch, noupdate=False, type='qweb'):
        view = self.env.ref("%s.%s" % (MODULE, name), raise_if_not_found=False)
        if view:
            try:
                view.write({
                    'arch': arch,
                })
                view._check_xml()
            except:
                _logger.warning('Cannot update view %s. Delete it.', name, exc_info=True)
                view.unlink()
                return

            return view.id

        try:
            with self.env.cr.savepoint():
                view = self.env['ir.ui.view'].create({
                    'name': name,
                    'type': type,
                    'arch': arch,
                    'inherit_id': self.env.ref(inherit_id, raise_if_not_found=True).id
                })
                view._check_xml()
        except:
            _logger.debug('Cannot create view %s. Cancel.', name, exc_info=True)
            return
        self.env['ir.model.data'].create({
            'name': name,
            'model': 'ir.ui.view',
            'module': MODULE,
            'res_id': view.id,
            'noupdate': noupdate,
        })
        return view.id
