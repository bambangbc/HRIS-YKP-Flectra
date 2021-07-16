import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta
from datetime import timedelta

# import babel

from flectra import api, fields, models, tools, _
# from flectra.addons import decimal_precision as dp
from flectra.exceptions import UserError, ValidationError
from flectra.tools import float_utils


class hr_master_salary(models.Model):
	_inherit = "hr.attendance"
	_description = "attendance"

	terlambat 		= fields.Float('Terlambat')