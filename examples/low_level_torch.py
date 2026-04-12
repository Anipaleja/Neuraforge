"""Optional example for raw torch usage.

Install torch manually if you want to run this script.
"""

try:
    import torch
    import torch.nn as nn
except ImportError:
    raise SystemExit("Install torch first: pip install torch")

layer = nn.Linear(4, 2)
x = torch.randn(1, 4)
print(layer(x))
