# nginx-http-hello-module

This demo module is excerpted from 
_Understanding NginX Modules Development and Architecture Resolving (Second Edition)_.  

Build NginX with this directory as a static or dynamic module:

```bash
$ ./configure --add-module=/path/to/nginx-http-hello-module
$ make
$ make install
```

This module could be used in `LOCATION PART` to debug NginX configure file, like:

```nginx
location ^~ / {
    hello;
}
```

Website response is a string `hello world`.  

