__author__ = "Adrian Weber, Centre for Development and Environment, University of Bern"
__date__ = "$Dec 12, 2012 3:52:32 PM$"

from decide_user.model.meta import UserSession
from decide_user.model.users import User
from decide_user.model.users import UserGroup
from repoze.what.adapters import BaseSourceAdapter

class SQLAlchemyGroupAdapter(BaseSourceAdapter):
    """
    Group source adapter based on example from
    http://what.repoze.org/docs/1.0/Manual/ManagingSources.html#sample-source-adapters
    """

    def __init__(self, * args, ** kwargs):
        super(SQLAlchemyGroupAdapter, self).__init__(*args, ** kwargs)

        self.sections = self.get_all_sections()

    def _get_all_sections(self):

        self.sections = {}

        for ug in UserSession.query(UserGroup).all():

            name = "%s-group" % ug.name.strip().lower()

            users = []
            for user in ug.users:
                users.append(user.email)

            self.sections[name] = set(users)

        # Close the database session
        UserSession.remove()
        
        return self.sections

    def _get_section_items(self, section):
        return self.sections[section]

    def _find_sections(self, credentials):
        username = credentials['repoze.what.userid']
        #return set([n for (n, g) in self.sections.items()
        #           if username in g])
        group = UserSession.query(UserGroup).join(User, UserGroup.id == User.fk_usergroup).filter(User.email == username).one()

        UserSession.remove()

        return set([u"%s-group" % group.name.strip().lower()])

    def _include_items(self, section, items):
        self.sections[section] |= items

    def _exclude_items(self, section, items):
        for item in items:
            self.sections[section].remove(item)

    def _item_is_included(self, section, item):
        return item in self.sections[section]

    def _create_section(self, section):
        self.sections[section] = set()

    def _edit_section(self, section, new_section):
        self._sections[new_section] = self.sections[section]
        del self.sections[section]

    def _delete_section(self, section):
        del self.sections[section]

    def _section_exists(self, section):
        return self.sections.has_key(section)