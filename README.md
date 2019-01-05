# Overview

This interface provides information about a middleware for keystone openstack service.

# Usage

This interface layer will set the following state:

  * `{relation_name}.connected` The relation is established, but the charm may
    not have provided any middleware information.

For example, the subordinate would handle the `keystone-middleware.connected` state
with something like:

```python
@reactive.when('keystone-middleware.connected')
def configure_keystone_middleware(principle):
    with provide_charm_instance() as charm_class:
        middleware_configuration = {
            "authentication": {
                "simple_token_header": "SimpleToken",
                "simple_token_secret": charm_class.get_ico_token()
            },
            "auth": {
                "methods": "external,password,token,oauth1",
                "external": "keystone.auth.plugins.external.Domain",
                "password": "keystone.auth.plugins.password.Password",
                "token": "keystone.auth.plugins.token.Token",
                "oauth1": "keystone.auth.plugins.oauth1.OAuth"
            }
        }
        principle.configure_principal(
            middleware_name=charm_class.service_name,
            configuration=middleware_configuration)
    reactive.set_state('ico.configured')
```

# metadata

To consume this interface in your charm or layer, add the following to `layer.yaml`:

```yaml
includes: ['interface:keystone-middleware']
```

and add a provides interface of type `keystone-middleware` to your charm or layers `metadata.yaml`:

```yaml
provides:
  keystone-middleware:
    interface: keystone-middleware
    scope: container
```

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/openstack-charms/+filebug).

For development questions please refer to the OpenStack [Charm Guide](https://github.com/openstack/charm-guide).