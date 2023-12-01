"""SSA Problem-Solver Streamlit Component."""


from collections.abc import Iterable, MutableMapping, Sequence
from collections import defaultdict
from uuid import UUID, uuid4

import streamlit as st
from streamlit_mic_recorder import speech_to_text

from openssa import LlamaIndexSSM
from openssa.core.ssa.ssa import RagSSA
from openssa.utils.fs import DirOrFilePath, FilePathSet, FileSource


__all__: Sequence[str] = ('SSAProbSolver',)


# Streamlit Session State alias "SSS" for brevity
sss: MutableMapping = st.session_state


class SSAProbSolver:
    """SSA Problem-Solver Streamlit Component."""

    # some typing for clarity to developers/maintainers
    # =================================================
    Uid: type = int | str | UUID  # accepted type(s) for unique IDs of SSAProbSolver instances & SSA conversations
    DocSrcHash: type = DirOrFilePath | FilePathSet  # type for documentary knowledge source hashes

    # relevant Streamlit Session State (SSS) elements
    # ===============================================
    DOC_SRC_PATHS_SSS_KEY: str = '_doc_src_paths'
    DOC_SRC_FILE_RELPATH_SETS_SSS_KEY: str = '_doc_src_file_relpath_sets'

    EXPERT_INSTRUCTIONS_SSS_KEY: str = '_expert_instructions'

    SSAS_SSS_KEY: str = '_ssas'
    SSA_CONVO_IDS_SSS_KEY: str = '_ssa_convo_ids'
    SSA_INTROS_SSS_KEY: str = '_ssa_intros'

    SSA_CONVO_NEXTQ_SSS_KEY: str = '_ssa_nextq'
    SSA_CONVO_QBOX_SSS_KEY: str = '_ssa_qbox'

    def __init__(self, unique_name: Uid,
                 doc_src_path: DirOrFilePath = '', doc_src_file_relpaths: FilePathSet = frozenset()):
        """Initialize and start running SSAProbSolver instance."""
        # initialize Streamlit Session State (SSS) elements if necessary
        # (this has to be done upon each instantiation
        # to avoid missing-state errors on multiple Streamlit sessions)
        self._init_sss()

        # set Unique Name
        assert unique_name, ValueError('SSAProbSolver instance requires explicit Unique Name')
        self.unique_name: self.Uid = unique_name

        # set Documentary Knowledge Source Path & any specific File Relative Paths if given
        if doc_src_path:
            self.doc_src_path: DirOrFilePath = doc_src_path
            if doc_src_file_relpaths:
                self.doc_src_file_relpaths: FilePathSet = doc_src_file_relpaths

        # start running in Streamlit app page
        self.run()

    @classmethod
    def _init_sss(cls):
        if cls.DOC_SRC_PATHS_SSS_KEY not in sss:
            sss[cls.DOC_SRC_PATHS_SSS_KEY]: defaultdict[cls.Uid, DirOrFilePath] = defaultdict(str)

        if cls.DOC_SRC_FILE_RELPATH_SETS_SSS_KEY not in sss:
            sss[cls.DOC_SRC_FILE_RELPATH_SETS_SSS_KEY]: defaultdict[cls.Uid, defaultdict[DirOrFilePath, FilePathSet]] = \
                defaultdict(lambda: defaultdict(frozenset))

        if cls.EXPERT_INSTRUCTIONS_SSS_KEY not in sss:
            sss[cls.EXPERT_INSTRUCTIONS_SSS_KEY]: defaultdict[cls.Uid, str] = defaultdict(str)

        if cls.SSAS_SSS_KEY not in sss:
            sss[cls.SSAS_SSS_KEY]: defaultdict[cls.DocSrcHash, RagSSA | None] = defaultdict(lambda: None)

        if cls.SSA_CONVO_IDS_SSS_KEY not in sss:
            sss[cls.SSA_CONVO_IDS_SSS_KEY]: defaultdict[cls.DocSrcHash, cls.Uid] = defaultdict(uuid4)

        if cls.SSA_INTROS_SSS_KEY not in sss:
            sss[cls.SSA_INTROS_SSS_KEY]: defaultdict[cls.DocSrcHash, str] = defaultdict(str)

    @property
    def doc_src_path(self) -> DirOrFilePath:
        return sss[self.DOC_SRC_PATHS_SSS_KEY][self.unique_name]

    @doc_src_path.setter
    def doc_src_path(self, path: DirOrFilePath, /):
        assert (clean_path := path.strip().rstrip('/')), ValueError(f'{path} not non-empty path')

        if clean_path != sss[self.DOC_SRC_PATHS_SSS_KEY][self.unique_name]:
            sss[self.DOC_SRC_PATHS_SSS_KEY][self.unique_name]: DirOrFilePath = clean_path

    @property
    def _doc_file_src(self) -> FileSource:
        assert (_ := self.doc_src_path), ValueError('Documentary Knowledge Source Path not yet specified')
        return FileSource(_)

    @property
    def doc_src_file_relpaths(self) -> FilePathSet:
        assert self._doc_file_src.is_dir, ValueError('Documentary Knowledge Source Path not directory')

        return sss[self.DOC_SRC_FILE_RELPATH_SETS_SSS_KEY][self.unique_name][self.doc_src_path]

    @doc_src_file_relpaths.setter
    def doc_src_file_relpaths(self, file_relpaths: Iterable[str], /):
        assert self._doc_file_src.is_dir, ValueError('Documentary Knowledge Source Path not directory')

        if ((file_relpath_set := frozenset(file_relpaths)) !=  # noqa: W504
                sss[self.DOC_SRC_FILE_RELPATH_SETS_SSS_KEY][self.unique_name][self.doc_src_path]):
            sss[self.DOC_SRC_FILE_RELPATH_SETS_SSS_KEY][self.unique_name][self.doc_src_path]: FilePathSet = \
                file_relpath_set

    @property
    def _hashable_doc_src_repr(self) -> DocSrcHash:
        """Return a hashable representation of Documentary Knowledge Source."""
        if self._doc_file_src.is_dir and (doc_src_file_relpaths := self.doc_src_file_relpaths):
            return frozenset(f'{self.doc_src_path}/{_}' for _ in doc_src_file_relpaths)

        return self.doc_src_path

    @property
    def expert_instructions(self) -> str:
        return sss[self.EXPERT_INSTRUCTIONS_SSS_KEY][self.unique_name]

    @expert_instructions.setter
    def expert_instructions(self, expert_instructions: str, /):
        if expert_instructions != sss[self.EXPERT_INSTRUCTIONS_SSS_KEY][self.unique_name]:
            sss[self.EXPERT_INSTRUCTIONS_SSS_KEY][self.unique_name]: str = expert_instructions

    @property
    def ssa(self) -> RagSSA | None:
        if ssa := sss[self.SSAS_SSS_KEY][self._hashable_doc_src_repr]:
            return ssa

        if st.button(label='Build SSA',
                     key=None,
                     on_click=None, args=None, kwargs=None,
                     type='secondary',
                     disabled=False,
                     use_container_width=False):
            ssa: RagSSA = LlamaIndexSSM()

            st.write('_Building SSA, please wait..._')

            if self._doc_file_src.on_s3:
                ssa.read_s3(self._hashable_doc_src_repr)
            else:
                ssa.read_directory(self.doc_src_path)

            st.write('_SSA ready!_')

            sss[self.SSAS_SSS_KEY][self._hashable_doc_src_repr]: RagSSA = ssa
            return ssa

        return None

    @property
    def ssa_convo_id(self) -> Uid:
        return sss[self.SSA_CONVO_IDS_SSS_KEY][self._hashable_doc_src_repr]

    def reset_ssa_convo_id(self):
        sss[self.SSA_CONVO_IDS_SSS_KEY][self._hashable_doc_src_repr]: self.Uid = uuid4()

    @property
    def ssa_intro(self) -> str:
        if not sss[self.SSA_INTROS_SSS_KEY][self._hashable_doc_src_repr]:
            self.reset_ssa_convo_id()

            sss[self.SSA_INTROS_SSS_KEY][self._hashable_doc_src_repr]: str = \
                self.ssa.discuss(user_input=(('In 100 words, summarize your expertise '
                                              'after you have read the following documents: '
                                              '(do NOT restate these sources in your answer)\n') +  # noqa: W504
                                             '\n'.join([self.doc_src_path])),
                                 conversation_id=self.ssa_convo_id)['content']

            self.reset_ssa_convo_id()

        return sss[self.SSA_INTROS_SSS_KEY][self._hashable_doc_src_repr]

    def ssa_solve(self):
        def submit_question():
            # discuss if question box is not empty
            if (next_question := sss[self.SSA_CONVO_QBOX_SSS_KEY].strip()):
                self.ssa.discuss(user_input=next_question, conversation_id=self.ssa_convo_id)

            # empty question box
            sss[self.SSA_CONVO_QBOX_SSS_KEY]: str = ''

        st.text_area(label='Next Problem', height=3,
                     key=self.SSA_CONVO_QBOX_SSS_KEY, on_change=submit_question)

        for msg in self.ssa.conversations.get(self.ssa_convo_id, []):
            st.write(f"{'__YOU__' if (msg['role'] == 'user') else '__SSA__'}: {msg['content']}")

    def run(self):
        """Run SSA Problem-Solver Streamlit Component on Streamlit app page."""
        st.subheader(self.unique_name)

        st.write('__DOCUMENTARY KNOWLEDGE SOURCE__:')

        if doc_src_path := st.text_input(label='Source File or Directory Path (Local or S3)',
                                         value=self.doc_src_path,
                                         max_chars=None,
                                         key=None,
                                         type='default',
                                         help='Source File or Directory Path (Local or S3)',
                                         autocomplete=None,
                                         on_change=None, args=None, kwargs=None,
                                         placeholder=None,
                                         disabled=False,
                                         label_visibility='visible'):
            self.doc_src_path: DirOrFilePath = doc_src_path

            if self._doc_file_src.is_dir:
                self.doc_src_file_relpaths: FilePathSet = frozenset(st.multiselect(
                    label='(if cherry-picking) Specific Source File Relative Paths',
                    options=self._doc_file_src.file_paths(relative=True),
                    default=sorted(self.doc_src_file_relpaths),
                    # format_func=None,
                    key=None,
                    help='(if cherry-picking) Specific Source File Relative Paths',
                    on_change=None, args=None, kwargs=None,
                    disabled=False,
                    label_visibility='visible',
                    max_selections=None))

        st.write('__EXPERIENTIAL KNOWLEDGE__:')
        recorded_expert_instructions = speech_to_text(start_prompt='Record Your Expert Instructions here or type below',
                                                      stop_prompt='Stop Recording',
                                                      just_once=False,
                                                      use_container_width=False,
                                                      language='en',
                                                      callback=None, args=(), kwargs={},
                                                      key=None)
        self.expert_instructions: str = st.text_area(label='Experiential Knowledge',
                                                     value=(recorded_expert_instructions or self.expert_instructions),
                                                     height=10,
                                                     max_chars=None,
                                                     key=None,
                                                     help='Experiential Knowledge (recorded or typed)',
                                                     on_change=None, args=None, kwargs=None,
                                                     placeholder=None,
                                                     disabled=False,
                                                     label_visibility='collapsed')

        if doc_src_path and self.ssa:
            st.write(f"__SSA's SPECIALIZED EXPERTISE__: {self.ssa_intro}")

            if st.button(label='Reset Problem-Solving Session',
                         key=None,
                         on_click=None, args=None, kwargs=None,
                         type='secondary',
                         disabled=False,
                         use_container_width=False):
                self.reset_ssa_convo_id()

            self.ssa_solve()
