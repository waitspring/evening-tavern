/**********************************************************************************************************************
 *                                                                                                                    *
 * ngx_http_echo_module.c                                                                                             *
 * author: Fu Xuanming (Waitspring)                                                                                   *
 *                                                                                                                    *
 **********************************************************************************************************************
 *
 */

#include <ngx_config.h>
#include <ngx_core.h>

typedef struct
{
    ngx_str_t ed;  /* ngx_str_t: src/core/ngx_string.h */
} ngx_http_echo_loc_conf_t;

static char *ngx_http_echo(ngx_conf_t *cf, ngx_command_t *cmd, void *child);
static void *ngx_http_echo_create_loc_conf(ngx_conf_t *cf);
static char *ngx_http_echo_merge_loc_conf(ngx_conf_t *cf, void *parent, void *child);
static ngx_int_t ngx_http_echo_init(ngx_conf_t *cf);

static ngx_command_t ngx_http_echo_command[] = {
    {
        ngx_string("echo"),
        NGX_HTTP_LOC_CONF | NGX_CONF_TAKE1,
        ngx_http_echo,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_echo_loc_conf_t, ed),
        NULL
    },
    ngx_null_command
};