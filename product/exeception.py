class ProductError(Exception):
    """
    Base class for Product Error
    """
    pass


class ProductCallingError(ProductError):

    def __init__(self, message, response):
        self._message = message
        self._response = response

        super(ProductError, self).__init__(
            "\n\n" +
            "  Message: %s\n" % self._message +
            "\n" +
            "  Status Code:  %s\n" % self._response.status_code +
            "  Response:\n    %s" % self._response.text +
            "\n"
        )