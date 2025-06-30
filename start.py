#!/usr/bin/env python
"""
OpenLens Application Launcher
Simple entry point to start the full application
"""

import os
import sys
from pathlib import Path

# Add the scripts directory to the path
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

# Import and run the main launcher
try:
    from start_openlens_full import main
    main()
except ImportError as e:
    print(f"❌ Failed to import launcher: {e}")
    print("Make sure you're running from the openlens-app directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting OpenLens: {e}")
    sys.exit(1)
