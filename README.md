upugdemo
========

Demo web application using bottle.py, angular.js, twitter bootstrap, and html5
------------------------------------------------------------------------
[GitHub Repository](https://github.com/SmithSamuelM/upugdemo "Repository Link")
https://github.com/SmithSamuelM/upugdemo

See my blog [Samuel Smith](http://samuelsmith.org/) http://samuelsmith.org/
for detailed exposition.

A github page can be found at the following:

[GitHub page](http://smithsamuelm.github.com/upugdemo "GitHub Page")
http://smithsamuelm.github.com/upugdemo

This is in support of a presentation at the Utah Python Users Group on November 8, 2012.

To use this demo you need to have python 2.7 installed and have an html5 compliant web browser. The demo was tested in Google Chrome on os X. Should
run fine on linux as well. 

To run the web server from the command line.  

    cd demo
    ./serving.py

This will run the webserver at port 8080.
To run on a different port enter it with the -p option
Too see all the options type
    ./serving.py -h

    $ ./serving.py -h
    usage: serving.py [-h] [-d] [-r] [-p [PORT]] [-a [HOST]] [-s [SERVER]]
    
    Runs localhost wsgi service on given host address and port. 
    Default host:port is localhost:8080.
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Debug mode.
      -r, --reload          Server reload mode if also in debug mode.
      -p [PORT], --port [PORT]
                            Wsgi server ip port.
      -a [HOST], --host [HOST]
                            Wsgi server ip host address.
      -s [SERVER], --server [SERVER]
                            Wsgi server type.

Enter
    http://localhost:8080 

