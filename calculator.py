"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def home(*args):
    return """<html>
    <head>
    <title>Lab 3 - WSGI Calculator</title>
    </head>
    <body>
    <p>This WSGI Calculator will take url inputs and do maths</p>
    <p>Examples:</p>
    <p><a href="http://localhost:8080/multiply/3/5">http://localhost:8080/multiply/3/5</a>   => 15</p>
    <p><a href="http://localhost:8080/add/23/42">http://localhost:8080/add/23/42</a>      => 65</p>
    <p><a href="http://localhost:8080/subtract/23/42">http://localhost:8080/subtract/23/42</a> => -19</p>
    <p><a href="http://localhost:8080/divide/22/11">http://localhost:8080/divide/22/11</a>   => 2</p>
    <p><a href="http://localhost:8080/divide/6/0">http://localhost:8080/divide/6/0</a>     => HTTP "400 Bad Request"</p>
    <p><a href="http://localhost:8080/">http://localhost:8080/</a>               => <html>Here's how to use this page...</html></p>
    </body>
    </html>"""


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return str(args[0] + args[1])


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    return str(args[0] - args[1])


def multiply(*args):
    """ Returns a STRING with the multiple of the arguments """
    return str(args[0] * args[1])


def divide(*args):
    """ Returns a STRING with the divisible of the arguments """
    return str(args[0] / args[1])


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    func_path = path.lstrip('/')
    if not func_path:
        func = home
        args = []
    else:
        args = func_path.strip("/").split("/")
        func_name = args.pop(0)
        func = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}.get(func_name, home)
        args = map(int, args)
    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    body = ""
    status = ""
    try:
        path = environ.get('PATH_INFO')
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Divide by zero</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
