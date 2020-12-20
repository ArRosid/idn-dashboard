from accounts.models import User
from import_export import resources

class UserResources(resources.ModelResource):
    class Meta:
        model = User