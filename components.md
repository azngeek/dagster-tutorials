# The code

Checkout my repository to follow my examples.

- `git clone git@github.com:azngeek/dagster-tutorials.git` (only once)
- `cd components`
- `uv sync`
- `dagster dev` or `dg dev` if you use the CLI.

# About

What are [components](https://docs.dagster.io/guides/build/components) in Dagster? I had some difficulties understanding the idea and concepts behind Dagster components - it is also a very new addition. Of course, you get the it if you start working with it and carefully read the documentation but let me try to explain it with my words.

Dagster components are an alternative way to create reusable elements like assets, asset checks, schedules, sensors, jobs, resources, and more. And to be very exact, Dagster components are a way to create isolated components that will return a `Dagster Definitions` object. Inspect this [class](https://github.com/dagster-io/dagster/blob/e5f6d24e58a6e731ea351a09e842bbf9e20aa6a4/python_modules/dagster/dagster/_core/definitions/definitions_class.py#L329) to see and understand what is possible.

# Overview about relevant directories

There might be some more files but what we are looking at, is what we will focus on.

- `pyproject.yaml`: Contains the `tool.dg.project` entry, which is required, that components will be loaded.
- `legacy`: I provided some examples, how legacy Dagster projects would be structured. This is essential if you plan to migrate and something I struggled in the beginning, when learning about `Dagster components`.
- `test`: You will find some test strategies with `Dagster components`. Not all examples will be discussed in this article. Feel free to explore some ideas.

```
tree -L 4

.
├── pyproject.toml
├── src
│   ├── my_project
│   │   ├── definitions.py
│   │   └── defs
│   │       └── __init__.py
│   └── legacy
│       ├── assets
│       │   └── assets.py
│       └── resources
│           └── my_legacy_api_client.py
├── tests
│   └── __init__.py
└── uv.lock

```

# The role of the definitions object

Open the `./my_project/definitions.py` file.

This is how the definition of a typical Dagster definition object looks. 
There is a very high chance it will look like this if you worked with a Dagster version older then `1.10`. Of course this example is simplified
but it contains all parts which are required to explain the concepts of the definitions object.

The definitions are essential for Dagster as it is the only way to know about all `assets`, `resources`, `schedules` etc. Again, check this [original code](https://github.com/dagster-io/dagster/blob/e5f6d24e58a6e731ea351a09e842bbf9e20aa6a4/python_modules/dagster/dagster/_core/definitions/definitions_class.py#L329) to see and understand what can be registered.

```
# ./my_project/definitions.py

defs = dg.Definitions(
    assets=dg.load_assets_from_modules([assets]),
    resources={
        'my_legacy_api_client': MyLegacyApiClient(api_key='donttellme')
    }
)
```

In case you want to add for example a `schedule` or a `sensor`, you would extend it in the configuration.

```
# ./my_project/definitions.py

defs = dg.Definitions(
    assets=dg.load_assets_from_modules([assets]),
    schedules=[my_schedule],
    sensors=[my_sensor],
    resources={
        'my_legacy_api_client': MyLegacyApiClient(api_key='donttellme')
    }
)
```

So, adding new features to your project means, you need to extend the configuration of this object. Here comes one central idea of
`components`: You might not want to do it manually but just configure your component and delegate the registering and loading of your 
features like `assets` or `resources` to dagster.

Run the following command to see all definitions: `dg list defs`. Your result will contain additional assets and resources but this is how it will look like if you
don't use any autoloaded resources.

```
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Section   ┃ Definitions                                                                                                       ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Assets    │ ┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│           │ ┃ Key       ┃ Group   ┃ Deps ┃ Kinds ┃ Description                                                              ┃ │
│           │ ┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│           │ │ old_asset │ default │      │       │ This is an example, how assets looked in the past. So prior Dagster 1.10 │ │
│           │ │           │         │      │       │ Assets would not be autoloa…                                             │ │
│           │ └───────────┴─────────┴──────┴───────┴──────────────────────────────────────────────────────────────────────────┘ │
│ Resources │ ┏━━━━━━━━━━━━━━━━━━━━━━┓                                                                                          │
│           │ ┃ Key                  ┃                                                                                          │
│           │ ┡━━━━━━━━━━━━━━━━━━━━━━┩                                                                                          │
│           │ │ my_legacy_api_client │                                                                                          │
│           │ └──────────────────────┘                                                                                          │
└───────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

# The autoloader

If you create a new project, the definitions will look exactly like this. There are some smaller improvements like the decorator `dg.definitions`
but most important, it only uses the method to load all definitions from a certain directory.

```
# ./my_project/definitions.py

@dg.definitions
def defs():
    return dg.load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)
```

The documentation tells us

```
...
It reads the project configuration (dg.toml or pyproject.toml), identifies
the defs module, and recursively loads all components, assets, jobs, and other Dagster
definitions from the project structure.
...
```

In our case it will look for any definitions in the directory `my_project/defs`. And if you have any function which can be loaded by Dagster
like the `daily_sales` asset in `./my_projects/defs/assets.py`, this will be available.

Run `dg list defs` again, and we will see the assets. Keep in mind that there was no need to register this asset automatically.


```
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Section ┃ Definitions                                            ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Assets  │ ┏━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┓ │
│         │ ┃ Key         ┃ Group   ┃ Deps ┃ Kinds ┃ Description ┃ │
│         │ ┡━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━┩ │
│         │ │ daily_sales │ default │      │       │             │ │
│         │ └─────────────┴─────────┴──────┴───────┴─────────────┘ │
└─────────┴────────────────────────────────────────────────────────┘
```

But what, if you want to use your existing project structure but with the autoloader? Well, you can. Use `dg.Definitions.merge` to get the
best of both worlds. Also feel free to add new `assets` and see, how the autoloader works.

```
@dg.definitions
def defs():
    return (
        dg.Definitions.merge(
            dg.Definitions(
                assets=dg.load_assets_from_modules([assets]),
                resources={
                    'my_legacy_api_client': MyLegacyApiClient(api_key='donttellme')
                }
            ),
            dg.load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)
        )
    )
```

# Are we already using components and what are they used for?

Short answer: No. In this stage no component is actually used. Only the autoloading feature is used and there is an opiniated project structure. To use components
we need to understand the benefits of using them.

Components are a very convenient way to develop reusable `assets`, `resources` and anything then can be registered via the definitions object once and then just
configure them with yaml-files.

Let's inspect the existing resource `MyLegacyApiClient` and how it would be registered in a component-only-setup. A resource like this requires two steps until it can be used
for example in assets.


```
# ./legacy/resources/my_legacy_api_client.py

class MyLegacyApiClient(dg.ConfigurableResource):

    api_key: str = Field(..., description="Secret API Key")

    def __init__(self, **data: Any):
        super().__init__(**data)
```

- You need to provide the api_key
- You need to register the resource in the definitions file with a specific unique key

```
# ./my_project/definitions.py

...
resources={
    'my_legacy_api_client': MyLegacyApiClient(api_key='donttellme')
}
...
```

Now remember, how the definitions-file would look like, if you would not register this service manually but depend on the autoloader. Where can you configure the api key
and how can I ensure that the resource will be available with the key `my_legacy_api_client`? We could of course merge the definitions with a manually registered client like
you will see in the definitions file.

```
# ./my_project/definitions.py

@dg.definitions
def defs():
    return dg.load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)
```

Well, here is the alternative approach with a component structure where the api_client will be initialized in the component. Take a look at which files were added. 
Actually this structure has not been created manually but is the result of a scaffolding command, which I will go through later.


- There is a `defs/my_api_client/defs.yaml` file.
- There is a `my_project/components/my_api_client_component.py` file

```
.
├── pyproject.toml
├── src
│   ├── legacy
│   │   └── resources
│   │       └── my_legacy_api_client.py
│   └── my_project
│       ├── components
│       │   └── my_api_client_component.py
│       └── defs
│           └── my_api_client
│               └── defs.yaml # This is where the api client is registered as a component


```

And here is the sneak-peak for the yaml-file

```
type: my_project.components.my_api_client_component.MyApiClientComponent 

attributes:
  api_key: "test"

```

# Refactor the simple service

We will pick the existing legacy service and wrap it into a component. Dagster comes with some useful helper commands to quickly
create new components.

Run `dg scaffold component MyApiClientComponent` to create a skeleton class. A new component named `my_api_client_component.py`will
be created in the `./my_project/components` directory. 

Now run `dg list components` to see that it exists as `my_project.components.my_api_client_component.MyApiClientComponent` in the list of all
registered components.

And it will have this structure. Notice that the component returns an empty
definitions object, so if you run `dg list defs`, there would be no new entry in the registered resources.

```
class MyApiClientComponent(dg.Component, dg.Model, dg.Resolvable):
    """COMPONENT SUMMARY HERE.

    COMPONENT DESCRIPTION HERE.
    """

    # added fields here will define params when instantiated in Python, and yaml schema via Resolvable

    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        # Add definition construction logic here.
        return dg.Definitions()

```

We will modifiy the `dg.Definitions()` part to wrap the existing client into the component. 

```
def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
    # Add definition construction logic here.
    return dg.Definitions(
        resources={
            'my_new_strapi_client': MyLegacyApiClient(api_key='test')
        }
    )
```

And finally run this  to let dagster create a configuration file named `./my_project/defs/my_api_client/defs.yaml`.
```
dg scaffold defs my_project.components.my_api_client_component.MyApiClientComponent my_api_client
```

This is mandatory as this file be used to automatically load the resources. I also want to check, that this is  the case, so we will double check it.

```
dg list defs

...

│ Resources │ ┏━━━━━━━━━━━━━━━━━━━━━━┓                                                                                            
│           │ ┃ Key                  ┃                                                                                         
│           │ ┡━━━━━━━━━━━━━━━━━━━━━━┩                                                                                       
│           │ │ my_legacy_api_client │                                                                                  
│           │ ├──────────────────────┤
│           │ │ my_new_strapi_client │
│           │ └──────────────────────┘ 
...
```

To recap what we did:

- We wrote a component wrapper for the legacy service
- The wrapper will return a definition object which will be loaded via the method `dg.load_from_defs_folder()`
- The scaffold command `dg scaffold defs` was used to automatically create a blueprint yaml file

At this point you might want to get rid of the manually registered Client assigned to the key `my_legacy_api_client`. Just remove or uncomment it.

```
@dg.definitions
def defs():
    return (
        dg.Definitions.merge(
            dg.Definitions(
                assets=dg.load_assets_from_modules([assets]),
                # resources={
                #     'my_legacy_api_client': MyLegacyApiClient(api_key='donttellme')
                # }
            ),
            dg.load_from_defs_folder(project_root=Path(__file__).parent.parent.parent)
        )
    )

```

# Make it configurable

A yaml file has been created but execpt that it is used to register the component, we still have hardcoded values. What we have:

```
./my_project/components/my_api_client_component.py

...
resources={
    'my_new_strapi_client': MyLegacyApiClient(api_key='test')
}
```

What we want is to pass the api key from the yaml configuration, so that it can be automatically resolved.
```
./my_project/components/my_api_client_component.py

@dg.scaffold_with(MyApiClientScaffolder)
class MyApiClientComponent(dg.Component, dg.Model, dg.Resolvable):

    api_key: str
    
    def build_defs(self, context: dg.ComponentLoadContext) -> dg.Definitions:
        # Add definition construction logic here.
        return dg.Definitions(
            resources={
                'my_new_strapi_client': MyLegacyApiClient(api_key=self.api_key)
            }
        )
```

And to make it a little bit more fancy, add a custom scaffolder, which will create the required yaml configuration.

```
./my_project/components/my_api_client_component.py

class MyApiClientScaffolder(dg.Scaffolder):
    """Scaffolds a template shell script alongside a filled-out defs.yaml file."""

    def scaffold(self, request: dg.ScaffoldRequest) -> None:
        dg.scaffold_component(
            request,
            {
                "api_key": "<your_api_key>"
            },
        )

@dg.scaffold_with(MyApiClientScaffolder)
class MyApiClientComponent(dg.Component, dg.Model, dg.Resolvable):
```

Now with everything in place, run this command again. Make sure an existing definition does not exists and see how dagster
creates a pre-configured yaml file for you.

```
dg scaffold defs my_project.components.my_api_client_component.MyApiClientComponent my_api_client
```

Congratulations, you now have a fully working component, which is configurable and autoloaded. In the next chapter we will check some testing strategies for components.

# Testing

TBD