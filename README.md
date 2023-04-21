SeaSnake
--------

SeaSnake is a user-friendly Python wrapper that enables seamless interaction with MERMAID (Marine Ecological Research Management Aid) platform. It allows researchers, data scientists, and marine enthusiasts to access, analyze, and manage their marine ecosystem data directly through Python scripts or Jupyter Notebooks.


# Install

`pip install -u py-seasnake`


# Quick Start

```
from seasnake import auth
from seasnake.auth import MermaidAuth
from seasnake.summaries import FishBelt

auth = MermaidAuth()
token = auth.request_token()

project_id = "<YOUR PROJECT ID>"
fb = FishBelt(token=token)
df_obs = fb.observations(project_id)

print(df_obs)

```

## Testing

`poetry run pytest --ruff --mypy tests/`
