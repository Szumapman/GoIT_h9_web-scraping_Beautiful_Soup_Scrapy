from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import (
    DateField,
    EmbeddedDocumentField,
    ListField,
    StringField,
    ReferenceField,
)


class Author(Document):
    name = StringField(required=True)
    born_date = DateField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class Tag(EmbeddedDocument):
    name = StringField()


class Quote(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author)
    quote = StringField(required=True)
    meta = {"allow_inheritance": True}
