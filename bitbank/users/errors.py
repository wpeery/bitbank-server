class UserError(Exception):
    """Base error for this model"""


class UnableToTransferSatoshis(UserError):
    """Error raised if we are unable to transfer satoshis"""
