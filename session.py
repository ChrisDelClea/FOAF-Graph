# noinspection PyProtectedMember
from collections import Callable

from streamlit.report_thread import ReportThread
from streamlit.server.server import Server


def get_state(setup_func: Callable[..., T], **kwargs) -> T:
    ctx = ReportThread.get_report_ctx()

    session = None
    session_infos = Server.get_current()._session_infos.values()

    for session_info in session_infos:
        if session_info.session._main_dg == ctx.main_dg:
            session = session_info.session

    if session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')

    # Got the session object! Now let's attach some state into it.

    if not getattr(session, '_custom_session_state', None):
        session._custom_session_state = setup_func(**kwargs)

    return session._custom_session_state
