import pytest
from factories import RoleFactory
from zk.model.role import Role

pytestmark = pytest.mark.usefixtures("sqlite")


def test_default_roles():
    roles = Role.find_all()
    print roles
    assert False
