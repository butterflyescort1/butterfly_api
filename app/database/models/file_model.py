from tortoise import fields, models


class FileTable(models.Model):
    class Meta:
        table = "files"
    
    id = fields.TextField(pk=True)
    file_id = fields.TextField(null=False)
