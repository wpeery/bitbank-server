import logging

import rest_framework.request
from django.db import transaction
from rest_framework import status
from rest_framework import response
from rest_framework import viewsets
from rest_framework import decorators

from bitbank.transfers.api import serializers
from bitbank.transfers import models as transfer_models
from bitbank.users import models as user_models
from bitbank.users import errors as user_errors
from bitbank import api_errors


class TransferViewSet(viewsets.ViewSet):
    serializer_class = serializers.TransferRequestSerializer
    logger = logging.getLogger(__name__)

    @decorators.action(methods=["post"], detail=False)
    def transfer_satoshi(self, request: rest_framework.request.Request):
        transfer_request = serializers.TransferRequestSerializer(
            data={
                "to_username": request.data.get("to_username"),
                "amount": request.data.get("amount"),
            }
        )
        # exceptions will be caught by django and will return a http status code 400
        transfer_request.is_valid(raise_exception=True)
        validated_to_username = transfer_request.validated_data["to_username"]
        validated_amount = transfer_request.validated_data["amount"]
        if request.user.username == validated_to_username:
            return api_errors.api_error_response(
                error_code=api_errors.UNABLE_TO_TRANSFER_FUNDS,
                details="Cannot transfer funds to self",
            )
        try:
            from_user = user_models.User.objects.get(username=request.user.username)
            to_user = user_models.User.objects.get(username=validated_to_username)
            with transaction.atomic():
                user_models.User.unsafe_transfer_satoshi(
                    from_username=request.user.username,
                    to_username=validated_to_username,
                    amount=validated_amount,
                )
                satoshi_transfer = transfer_models.SatoshiTransfer(
                    from_user=from_user, to_user=to_user, amount=validated_amount
                )
                satoshi_transfer.save()
        except user_models.User.DoesNotExist:
            return api_errors.api_error_response(
                error_code=api_errors.ENTITY_DOES_NOT_EXIST
            )
        except user_errors.NotEnoughFunds:
            return api_errors.api_error_response(error_code=api_errors.NOT_ENOUGH_FUNDS)
        except user_errors.UnableToTransferFunds as e:
            self.logger.warning("Unable to transfer satoshis: %s", e)
            return api_errors.api_error_response(
                error_code=api_errors.UNABLE_TO_TRANSFER_FUNDS
            )
        return response.Response(status=status.HTTP_200_OK, data={"success": True})
