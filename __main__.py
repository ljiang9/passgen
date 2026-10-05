"""Enables `python -m passgen`."""
if __package__:
    from .passgen import main
else:
    from passgen import main
import sys
sys.exit(main())
