/**********************************************************************************************************************
 *                                                                                                                    *
 * ngx_http_mytest_module.c                                                                                           *
 * author: Fu Xuanming (Waitspring)                                                                                   *
 *                                                                                                                    *
 **********************************************************************************************************************
 *
 */

#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>

static char *ngx_http_mytest(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
static ngx_int_t ngx_http_mytest_handler(ngx_http_request_t *r);
static ngx_command_t ngx_http_mytest_commands[] = {
    {
        ngx_string("mytest"),
        NGX_HTTP_MAIN_CONF | NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF | NGX_CONF_NOARGS,
        ngx_http_mytest,
        NGX_HTTP_LOC_CONF_OFFSET,
        0,
        NULL
    },
    ngx_null_command
};
static ngx_http_module_t ngx_http_mytest_module_ctx = {
    NULL,                                        // preconfiguration
    NULL,                                        // postconfiguration
    NULL,                                        // create main configuration
    NULL,                                        // init main configuration
    NULL,                                        // create server configuration
    NULL,                                        // merge server configuration
    NULL,                                        // create location configuration
    NULL                                         // merge location configuration
};

ngx_module_t ngx_http_mytest_module = {
    NGX_MODULE_V1,
   &ngx_http_mytest_module_ctx,                  // module context
    ngx_http_mytest_commands,                    // module directives
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

static char *ngx_http_mytest(ngx_conf_t *cf, ngx_command_t *cmd, void *conf) {
    ngx_http_core_loc_conf_t *clcf;
    clcf = ngx_http_conf_get_module_loc_conf(cd, ngx_http_core_module);
    clcf->handler = ngx_http_mytest_handler;
    return NGX_CONF_OK;
}

static ngx_int_t ngx_http_mytest_handler(ngx_http_request_t *r) {
    if (!(r->method & (NGX_HTTP_GET | NGX_HTTP_HEAD))) {
        return NGX_HTTP_NOT_ALLOWED;
    }
    ngx_int_t rc = ngx_http_discard_request_body(r);
    if (rc != NGX_OK) {
        return rc;
    }
    ngx_buf_t *b;
    b = ngx_palloc(r->pool, sizeof(ngx_buf_t));
    u_char* filename = (u_char*)"/tmp/test.txt";
    b->in_file = 1;
    b->file = ngx_pcalloc(r->pool, sizeof(ngx_file_t));
    b->file->fd = ngx_open_file(filename, NGX_FILE_RDONLY | NGX_FILE_NONBLOCK, NGX_FILE_OPEN, 0);
    b->file->log = r->connection->log;
    b->file->name.data = filename;
    b->file->name.len = sizeof(filename) - 1;
    if (b->file->fd <= 0)
    {
        return NGX_HTTP_NOT_FOUND;
    }
    r->allow_ranges = 1;
    if (ngx_file_info(filename, &b->file->info) == NGX_FILE_ERROR)
    {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    b->file_pos = 0;
    b->file_last = b->file->info.st_size;
    ngx_pool_cleanup_t* cln = ngx_pool_cleanup_add(r->pool, sizeof(ngx_pool_cleanup_file_t));
    if (cln == NULL)
    {
        return NGX_ERROR;
    }
    cln->handler = ngx_pool_cleanup_file;
    ngx_pool_cleanup_file_t *clnf = cln->data;
    clnf->fd = b->file->fd;
    clnf->name = b->file->name.data;
    clnf->log = r->pool->log;
    ngx_str_t type = ngx_string("text/plain");
    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_length_n = b->file->info.st_size;
    r->headers_out.content_type = type;
    rc = ngx_http_send_header(r);
    if (rc == NGX_ERROR || rc > NGX_OK || r->header_only)
    {
        return rc;
    }
    ngx_chain_t out;
    out.buf = b;
    out.next = NULL;
    return ngx_http_output_filter(r, &out);
}
