#include <rime_api.h>
#include <stdio.h>
#include <stdlib.h>

#define RIME_DATA_DIR "/usr/share/rime-data"
#define RIME_USER_DIR "/home/cycatz/.local/fcitx/rime"
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

void tmux_rime_notification_handler(void* context_object,
                                    RimeSessionId session_id,
                                    const char* message_type,
                                    const char* message_value)

{
}

int tmux_rime_start(TmuxRime *tmux_rime, int fullcheck)
{
    const char *shared_data_dir = RIME_DATA_DIR; 
    const char *user_data_dir = RIME_USER_DIR;

    RIME_STRUCT(RimeTraits, tmux_rime_traits); 
    tmux_rime_traits.shared_data_dir = shared_data_dir;
    tmux_rime_traits.user_data_dir = user_data_dir;
    tmux_rime_traits.app_name = "rime.tmux-rime"; 
    tmux_rime_traits.distribution_name = "Rime";
    tmux_rime_traits.distribution_code_name = "tmux-rime";
    tmux_rime_traits.distribution_version = TMUX_RIME_VERSION;

    if (tmux_rime->first_run) {
        tmux_rime->api->setup(&tmux_rime_traits);
        tmux_rime->first_run = 0;
    }
    tmux_rime->api->initialize(&tmux_rime_traits);
    tmux_rime->api->set_notification_handler(tmux_rime_notification_handler, tmux_rime);
    tmux_rime->api->start_maintenance(fullcheck); 

    tmux_rime->session_id = tmux_rime->api->create_session();

    printf("tmux-rime session id: %ld\n", tmux_rime->session_id);
    
    return 0;
}

int tmux_rime_finish(TmuxRime *tmux_rime)
{
    if (tmux_rime->session_id) {
        tmux_rime->api->destroy_session(tmux_rime->session_id);
        tmux_rime->session_id = 0;
    }
    tmux_rime->api->finalize();
    free(tmux_rime);
    return 0;
}

int tmux_rime_init()
{
    TmuxRime *tmux_rime;
    tmux_rime_malloc(tmux_rime, sizeof(TmuxRime), -1);  

    tmux_rime->first_run = 0;
    tmux_rime->api = rime_get_api();
    if (!tmux_rime->api) {
        free(tmux_rime);      
        return -1;
    }
    tmux_rime_start(tmux_rime, 0);
    tmux_rime_finish(tmux_rime);
    return 0;
}


int main()
{
    tmux_rime_init();
}
