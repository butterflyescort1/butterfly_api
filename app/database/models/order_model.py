from tortoise import fields, models


class OrderTable(models.Model):
    class Meta:
        table = "orders"
    
    mammoth_id = fields.IntField(null=False)
    model_name = fields.TextField(null=False)
    photo_link = fields.TextField(null=False)
    service_name = fields.TextField(null=False)
    addservice_name = fields.TextField(null=False)
    amount = fields.IntField(null=False)
    status = fields.TextField(null=False)
