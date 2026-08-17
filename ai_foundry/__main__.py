"""允许 `python -m ai_foundry` 直接运行。"""

from .cli import main

raise SystemExit(main())
