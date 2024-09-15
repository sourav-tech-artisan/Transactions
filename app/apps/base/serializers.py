from rest_framework import serializers

class DynamicFieldsSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional fields argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the fields argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            # return all the fields if none of the provide fields is part of serializer
            fields_to_pop = existing - allowed if len(allowed) > 0 else []
            

            for field_name in fields_to_pop:
                self.fields.pop(field_name)
