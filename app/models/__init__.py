"""
Импорт производится в пределах одного Python-пакета
app/models, чтобы не разбираться, какие между
моделями отношения, проще импортировать их сразу все.
"""

from .charity_project import CharityProject # noqa
from .donation import Donation # noqa
from .user import User # noqa
