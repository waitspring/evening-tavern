/**********************************************************************************************************************
 *                                                                                                                    *
 * ngx_http_hello_module.c                                                                                            *
 * author: Fu Xuanming (Waitspring)                                                                                   *
 *                                                                                                                    *
 **********************************************************************************************************************
 *
 * define a command that return string "hello world"
 */

# include <nginx.h>
# include <ngx_config.h>
# include <ngx_core.h>
# include <ngx_http.h>


static char *ngx_http_hello(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
static ngx_int_t ngx_http_hello_handler(ngx_http_request_t *r);
static ngx_command_t ngx_http_hello_commands[] = {
    {
        // define command "hello" which could be used in nginx.conf, return string "hello world".
        ngx_string("hello"),
        NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF | NGX_CONF_NOARGS,
        ngx_http_hello,
        NGX_HTTP_LOC_CONF_OFFSET,
        0,
        NULL
    },
    ngx_null_command
};

static ngx_http_module_t ngx_http_hello_module_ctx = {
    NULL,                                        // preconfiguration
    NULL,                                        // postconfiguration
    NULL,                                        // create main configuration
    NULL,                                        // init main configuration
    NULL,                                        // create server configuration
    NULL,                                        // merge server configuration
    NULL,                                        // create location configuration
    NULL                                         // merge location configuration
};

ngx_module_t ngx_http_hello_module = {
    NGX_MODULE_V1,
   &ngx_http_hello_module_ctx,                   // module context
    ngx_http_hello_commands,                     // module directives
    NGX_HTTP_MODULE,                             // module type
    NULL,                                        // init master
    NULL,                                        // init module
    NULL,                                        // init process
    NULL,                                        // init thread
    NULL,                                        // exit thread
    NULL,                                        // exit process
    NULL,                                        // exit master
    NGX_MODULE_V1_PADDING
};

static char *ngx_http_hello(ngx_conf_t *cf, ngx_command_t *cmd, void *conf) {
    ngx_http_core_loc_conf_t *clcf;
    clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
    clcf->handler = ngx_http_hello_handler;

    return NGX_CONF_OK;
}

static ngx_int_t ngx_http_hello_handler(ngx_http_request_t *r)
{
    u_char *ngx_hello_world = (u_char *) "hello world";
    size_t sz = strlen((const char *)ngx_hello_world);

    r->headers_out.content_type.len = strlen("text/html") - 1;
    r->headers_out.content_type.data = (u_char *) "text/html";
    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_length_n = sz;
    ngx_http_send_header(r);

    ngx_buf_t *b;
    ngx_chain_t *out;
    b = ngx_calloc_buf(r->pool);
    out = ngx_alloc_chain_link(r->pool);
    out->buf = b;
    out->next = NULL;
    b->pos = ngx_hello_world;
    b->last = ngx_hello_world + sz;
    b->memory = 1;
    b->last_buf = 1;

    return ngx_http_output_filter(r, out);
}
