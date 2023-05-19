# -*- coding: utf-8 -*-

from ctypes import *
from rime_wrapper.raw import *

class RimeWrapper:
    def __init__(self):
        self.rime_wrapper_ptr = rime_wrapper_init()

    def start(self):
        rime_wrapper_start(self.rime_wrapper_ptr, 0)

    def has_composition(self, _context=None):
        new_created = False
        if _context is None:
            new_created = True
            _context = rime_wrapper_get_context(self.rime_wrapper_ptr)
        res = _context.contents.composition is not None and _context.contents.composition.length > 0
        if new_created:
            rime_wrapper_free_context(self.rime_wrapper_ptr, _context)

        return res

    def has_candidates(self, _context=None):
        new_created = False
        if _context is None:
            new_created = True
            _context = rime_wrapper_get_context(self.rime_wrapper_ptr)

        res = _context.contents.menu.page_size > 0
        if new_created:
            rime_wrapper_free_context(self.rime_wrapper_ptr, _context)

        return res

    def get_schema_list(self):
        _schema_list = rime_wrapper_get_schema_list(self.rime_wrapper_ptr)

        list_size = _schema_list.contents.size
        schema_list = _schema_list.contents.list

        items = []
        for i in range(list_size):
            schema = schema_list[i]
            items.append((schema.schema_id.decode('utf-8'),
                          schema.name.decode('utf-8')))
        rime_wrapper_free_schema_list(self.rime_wrapper_ptr, _schema_list)
        return items

    def set_schema(self, schema_id):
        return rime_wrapper_set_schema(self.rime_wrapper_ptr, c_char_p(schema_id.encode('utf-8')))

    def get_commit_text_preview(self):
        _context = rime_wrapper_get_context(self.rime_wrapper_ptr)
        commit_text_preview = _context.contents.commit_text_preview.decode('utf-8')
        rime_wrapper_free_context(self.rime_wrapper_ptr, _context)

        return commit_text_preview

    def get_candidates(self):
        _context = rime_wrapper_get_context(self.rime_wrapper_ptr)
        menu = _context.contents.menu

        candidates = []

        if self.has_candidates():
            page_size = menu.page_size
            page_no = menu.page_no
            num_candidates = menu.num_candidates
            _candidates = menu.candidates

            for i in range(num_candidates):
                candidate = _candidates[i]

                text = candidate.text.decode('utf-8')
                comment = ''
                if candidate.comment is not None:
                    comment = candidate.comment.decode('utf-8')
                candidates.append((text, comment))

        rime_wrapper_free_context(self.rime_wrapper_ptr, _context)
        return candidates

    def get_composition(self):
        _context = rime_wrapper_get_context(self.rime_wrapper_ptr)

        composition = RimeComposition()
        if self.has_composition(_context):
            # Deep copy
            composition = RimeComposition(_context.contents.composition.length,
                                          _context.contents.composition.cursor_pos,
                                          _context.contents.composition.sel_start,
                                          _context.contents.composition.sel_end,
                                          _context.contents.composition.preedit)

        rime_wrapper_free_context(self.rime_wrapper_ptr, _context)

        return composition

    def get_composition_preedit(self):
        _context = rime_wrapper_get_context(self.rime_wrapper_ptr)

        composition_preedit = ''
        if self.has_composition(_context):
            composition_preedit = _context.contents.composition.preedit.decode('utf-8')

        rime_wrapper_free_context(self.rime_wrapper_ptr, _context)
        return composition_preedit


    def get_commit_text_preview(self):
        _context = rime_wrapper_get_context(self.rime_wrapper_ptr)

        commit_text_preview = ''
        _commit_text_preview = _context.contents.commit_text_preview
        if _commit_text_preview is not None:
            commit_text_preview = _commit_text_preview.decode('utf-8')
        rime_wrapper_free_context(self.rime_wrapper_ptr, _context)
        return commit_text_preview
    # def get_context(self):
    #     _context = rime_wrapper_get_context(self.rime_wrapper_ptr)
    #     commit_text_preview = _context.contents.commit_text_preview.decode('utf-8')
    #     select_labels = _context.contents.select_labels
    #     rime_wrapper_free_context(self.rime_wrapper_ptr, _context)

    def get_commit(self):
        _commit = rime_wrapper_get_commit(self.rime_wrapper_ptr)

        text = ''
        if _commit is None:
            return None
        else:
            try:
                data_size = _commit.contents.data_size
                text = _commit.contents.text.decode('utf-8')
            except ValueError:  # Ignore the error when contents is None
                pass

        rime_wrapper_free_commit(self.rime_wrapper_ptr, _commit)
        return text

    def process_key(self, keycode, mask):
        return rime_wrapper_process_key(self.rime_wrapper_ptr, keycode, mask)


    def commit_composition(self):
        return rime_wrapper_commit_composition(self.rime_wrapper_ptr)

    def clear_composition(self):
        rime_wrapper_clear_composition(self.rime_wrapper_ptr)

    def get_input_str(self):
        _input_str = rime_wrapper_get_input_str(self.rime_wrapper_ptr)
        if _input_str is None:
            print('Error!')
            return ''
        else:
            input_str = cast(_input_str, c_char_p).value.decode('utf-8')
            rime_wrapper_free_str(_input_str)
            return input_str

    def finish(self):
        rime_wrapper_finish(self.rime_wrapper_ptr)


# rime_wrapper.start()
# rime_wrapper.finish()
