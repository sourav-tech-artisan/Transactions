from rest_framework import serializers
from django.core.validators import MinValueValidator
from app.apps.transactions.repositories.transactionrepo import TransactionRepository

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


class TransactionCreateSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    transaction_type = serializers.CharField(max_length=50)
    parent_transaction = serializers.PrimaryKeyRelatedField(queryset=TransactionRepository.get_all_queryset(), required=False)

    class Meta:
        model = TransactionRepository.get_model()
        fields = ("amount", "transaction_type", "parent_transaction")

    def validate(self, attrs):
        super().validate(attrs)
        # total amount is the same as amount for the initial transaction
        attrs["total_amount"] = attrs["amount"]
        return attrs
    

class TransactionUpdateSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)], required=False)
    transaction_type = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = TransactionRepository.get_model()
        fields = ("amount", "transaction_type",)

    def validate(self, attrs):
        super().validate(attrs)
        instance = self.context.get("instance")
        # check if the amount is being updated
        if "amount" in attrs:
            difference_in_amount = attrs["amount"] - instance.amount
            attrs["total_amount"] = instance.total_amount + difference_in_amount
        return attrs

class TransactionReadSerializer(DynamicFieldsSerializer):
    class Meta:
        model = TransactionRepository.get_model()
        fields = "__all__"