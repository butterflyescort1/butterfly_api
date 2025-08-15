from tortoise import fields, models


class UserTable(models.Model):
    class Meta:
        table = "users"
    
    id = fields.IntField(pk=True)
    balance = fields.IntField(null=False, default=0)
    city = fields.TextField(null=False)
