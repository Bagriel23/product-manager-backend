from mongoengine import connect, Document, SequenceField, StringField, BooleanField
connect ("ProductsDB")

class Product(Document):
    id = SequenceField(primary_key=True, sequence_name="id_sequence")
    name = StringField(required=True)
    description = StringField(required=False)
    price = StringField(required=True)
    available = BooleanField(required=False)
    
