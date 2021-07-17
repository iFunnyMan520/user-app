#!/usr/bin/env python
from app import make_app


app = make_app()


if __name__ == '__main__':
    app.run(port=1234, debug=True)