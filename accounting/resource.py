from import_export import resources
from accounting.models import *

class ExpensesIncurredResource(resources.ModelResource):
    class Meta:
        model = ExpensesIncurred
