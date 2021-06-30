#pragma once
#include <rime_api.h>
#include <stdio.h>
#include <stdlib.h>

#define RIME_DATA_DIR "/usr/share/rime-data"
#define RIME_USER_DIR "/home/cycatz/.config/tmux_rime/rime"
#define RIME_WRAPPER_VERSION "0.0.1"  

#define rime_wrapper_malloc(x, size, ret) \
    do {                               \
        (x) = malloc((size));          \
        if ((x) == NULL) {             \
            perror("malloc\n");        \
            return (ret);              \
        }                              \
    } while (0)

typedef struct _RimeWrapper {
    RimeSessionId session_id;
    RimeApi *api;
    int first_run;
} RimeWrapper;  

void rime_wrapper_notification_handler(void*, RimeSessionId, const char*, const char*);
int  rime_wrapper_process_key(RimeWrapper *, int, int);
int  rime_wrapper_commit_composition(RimeWrapper *);

char *rime_wrapper_get_input_str(RimeWrapper *);
void rime_wrapper_free_str(char *);

void rime_wrapper_set_cursor_pos(RimeWrapper *, int);
void rime_wrapper_clear_composition(RimeWrapper *);

RimeCommit *rime_wrapper_get_commit(RimeWrapper *);
void  rime_wrapper_free_commit(RimeWrapper *, RimeCommit *);

RimeContext *rime_wrapper_get_context(RimeWrapper *);
void rime_wrapper_free_context(RimeWrapper *, RimeContext *);

RimeSchemaList *rime_wrapper_get_schema_list(RimeWrapper *);
void rime_wrapper_free_schema_list(RimeWrapper *, RimeSchemaList *);

int  rime_wrapper_set_schema(RimeWrapper *, const char *);
int  rime_wrapper_start(RimeWrapper *, int);
int  rime_wrapper_finish(RimeWrapper *);
RimeWrapper *rime_wrapper_init(void);
