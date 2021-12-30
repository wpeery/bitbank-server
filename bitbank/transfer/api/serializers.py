from rest_framework import serializers


class TransferRequestSerializer(serializers.Serializer):
    to_username = serializers.CharField(required=True, min_length=1, max_length=255)
    # right now this is hardcoded to the logged-in user, in the future we may expose
    # this parameter to people with admin rights
    from_username = serializers.CharField(required=False, min_length=1, max_length=255)
    amount = serializers.IntegerField(min_value=0, required=True)
