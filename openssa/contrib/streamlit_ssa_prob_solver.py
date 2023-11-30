"""ChatSSA Streamlit Component."""


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
    KnowledgeSrcHash: type = DirOrFilePath | FilePathSet  # type for knowledge source hashes

    # relevant Streamlit Session State (SSS) elements
    # ===============================================
    KNOWLEDGE_SRC_PATHS_SSS_KEY: str = '_knowledge_src_paths'
    KNOWLEDGE_SRC_FILE_RELPATH_SETS_SSS_KEY: str = '_knowledge_src_file_relpath_sets'

    SSAS_SSS_KEY: str = '_ssas'
    SSA_CONVO_IDS_SSS_KEY: str = '_ssa_convo_ids'
    SSA_INTROS_SSS_KEY: str = '_ssa_intros'

    SSA_CONVO_NEXTQ_SSS_KEY: str = '_ssa_nextq'
    SSA_CONVO_QBOX_SSS_KEY: str = '_ssa_qbox'

    def __init__(self, unique_name: Uid,
                 knowledge_src_path: DirOrFilePath = '', knowledge_src_file_relpaths: FilePathSet = frozenset()):
        """Initialize and start running SSAProbSolver instance."""
        # initialize Streamlit Session State (SSS) elements if necessary
        # (this has to be done upon each instantiation
        # to avoid missing-state errors on multiple Streamlit sessions)
        self._init_sss()

        # set Unique Name
        assert unique_name, ValueError('SSAProbSolver instance requires explicit Unique Name')
        self.unique_name: self.Uid = unique_name

        # set Knowledge Source Path & any specific File Relative Paths if given
        if knowledge_src_path:
            self.knowledge_src_path: DirOrFilePath = knowledge_src_path
            if knowledge_src_file_relpaths:
                self.knowledge_src_file_relpaths: FilePathSet = knowledge_src_file_relpaths

        # start running in Streamlit app page
        self.run()

    @classmethod
    def _init_sss(cls):
        if cls.KNOWLEDGE_SRC_PATHS_SSS_KEY not in sss:
            sss[cls.KNOWLEDGE_SRC_PATHS_SSS_KEY]: defaultdict[cls.Uid, DirOrFilePath] = defaultdict(str)

        if cls.KNOWLEDGE_SRC_FILE_RELPATH_SETS_SSS_KEY not in sss:
            sss[cls.KNOWLEDGE_SRC_FILE_RELPATH_SETS_SSS_KEY]: defaultdict[cls.Uid, defaultdict[DirOrFilePath, FilePathSet]] = \
                defaultdict(lambda: defaultdict(frozenset))

        if cls.SSAS_SSS_KEY not in sss:
            sss[cls.SSAS_SSS_KEY]: defaultdict[cls.KnowledgeSrcHash, RagSSA | None] = defaultdict(lambda: None)

        if cls.SSA_CONVO_IDS_SSS_KEY not in sss:
            sss[cls.SSA_CONVO_IDS_SSS_KEY]: defaultdict[cls.KnowledgeSrcHash, cls.Uid] = defaultdict(uuid4)

        if cls.SSA_INTROS_SSS_KEY not in sss:
            sss[cls.SSA_INTROS_SSS_KEY]: defaultdict[cls.KnowledgeSrcHash, str] = defaultdict(str)

    @property
    def knowledge_src_path(self) -> DirOrFilePath:
        return sss[self.KNOWLEDGE_SRC_PATHS_SSS_KEY][self.unique_name]

    @knowledge_src_path.setter
    def knowledge_src_path(self, path: DirOrFilePath, /):
        assert (clean_path := path.strip().rstrip('/')), ValueError(f'{path} not non-empty path')

        if clean_path != sss[self.KNOWLEDGE_SRC_PATHS_SSS_KEY][self.unique_name]:
            sss[self.KNOWLEDGE_SRC_PATHS_SSS_KEY][self.unique_name]: DirOrFilePath = clean_path

    @property
    def _knowledge_file_src(self) -> FileSource:
        assert (_ := self.knowledge_src_path), ValueError('Knowledge Source Path not yet specified')
        return FileSource(_)

    @property
    def knowledge_src_file_relpaths(self) -> FilePathSet:
        assert self._knowledge_file_src.is_dir, ValueError('Knowledge Source Path not directory')

        return sss[self.KNOWLEDGE_SRC_FILE_RELPATH_SETS_SSS_KEY][self.unique_name][self.knowledge_src_path]

    @knowledge_src_file_relpaths.setter
    def knowledge_src_file_relpaths(self, file_relpaths: Iterable[str], /):
        assert self._knowledge_file_src.is_dir, ValueError('Knowledge Source Path not directory')

        if ((file_relpath_set := frozenset(file_relpaths)) !=  # noqa: W504
                sss[self.KNOWLEDGE_SRC_FILE_RELPATH_SETS_SSS_KEY][self.unique_name][self.knowledge_src_path]):
            sss[self.KNOWLEDGE_SRC_FILE_RELPATH_SETS_SSS_KEY][self.unique_name][self.knowledge_src_path]: FilePathSet = \
                file_relpath_set

    @property
    def _hashable_knowledge_src_repr(self) -> KnowledgeSrcHash:
        """Return a hashable representation of Knowledge Source."""
        if self._knowledge_file_src.is_dir and (knowledge_src_file_relpaths := self.knowledge_src_file_relpaths):
            return frozenset(f'{self.knowledge_src_path}/{_}' for _ in knowledge_src_file_relpaths)

        return self.knowledge_src_path

    @property
    def ssa(self) -> RagSSA | None:
        if ssa := sss[self.SSAS_SSS_KEY][self._hashable_knowledge_src_repr]:
            return ssa

        if st.button(label='Build SSA',
                     key=None,
                     on_click=None, args=None, kwargs=None,
                     type='secondary',
                     disabled=False,
                     use_container_width=False):
            ssa: RagSSA = LlamaIndexSSM()

            st.write('_Building SSA, please wait..._')

            if self._knowledge_file_src.on_s3:
                ssa.read_s3(self._hashable_knowledge_src_repr)
            else:
                ssa.read_directory(self.knowledge_src_path)

            st.write('_SSA ready!_')

            sss[self.SSAS_SSS_KEY][self._hashable_knowledge_src_repr]: RagSSA = ssa
            return ssa

        return None

    @property
    def ssa_convo_id(self) -> Uid:
        return sss[self.SSA_CONVO_IDS_SSS_KEY][self._hashable_knowledge_src_repr]

    def reset_ssa_convo_id(self):
        sss[self.SSA_CONVO_IDS_SSS_KEY][self._hashable_knowledge_src_repr]: self.Uid = uuid4()

    @property
    def ssa_intro(self) -> str:
        if not sss[self.SSA_INTROS_SSS_KEY][self._hashable_knowledge_src_repr]:
            self.reset_ssa_convo_id()

            sss[self.SSA_INTROS_SSS_KEY][self._hashable_knowledge_src_repr]: str = \
                self.ssa.discuss(user_input=(('In 100 words, summarize your expertise '
                                              'after you have read the following documents: '
                                              '(do NOT restate these sources in your answer)\n') +  # noqa: W504
                                             '\n'.join([self.knowledge_src_path])),
                                 conversation_id=self.ssa_convo_id)['content']

            self.reset_ssa_convo_id()

        return sss[self.SSA_INTROS_SSS_KEY][self._hashable_knowledge_src_repr]

    def ssa_discuss(self):
        def submit_question():
            # discuss if question box is not empty
            if (next_question := sss[self.SSA_CONVO_QBOX_SSS_KEY].strip()):
                self.ssa.discuss(user_input=next_question, conversation_id=self.ssa_convo_id)

            # empty question box
            sss[self.SSA_CONVO_QBOX_SSS_KEY]: str = ''

        st.text_area(label='Next Question', height=3,
                     key=self.SSA_CONVO_QBOX_SSS_KEY, on_change=submit_question)

        for msg in self.ssa.conversations.get(self.ssa_convo_id, []):
            st.write(f"{'__YOU__' if (msg['role'] == 'user') else '__SSA__'}: {msg['content']}")

    def run(self):
        """Run ChatSSA Streamlit Component on Streamlit app page."""
        st.subheader(f'Small Specialist Agent (SSA): {self.unique_name}')

        if knowledge_src_path := st.text_input(label='DOCUMENTARY KNOWLEDGE Source Path (Local|GCS|GDrive|S3)',
                                               value=self.knowledge_src_path,
                                               max_chars=None,
                                               key=None,
                                               type='default',
                                               help='DOCUMENTARY KNOWLEDGE Source Path (Local|GCS|GDrive|S3)',
                                               autocomplete=None,
                                               on_change=None, args=None, kwargs=None,
                                               placeholder=None,
                                               disabled=False,
                                               label_visibility='visible'):
            self.knowledge_src_path: DirOrFilePath = knowledge_src_path

            if self._knowledge_file_src.is_dir:
                self.knowledge_src_file_relpaths: FilePathSet = frozenset(st.multiselect(
                    label='(if cherry-picking) Specific Knowledge Source File Relative Paths',
                    options=self._knowledge_file_src.file_paths(relative=True),
                    default=sorted(self.knowledge_src_file_relpaths),
                    # format_func=None,
                    key=None,
                    help='(if cherry-picking) Specific Knowledge Source File Relative Paths',
                    on_change=None, args=None, kwargs=None,
                    disabled=False,
                    label_visibility='visible',
                    max_selections=None))

            st.write('EXPERIENTIAL KNOWLEDGE')
            experiential_knowledge = speech_to_text(start_prompt='Start Recording', stop_prompt='Stop Recording',
                                                    just_once=False,
                                                    use_container_width=False,
                                                    language='en',
                                                    callback=None, args=(), kwargs={},
                                                    key=None)
            st.write(experiential_knowledge)

            if self.ssa:
                st.write(f'__MY SPECIALIZED EXPERTISE:__ {self.ssa_intro}')

                if st.button(label='Reset Discussion',
                             key=None,
                             on_click=None, args=None, kwargs=None,
                             type='secondary',
                             disabled=False,
                             use_container_width=False):
                    self.reset_ssa_convo_id()

                self.ssa_discuss()
