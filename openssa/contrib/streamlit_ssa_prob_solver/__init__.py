"""SSA Problem-Solver Streamlit Component."""


from collections.abc import Iterable, MutableMapping, Sequence
from collections import defaultdict
from uuid import UUID

import streamlit as st
from streamlit_mic_recorder import speech_to_text

from openssa.core.ssa.ssa import RagSSA
from openssa.core.ooda_rag.heuristic import TaskDecompositionHeuristic
from openssa.core.ooda_rag.custom import CustomSSM
from openssa.core.ooda_rag.solver import OodaSSA
from openssa.utils.fs import DirOrFilePath, FilePathSet, FileSource
from openssa.utils.llm_config import LLMConfig


__all__: Sequence[str] = ('SSAProbSolver',)


# Streamlit Session State alias "SSS" for brevity
sss: MutableMapping = st.session_state


# github.com/streamlit/streamlit/issues/3587#issuecomment-1182896894
def update_multiselect_style():
    st.markdown(
        """
        <style>
            .stMultiSelect [data-baseweb="tag"] {
                height: fit-content;
            }
            .stMultiSelect [data-baseweb="tag"] span[title] {
                white-space: normal; max-width: 100%; overflow-wrap: anywhere;
            }
        </style>
        """,
        unsafe_allow_html=True)


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

    PROBLEMS_SSS_KEY: str = '_problems'
    EXPERT_HEURISTICS_SSS_KEY: str = '_expert_heuristics'
    FINE_TUNED_MODELS_SSS_KEY: str = '_fine_tuned_models'

    SSAS_SSS_KEY: str = '_ssas'

    def __init__(self, unique_name: Uid, domain: str = '',
                 problem: str = '', expert_heuristics: str = '',
                 fine_tuned_model_url: str = '',
                 doc_src_path: DirOrFilePath = '', doc_src_file_relpaths: FilePathSet = frozenset()):
        # pylint: disable=too-many-arguments
        """Initialize and start running SSAProbSolver instance."""
        # initialize Streamlit Session State (SSS) elements if necessary
        # (this has to be done upon each instantiation to avoid missing-state errors on multiple Streamlit sessions)
        self._init_sss()

        # set Unique Name
        assert unique_name, ValueError('SSAProbSolver instance requires explicit Unique Name')
        self.unique_name: self.Uid = unique_name

        # set Domain
        self.domain: str = domain.strip()

        # set Problem
        if not self.problem:
            self.problem: str = problem

        # set Expert Heuristics
        if not self.expert_heuristics:
            self.expert_heuristics: str = expert_heuristics

        # set Fine-Tuned Model URL
        if not self.fine_tuned_model_url:
            self.fine_tuned_model_url: str = fine_tuned_model_url

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

        if cls.PROBLEMS_SSS_KEY not in sss:
            sss[cls.PROBLEMS_SSS_KEY]: defaultdict[cls.Uid, str] = defaultdict(str)

        if cls.EXPERT_HEURISTICS_SSS_KEY not in sss:
            sss[cls.EXPERT_HEURISTICS_SSS_KEY]: defaultdict[cls.Uid, str] = defaultdict(str)

        if cls.FINE_TUNED_MODELS_SSS_KEY not in sss:
            sss[cls.FINE_TUNED_MODELS_SSS_KEY]: defaultdict[cls.Uid, str] = defaultdict(str)

        if cls.SSAS_SSS_KEY not in sss:
            sss[cls.SSAS_SSS_KEY]: defaultdict[cls.DocSrcHash, RagSSA | None] = defaultdict(lambda: None)

    @property
    def problem(self) -> str:
        return sss[self.PROBLEMS_SSS_KEY][self.unique_name]

    @problem.setter
    def problem(self, problem: str, /):
        if problem != sss[self.PROBLEMS_SSS_KEY][self.unique_name]:
            sss[self.PROBLEMS_SSS_KEY][self.unique_name]: str = problem

    @property
    def expert_heuristics(self) -> str:
        return sss[self.EXPERT_HEURISTICS_SSS_KEY][self.unique_name]

    @expert_heuristics.setter
    def expert_heuristics(self, expert_heuristics: str, /):
        if expert_heuristics != sss[self.EXPERT_HEURISTICS_SSS_KEY][self.unique_name]:
            sss[self.EXPERT_HEURISTICS_SSS_KEY][self.unique_name]: str = expert_heuristics

    def append_expert_heuristics(self, addl_expert_heuristics: str, /):
        self.expert_heuristics += f'\n{addl_expert_heuristics}'

    @property
    def fine_tuned_model_url(self) -> str:
        return sss[self.FINE_TUNED_MODELS_SSS_KEY][self.unique_name]

    @fine_tuned_model_url.setter
    def fine_tuned_model_url(self, fine_tuned_model_url: str, /):
        if fine_tuned_model_url != sss[self.FINE_TUNED_MODELS_SSS_KEY][self.unique_name]:
            sss[self.FINE_TUNED_MODELS_SSS_KEY][self.unique_name]: str = fine_tuned_model_url

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

        if (file_relpath_set := frozenset(file_relpaths)) != \
                sss[self.DOC_SRC_FILE_RELPATH_SETS_SSS_KEY][self.unique_name][self.doc_src_path]:
            sss[self.DOC_SRC_FILE_RELPATH_SETS_SSS_KEY][self.unique_name][self.doc_src_path]: FilePathSet = file_relpath_set

    @property
    def _hashable_doc_src_repr(self) -> DocSrcHash:
        """Return a hashable representation of Documentary Knowledge Source."""
        if self._doc_file_src.is_dir and (doc_src_file_relpaths := self.doc_src_file_relpaths):
            return frozenset(f'{self.doc_src_path}/{_}' for _ in doc_src_file_relpaths)

        return self.doc_src_path

    @property
    def ssa(self) -> RagSSA | None:
        if ssa := sss[self.SSAS_SSS_KEY][self._hashable_doc_src_repr]:
            return ssa

        if st.button(label='Build SSA',
                     key=None,
                     on_click=None,
                     args=None,
                     kwargs=None,
                     type="primary",
                     disabled=False,
                     use_container_width=False):
            llm = LLMConfig.get_llm_llama_2_70b()
            embed_model = LLMConfig.get_aito_embeddings()
            ssa: RagSSA = CustomSSM(llm=llm, embed_model=embed_model)

            st.write('_Building SSA, please wait..._')

            if self._doc_file_src.on_s3:
                ssa.read_s3(self._hashable_doc_src_repr)
            else:
                ssa.read_directory(self.doc_src_path)

            st.write('_SSA ready!_')

            sss[self.SSAS_SSS_KEY][self._hashable_doc_src_repr]: RagSSA = ssa
            return ssa

        return None

    def ssa_solve(self):
        ooda_ssa = OodaSSA(task_heuristics=TaskDecompositionHeuristic({}),
                           highest_priority_heuristic=self.expert_heuristics)

        ooda_ssa.activate_resources(self.doc_src_path)

        solution: str = ooda_ssa.solve(self.problem)

        st.write(solution)

    def run(self):
        """Run SSA Problem-Solver Streamlit Component on Streamlit app page."""
        st.header(body=self.unique_name, divider=not self.domain)
        if self.domain:
            st.subheader(body=f'domain: _{self.domain}_', divider=True)

        st.write('__PROBLEM TO SOLVE__')

        self.problem: str = st.text_area(label='Problem to Solve',
                                         value=self.problem,
                                         height=3,
                                         max_chars=None,
                                         key=None,
                                         help='State the Problem to Solve',
                                         on_change=None, args=None, kwargs=None,
                                         placeholder='What problem would you like to solve?',
                                         disabled=False,
                                         label_visibility='collapsed')

        st.write('__EXPERT HEURISTICS__')

        if recorded_expert_heuristics := speech_to_text(start_prompt='Expert Heuristics: 🎤 here or ⌨️ below',
                                                        stop_prompt='Stop Recording',
                                                        just_once=True,
                                                        use_container_width=False,
                                                        language='en',
                                                        callback=None, args=(), kwargs={},
                                                        key=None):
            if self.ssa:
                recorded_expert_heuristics: str = self.ssa.discuss(f"""
                    Given your understanding of the domain "{self.domain}",
                    please rectify and/or restructure the following recorded info
                    to make it clear and understandable to both humans and other processing engines:

                    {recorded_expert_heuristics}

                    Please return the rectified/restructured info in the form of at most 3 paragraphs.
                """)['content']

                st.write(f'"{recorded_expert_heuristics}"')

            else:
                st.write(f'_"{recorded_expert_heuristics}"_')

            st.button(label='append to saved heuristics below?',
                      key=None,
                      on_click=self.append_expert_heuristics, args=(recorded_expert_heuristics,), kwargs=None,
                      type='secondary',
                      disabled=False,
                      use_container_width=False)

        self.expert_heuristics: str = st.text_area(label='Expert Heuristics',
                                                   value=self.expert_heuristics,
                                                   height=10,
                                                   max_chars=None,
                                                   key=None,
                                                   help='Expert Heuristics (recorded or typed)',
                                                   on_change=None, args=None, kwargs=None,
                                                   placeholder='Expert Heuristics (recorded or typed)',
                                                   disabled=False,
                                                   label_visibility='collapsed')

        st.write('_(optional)_ __DOMAIN-FINE-TUNED MODEL__')

        self.fine_tuned_model_url: str = st.text_input(label='_(optional)_ Domain-Fine-Tuned Model URL',
                                                       value=self.fine_tuned_model_url,
                                                       max_chars=None,
                                                       type='default',
                                                       help='_(optional)_ Domain-Fine-Tuned Model URL',
                                                       autocomplete=None,
                                                       on_change=None,
                                                       args=None,
                                                       kwargs=None,
                                                       placeholder='(optional) Domain-Fine-Tuned Model URL',
                                                       disabled=False,
                                                       label_visibility='collapsed')

        st.write('__RESOURCES__ _(e.g., Documents, Sensors & Actuators)_')

        update_multiselect_style()

        if doc_src_path := st.text_input(label='Resources Directory/File Path _(Local/S3)_',
                                         value=self.doc_src_path,
                                         max_chars=None,
                                         type='default',
                                         help='Resources Directory/File Path _(Local/S3)_',
                                         autocomplete=None,
                                         on_change=None, args=None, kwargs=None,
                                         placeholder='Resources Directory/File Path (Local|S3)',
                                         disabled=False,
                                         label_visibility='visible'):
            self.doc_src_path: DirOrFilePath = doc_src_path

            if self._doc_file_src.is_dir:
                self.doc_src_file_relpaths: FilePathSet = frozenset(
                    st.multiselect(label='Specific File Relpaths _(if cherry-picking)_',
                                   options=self._doc_file_src.file_paths(relative=True),
                                   default=sorted(self.doc_src_file_relpaths),
                                   # format_func=None,
                                   key=None,
                                   help='Specific File Relpaths _(if cherry-picking)_',
                                   on_change=None, args=None, kwargs=None,
                                   disabled=False,
                                   label_visibility='visible',
                                   max_selections=None))

            if self.ssa and st.button(label=f'__SOLVE__: _{self.problem}_',
                                      key=None,
                                      on_click=None, args=None, kwargs=None,
                                      type='primary',
                                      disabled=False,
                                      use_container_width=False):
                self.ssa_solve()
