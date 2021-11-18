from werkzeug.exceptions import BadRequest, HTTPException

class InvalidArgument(BadRequest):
    def __init__(self, description=None):
        super(InvalidArgument, self).__init__()
        if description:
            self.description = description
