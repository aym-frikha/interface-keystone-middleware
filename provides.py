#!/usr/bin/python
import json

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KeystoneMiddlewareProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:keystone-middleware}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')

    @hook('{provides:keystone-middleware}-relation-{broken, departed}')
    def broken(self):
        self.set_state('{relation_name}.departing')
        self.remove_state('{relation_name}.connected')

    def configure_principal(self, middleware_name, configuration):
        """Send principle keystone-middleware configuration"""
        conv = self.conversation()

        middleware_config = {
            "keystone": {
                "/etc/keystone/keystone.conf": {
                    "sections": configuration

                }
            }
        }
        conv.set_remote(middleware_name=middleware_name,
                        subordinate_configuration=json.dumps(middleware_config))
