from datetime import datetime

import pytest

from dho_scraper.items import DhOMessage


@pytest.fixture
def dho_msg() -> DhOMessage:
    return DhOMessage(
        msg_id=15662490,
        thread_id=15662491,
        title='10 things you disagree with Classical Buddhism',
        author='A. Dietrich Ringle',
        date=datetime(2019, 9, 14, 8, 13, 24),
        msg='Lists are handy things, and in this case they line up with brain wave function.<br /><br />I&#39;ll be surprised.',
        is_first_in_thread=True,
    )
