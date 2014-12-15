
class OpenstackAssertException(Exception):
    msg_fmt = "OpenstackAssertException - %(exception)s"
    def __init__(self, message=None, **kwargs):
        if not message:
            message = self.msg_fmt % kwargs
        super(OpenstackAssertException, self).__init__(message)


class PreconditionNotMeetException(OpenstackAssertException):
    msg_fmt = "Resource %(resource)s validate %(validate)s \
                require precondition %(precondition)s."


class ResourceNotReadyException(OpenstackAssertException):
    msg_fmt = "Resource %(resource)s depends on Resource %(pre_resource)s" \
              "on #%(pre_validate)s."