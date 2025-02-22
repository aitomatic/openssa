from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import TYPE_CHECKING

from loguru import logger
from tqdm import tqdm

from data_and_knowledge import FbId, Answer, FB_IDS, DOC_NAMES_BY_FB_ID, QS_BY_FB_ID, OUTPUT_FILE_PATH, get_or_create_output_df  # noqa: E501
from log import switch_log_file

if TYPE_CHECKING:
    from pandas import DataFrame


type QAFunc = Callable[[FbId], Answer]


@dataclass
class log_qa_and_update_output_file:  # noqa: N801
    output_name: str

    def __call__(self, qa_func: QAFunc) -> QAFunc:
        @wraps(wrapped=qa_func)
        def decorated_qa_func(fb_id: FbId) -> Answer:
            switch_log_file(fb_id=fb_id, output_name=self.output_name)

            logger.info((question := f'\n{fb_id}\n{DOC_NAMES_BY_FB_ID[fb_id]}:\n{QS_BY_FB_ID[fb_id]}\n') +
                        '\n... solving process starting ...\n',
                        depth=1)

            logger.info(question + (f'\n{self.output_name.upper()}:\n'
                                    f'{(answer := qa_func(fb_id)).replace('{', '{{').replace('}', '}}')}\n'),
                        depth=1)

            output_df: DataFrame = get_or_create_output_df()
            output_df.loc[fb_id, self.output_name]: str = answer
            output_df.to_csv(OUTPUT_FILE_PATH, index=True)

            return answer

        return decorated_qa_func
