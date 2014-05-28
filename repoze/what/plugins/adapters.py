__author__ = "Adrian Weber, Centre for Development and Environment, University of Bern"
__date__ = "$Dec 12, 2012 3:52:32 PM$"

from decide_user.model.meta import UserSession
from decide_user.model.users import User
from decide_user.model.users import UserGroup
from decide_user.model.users import Role
from repoze.what.adapters import BaseSourceAdapter

class SQLAlchemyGroupAdapter(BaseSourceAdapter):
    """
    Group source adapter based on example from
    http://what.repoze.org/docs/1.0/Manual/ManagingSources.html#sample-source-adapters
    """

    def __init__(self, * args, ** kwargs):
        super(SQLAlchemyGroupAdapter, self).__init__(*args, ** kwargs)
        
        self.is_writable = False

        self.sections = self.get_all_sections()

    def _get_all_sections(self):
        """
        Get all sections i.e. groups with corresponding users in the following
        form:
        
        {u'gol': set([u'user_5577@hotmail.com']),
        u'ingo': set([u'useremail@gmail.com']),
        u'cde': set([u'firstname.lastname@cde.unibe.ch']),
        u'registered': set([u'hotmailuser@hotmail.com', u'first.last@gmail.com']),
        u'mpi': set([u'soupi_2004@yahoo.com', u'user2@yahoo.com']),
        u'fullaccess': set([u'anotheruser@gmail.com', u'admin@cde.unibe.ch'])
        }
        
        This method is only called when the server is restarted!
        
        """
        
        sections = {}

        for ug in UserSession.query(UserGroup).all():

            name = "%s" % ug.name.strip().lower()

            users = []
            for user in ug.users:
                users.append(user.email)

            sections[name] = set(users)

        # Close the database session
        UserSession.remove()
        
        return sections

    def _get_section_items(self, section):
        """
        Untested! Since I'm not sure when and whether this method is called in Pylons.
        """

        usergroup = UserSession.query(UserGroup).filter(UserGroup.name == section).first()
        users = usergroup.users

        # Close the database session
        UserSession.remove()
        
        return set([unicode(user.email) for user in users])

    def _find_sections(self, credentials):
        """
        This method return the list of groups the current user belongs to in the
        following form:
        
        set([u'cde', u'ingo'])

        It is called with every Pylons request.

        """
        
        # Get the username from the credentials
        username = credentials['repoze.what.userid']
        
        # Query all groups an user belongs to
        user = UserSession.query(User).filter(User.email == username).first()
        groups = user.groups

        # Close the session
        UserSession.remove()
        
        return set([unicode(g.name.strip().lower()) for g in groups])

    def _include_items(self, section, items):
        raise NotImplementedError("SQLAlchemyGroupAdapter._include_items is not implemented.")

    def _exclude_items(self, section, items):
        raise NotImplementedError("SQLAlchemyGroupAdapter._exclude_items is not implemented.")

    def _item_is_included(self, section, item):
        raise NotImplementedError("SQLAlchemyGroupAdapter._item_is_included is not implemented.")

    def _create_section(self, section):
        raise NotImplementedError("SQLAlchemyGroupAdapter._create_section is not implemented.")

    def _edit_section(self, section, new_section):
        raise NotImplementedError("SQLAlchemyGroupAdapter._edit_section is not implemented.")

    def _delete_section(self, section):
        raise NotImplementedError("SQLAlchemyGroupAdapter._delete_section is not implemented.")

    def _section_exists(self, section):
        raise NotImplementedError("SQLAlchemyGroupAdapter._section_exists is not implemented.")
    
class SQLAlchemyPermissionAdapter(BaseSourceAdapter):
    """
    A source adapter to an existing SQLAlchemy model
    """

    def __init__(self, *args, **kwargs):
        super(SQLAlchemyPermissionAdapter, self).__init__(*args, **kwargs)
        
        self.is_writable = False
 
        self.sections = self.get_all_sections()

    def _get_all_sections(self):
        """
        Get all groups per privileges (aka permissions) in the following form:
        
        sections = {
            u'gol_view': set([u'gol', u'fullaccess', u'mpi']),
            u'public_view': set([u'gol', u'registered', u'fullaccess', u'ingo', u'mpi']),
            u'mpi_view': set([u'fullaccess', u'mpi']),
            u'cde_view': set([u'cde']),
            u'maf_view': set([u'fullaccess']),
            u'fullaccess_view': set([u'fullaccess']),
            u'ingo_view': set([u'gol', u'fullaccess', u'ingo', u'mpi'])
        }

        This method is only called on server startup!
        """
        
        sections = {}
        
        for r in UserSession.query(Role).all():
            sections[unicode(r.name)] = set(unicode(g.name) for g in r.groups)

        # Close the database session
        UserSession.remove()
        
        return sections

    def _get_section_items(self, section):
        raise NotImplementedError("SQLAlchemyPermissionAdapter.get_sections_items is not implemented.")

    def _find_sections(self, group_name):
        """
        Returns a list of all privileges for the requested group name in the 
        following form:
        
        privileges = set([u'view', u'edit', u'translate', u'administer'])
        
        It is called with every Pylons request.
        
        """
                    
        group = UserSession.query(UserGroup).filter(UserGroup.name == group_name).one()
        
        privileges = set([unicode(r.name) for r in group.roles])
        
        return privileges

    def _include_items(self, section, items):
        raise NotImplementedError("SQLAlchemyPermissionAdapter._include_items is not implemented.")

    def _exclude_items(self, section, items):
        raise NotImplementedError("SQLAlchemyPermissionAdapter._exclude_items is not implemented.")

    def _item_is_included(self, section, item):
        raise NotImplementedError("SQLAlchemyPermissionAdapter._item_is_included is not implemented.")

    def _create_section(self, section):
        raise NotImplementedError("SQLAlchemyPermissionAdapter._create_section is not implemented.")

    def _edit_section(self, section, new_section):
        raise NotImplementedError("SQLAlchemyPermissionAdapter._edit_section is not implemented.")

    def _delete_section(self, section):
        raise NotImplementedError("SQLAlchemyPermissionAdapter._delete_section is not implemented.")

    def _section_exists(self, section):
        raise NotImplementedError("SQLAlchemyPermissionAdapter._section_exists is not implemented.")