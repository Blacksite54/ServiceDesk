from rest_framework import serializers
from rest_framework.fields import empty


class LowercaseEmailField(serializers.EmailField):
    def run_validation(self, data=empty):
        data = super(LowercaseEmailField, self).run_validation(data)
        if data is empty or not data:
            return data
        return data.lower()
