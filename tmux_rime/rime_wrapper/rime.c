#include <string.h>

#include "rime.h"

// Redefine related macros for the pointer type
// #define RIME_STRUCT_INIT_P(Type, var) ((var)->data_size = sizeof(Type) - sizeof((var)->data_size))
#define RIME_STRUCT_P(Type, var) *var = (Type){0}; RIME_STRUCT_INIT(Type, *var);

static char *copy_string(const char *src)
{
    char *dst;
    size_t len = strlen(src);

    rime_wrapper_malloc(dst, len + 1, NULL);
    strcpy(dst, src); 
    dst[len] = '\0';

    return dst;
}

void rime_wrapper_notification_handler(void* context_object,
                                    RimeSessionId session_id,
                                    const char* message_type,
                                    const char* message_value)

{
}

int rime_wrapper_process_key(RimeWrapper *rime_wrapper, int keycode, int mask)
{
    if (!rime_wrapper->api->process_key(rime_wrapper->session_id, keycode, mask)) {
        return -1;
    }
    return 0;
}

int  rime_wrapper_commit_composition(RimeWrapper *rime_wrapper)
{
    if (!rime_wrapper->api->commit_composition(rime_wrapper->session_id)) {
        return -1;
    }
    return 0;
}

char *rime_wrapper_get_input_str(RimeWrapper *rime_wrapper)
{
    const char* input = rime_wrapper->api->get_input(rime_wrapper->session_id);
    if (!input) {
        return NULL;
    }
    return copy_string(input);
}

void rime_wrapper_free_str(char *str)
{
    free(str);
}

void rime_wrapper_set_cursor_pos(RimeWrapper *rime_wrapper, int pos)
{
    rime_wrapper->api->set_caret_pos(rime_wrapper->session_id, pos);
}

void rime_wrapper_clear_composition(RimeWrapper *rime_wrapper)
{
    rime_wrapper->api->clear_composition(rime_wrapper->session_id);
}

RimeCommit *rime_wrapper_get_commit(RimeWrapper *rime_wrapper)
{
    RimeCommit *commit;

    rime_wrapper_malloc(commit, sizeof(RimeCommit), NULL);   

    RIME_STRUCT_P(RimeCommit, commit);

    if (!rime_wrapper->api->get_commit(rime_wrapper->session_id, commit)) {
        return NULL;
    }

    return commit;
}

void rime_wrapper_free_commit(RimeWrapper *rime_wrapper, RimeCommit *commit)
{
    rime_wrapper->api->free_commit(commit);
    free(commit);
}


RimeContext *rime_wrapper_get_context(RimeWrapper *rime_wrapper)
{
    RimeContext *context;

    rime_wrapper_malloc(context, sizeof(RimeContext), NULL);   

    RIME_STRUCT_P(RimeContext, context);

    if (!rime_wrapper->api->get_context(rime_wrapper->session_id, context)) {
        return NULL;
    }

    return context;
}

void rime_wrapper_free_context(RimeWrapper *rime_wrapper, RimeContext *context)
{
    rime_wrapper->api->free_context(context);
    free(context);
}

RimeSchemaList *rime_wrapper_get_schema_list(RimeWrapper *rime_wrapper)
{
    RimeSchemaList *schema_list;  

    rime_wrapper_malloc(schema_list, sizeof(schema_list), NULL);   

    if (!rime_wrapper->api->get_schema_list(schema_list)) {
        return NULL;
    }
    return schema_list;
}

void rime_wrapper_free_schema_list(RimeWrapper *rime_wrapper, RimeSchemaList *schema_list)
{
    rime_wrapper->api->free_schema_list(schema_list);
    free(schema_list);
}

int rime_wrapper_set_schema(RimeWrapper *rime_wrapper, const char *schema_id)
{

    if (!rime_wrapper->api->select_schema(rime_wrapper->session_id, schema_id)) {
        return -1;
    }

    return 0;
}
int rime_wrapper_start(RimeWrapper *rime_wrapper, int fullcheck)
{
    const char *shared_data_dir = RIME_DATA_DIR; 
    const char *user_data_dir = RIME_USER_DIR;

    RIME_STRUCT(RimeTraits, rime_wrapper_traits); 
    rime_wrapper_traits.shared_data_dir = shared_data_dir;
    rime_wrapper_traits.user_data_dir = user_data_dir;
    rime_wrapper_traits.app_name = "rime.tmux-rime"; 
    rime_wrapper_traits.distribution_name = "Rime";
    rime_wrapper_traits.distribution_code_name = "tmux-rime";
    rime_wrapper_traits.distribution_version = RIME_WRAPPER_VERSION;

    if (rime_wrapper->first_run) {
        rime_wrapper->api->setup(&rime_wrapper_traits);
        rime_wrapper->first_run = 0;
    }
    rime_wrapper->api->initialize(&rime_wrapper_traits);
    rime_wrapper->api->set_notification_handler(rime_wrapper_notification_handler, rime_wrapper);
    rime_wrapper->api->start_maintenance(fullcheck); 

    rime_wrapper->session_id = rime_wrapper->api->create_session();

    // wait for deploy
    rime_wrapper->api->join_maintenance_thread();
    printf("tmux-rime session id: %ld\n", rime_wrapper->session_id);
    
    return 0;
}

int rime_wrapper_finish(RimeWrapper *rime_wrapper)
{
    if (rime_wrapper->session_id) {
        rime_wrapper->api->destroy_session(rime_wrapper->session_id);
        rime_wrapper->session_id = 0;
    }
    rime_wrapper->api->finalize();
    free(rime_wrapper);
    return 0;
}

RimeWrapper *rime_wrapper_init(void)
{
    RimeWrapper *rime_wrapper;
    rime_wrapper_malloc(rime_wrapper, sizeof(RimeWrapper), NULL);  

    rime_wrapper->first_run = 1;
    rime_wrapper->api = rime_get_api();
    if (!rime_wrapper->api) {
        free(rime_wrapper);      
        return NULL;
    }

    return rime_wrapper; 
    // rime_wrapper_start(rime_wrapper, 0);
    // rime_wrapper_get_schemas(rime_wrapper);
    // rime_wrapper_get_commit(rime_wrapper);
    // rime_wrapper_finish(rime_wrapper);
    // return 0;
}

/*
int main()
{
    rime_wrapper_init();
}
*/
