CMPUT404-assignment-webserver
=============================

* Eric Brisson
* ebrisson (CCID)
* 1615620 (student number)

------------------------------

CMPUT404-assignment-webserver

See requirements.org (plain-text) for a description of the project.

Make a simple webserver.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

server.py contains contributions from:

* Abram Hindle
* Eddie Antonio Santos
* Jackson Z Chang
* Mandy Meindersma 

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

Assumptions Made
========================
* According to HTTP spec RF7230, under section 5.3.1 on the linked page below,
requests need to be made using absolute paths. As such, if my web server detects
the usage of a relative path (ie. sees ".." in a file path), it will automatically respond
with a 404 Not Found response. If the client makes a request and wants to use ".." to go up a
directory but stay withing the ./www directory serving the files for the web server, they should just use
the absolute path instead.

    * https://www.rfc-editor.org/rfc/rfc7230#section-5.3.1

* As per the eClass forum post below, 301 Moved Permanently redirection is to work for both 127.0.0.1,
and localhost, depending on what the client requested in the host header of its request. However, according
to HTTP spec 2616, under section 14.23, the Host header is required for an HTTP 1.1 request, and thus if it is missing,
the server will respond with a 400 Bad Request response.

    * https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=2169418
    * https://www.rfc-editor.org/rfc/rfc2616

* According to HTTP spec RF7231, under section 7.4.1, the Allow header must be included in a 405 response indicating
which methods are allowed. In the case of this assignment, only GET requests are permitted to this web server.

    * https://www.rfc-editor.org/rfc/rfc7231#section-7.4.1


