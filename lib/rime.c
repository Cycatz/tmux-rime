#include "rime.h"

void tmux_rime_notification_handler(void* context_object,
                                    RimeSessionId session_id,
                                    const char* message_type,
                                    const char* message_value)

{
}

int tmux_rime_process_key(TmuxRime *tmux_rime, int keycode, int mask)
{
    if (!tmux_rime->api->process_key(tmux_rime->session_id, keycode, mask)) {
        return -1;
    }
    return 0;
}

int tmux_rime_get_commit(TmuxRime *tmux_rime)
{
    RIME_STRUCT(RimeCommit, commit);
    if (!tmux_rime->api->get_commit(tmux_rime->session_id, &commit)) {
        return -1;
    }
    if (!commit.text) {
        return -2;
    }
    printf("%s\n", commit.text); 
    tmux_rime->api->free_commit(&commit);

    return 0;
}


int tmux_rime_get_schemas(TmuxRime *tmux_rime)
{

    RimeSchemaList schema_list;

    if (!tmux_rime->api->get_schema_list(&schema_list)) {
        return -1;
    }

    for (int i = 0; i < schema_list.size; i++) {
        RimeSchemaListItem item = schema_list.list[i];
        printf("%s %s\n", item.schema_id, item.name);
    }
    tmux_rime->api->free_schema_list(&schema_list);

    return 0;
}

int tmux_rime_set_schema(TmuxRime *tmux_rime, const char *schema_id)
{

    if (!tmux_rime->api->select_schema(tmux_rime->session_id, schema_id)) {
        return -1;
    }

    return 0;
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

    // wait for deploy
    tmux_rime->api->join_maintenance_thread();
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

TmuxRime *tmux_rime_init()
{
    TmuxRime *tmux_rime;
    tmux_rime_malloc(tmux_rime, sizeof(TmuxRime), NULL);  

    tmux_rime->first_run = 1;
    tmux_rime->api = rime_get_api();
    if (!tmux_rime->api) {
        free(tmux_rime);      
        return NULL;
    }

    return tmux_rime; 
    // tmux_rime_start(tmux_rime, 0);
    // tmux_rime_get_schemas(tmux_rime);
    // tmux_rime_get_commit(tmux_rime);
    // tmux_rime_finish(tmux_rime);
    // return 0;
}

/*
int main()
{
    tmux_rime_init();
}
*/
