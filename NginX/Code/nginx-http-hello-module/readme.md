# nginx-http-hello-module

### Installation

Build NginX with this directory as a static or dynamic module.  

```bash
./configure --add-module=/path/to/nginx-http-hello-module
make
make install
```

### Usage

```bash
location ^~ / {
    hello;
}
```
