class HepsiburadaError(Exception):
    """
    Base class for Hepsiburada Api Error
    """
    pass


class HepsiburadaAPIError(HepsiburadaError):

    def __init__(self, message, response):
        self._message = message
        self._response = response

        super(HepsiburadaAPIError, self).__init__(
            "\n\n" +
            "  Message: %s\n" % self._message +
            "\n" +
            "  Status Code:  %s\n" % self._response.status_code +
            "  Response:\n    %s" % self._response.text +
            "\n"
        )