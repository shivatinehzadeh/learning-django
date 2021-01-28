from .models import Book
from rest_framework import serializers


class BookSerializers(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="myApp:book-detail")

    class Meta:
        model= Book
        fields=['url','name','description']