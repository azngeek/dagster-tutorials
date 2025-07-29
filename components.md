# About

What are [components](https://docs.dagster.io/guides/build/components) in Dagster? I had some difficulties understanding the idea and concepts behind Dagster components - it is also a very new addition. Of course, you get the it if you start working with it and carefully read the documentation but let me try to explain it with my words.

Dagster components are an alternative way to create reusable elements like assets, asset checks, schedules, sensors, jobs, resources, and more. And to be very exact, Dagster components are a way to create isolated components that will return a `Dagster Definitions` object. Inspect this [class](https://github.com/dagster-io/dagster/blob/e5f6d24e58a6e731ea351a09e842bbf9e20aa6a4/python_modules/dagster/dagster/_core/definitions/definitions_class.py#L329) to see and understand what is possible.

Still not there? Let me give you an example. Usually you will not use components until you are in a more advanced stage of using Dagster. Because you read a blog post about it or just because you wanted to improve the quality of life of your dear colleagues.

This is how the definition of a typical Dagster definition object looks. There is a very high chance it will look like this. You might have more or less. :)

```
# /definitions.py

defs = Definitions(
   assets=assets,
   schedules=schedules,
  resources={
    'my_service': MyService(api_key='donttellme')
  }
)
```

Now let me pick up any part of the definitions to explain the concept of `Dagster Components`. It could be anything because you can make a component out of it, if it returns a `Dagster Definition`. I choose resources. The official documentation makes some assumptions upfront you should know, when you need to convert your project layout to a Dagster Component compatible layout. If you want this question to be answered: It is still to early, but I will point it out. For now, we will continue with the class definition of this service, how it would look like. 

```
# /resources/my_service

import dagster as dg

class MyService(dg.ConfigurableResource):
  api_key: str = Field(..., description="Secret API Key")

```

This is indeed a simple class which only requires an attribute `api_key` to be initialized. So exactly like this `... 'my_service': MyService(api_key='donttellme') ...`. This also means:

- The service needs to be initialized in the `definitions.py` file
- The service requires configuration
- The definition needs to be extended

What if there would be an option to not edit the `definitions.py` file at all and provide a mechanismn which gives you the possibility to use a declarative approach to define your resource? Before you answer this question, ask yourself if you need this. There is nothing wrong about editing the definitions file and also maybe there is no big advantage as well except having a more modular approach to structure your project. But back to the answer: There is an approach and it is achieved by the following terms:

- Any entity which can return a `Dagster definition object` can also be modeled as a `component`.
- Any component can be configured via a humand readable configuration file in `yaml`.
- The configuration files need to be read, initialized and the loaded entities appended to the main definitions configuration.

I hope you see, where this is going. I will continue with the official [migration guide](https://docs.dagster.io/guides/build/projects/moving-to-components/migrating-project) for existing projects. This is what the official documentation shows. I adapted it to our needs.

```
.
├── my_existing_project
│   ├── __init__.py
│   ├── assets.py
│   ├── definitions.py
│   ├── resources
│   │    └── my_service.py
│   └── py.typed
├── pyproject.toml
└── uv.lock
```

But let me show you, what we actually want to have. 

- There is a new directory `defs` which will contain a configurable definition for each resource.
- The components are also placed in a new directory called `components`.


```
.
├── my_existing_project
│   ├── __init__.py
│   ├── assets.py
│   ├── definitions.py
│   ├── components
│   │    └── my_service_component.py
│   ├── defs // This is important
│   │    └── my_client
│   │       └── defs.yaml
│   └── py.typed
├── pyproject.toml
└── uv.lock
```

So to get the functionality to automatically register the components with the definition, we need to change the way, how definitions are loaded. As our plan is to migrate/refactor the service to a component and autoload it, we can use the `Definitions.merge` method to do it.

```
defs = dg.Definitions.merge(
    dg.Definitions(
        assets=assets,
        schedules=schedules,
        # resources={
        #  'my_service': MyService(api_key='donttellme')
        # }
    ),
    dg.components.load_from_defs_folder(project_root=Path(__file__).parent.parent),
)
```

## Whats next?

Curious about what comes next? I will continue with this tutorial to just complete it, but in the meanwhile let me know if this was helpful so far :) 
