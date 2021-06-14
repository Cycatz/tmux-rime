#pragma once
#include <rime_api.h>
#include <stdio.h>
#include <stdlib.h>

#define RIME_DATA_DIR "/usr/share/rime-data"
#define RIME_USER_DIR "/home/cycatz/.config/fcitx/rime"
#define TMUX_RIME_VERSION "0.0.1"  

#define tmux_rime_malloc(x, size, ret) \
    do {                               \
        (x) = malloc((size));          \
        if ((x) == NULL) {             \
            perror("malloc\n");        \
            return (ret);              \
        }                              \
    } while (0)

typedef struct _TmuxRime {
    RimeSessionId session_id;
    RimeApi *api;
    int first_run;
} TmuxRime;  

void tmux_rime_notification_handler(void*, RimeSessionId, const char*, const char*);
int  tmux_rime_process_key(TmuxRime *, int, int);
int  tmux_rime_get_commit(TmuxRime *);
int  tmux_rime_get_schemas(TmuxRime *);
int  tmux_rime_set_schema(TmuxRime *, const char *);
int  tmux_rime_start(TmuxRime *, int);
int  tmux_rime_finish(TmuxRime *);
TmuxRime *tmux_rime_init();
