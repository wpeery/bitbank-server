class UserError(Exception):
    """Base error for this model"""


class UnableToTransferFunds(UserError):
    """Error raised if we are unable to transfer funds"""


class NotEnoughFunds(UnableToTransferFunds):
    """Error raised if there are not enough funds to transfer"""
