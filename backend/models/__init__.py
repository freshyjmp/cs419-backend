"""
Treating models as a subpackage of our backend package.

Allows for import style like 

```
from backend.models import Modelname
```

"""
from backend.models.request import Request
from backend.models.edge import Edge
