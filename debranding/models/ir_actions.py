# -*- coding: utf-8 -*-
from flectra import models


class IrActionsActWindowDebranding(models.Model):
    _inherit = 'ir.actions.act_window'

    def read(self, fields=None, load='_classic_read'):
        results = super(IrActionsActWindowDebranding, self).read(
            fields=fields, load=load)
        if not fields or 'help' in fields:
            new_name = "SIM HR"
            for res in results:
                if isinstance(res, dict) and res.get('help'):
                    res['help'] = res['help'].replace('Flectra', new_name)
        return results
