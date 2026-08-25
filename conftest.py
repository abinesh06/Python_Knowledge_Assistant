# This file is intentionally empty.
#
# pytest always imports conftest.py automatically, and the moment it does,
# it adds this file's directory (the project root) to sys.path.
# That's what lets tests/test_text_utils.py do:
#     from pka.text_utils import extract_hashtags
# without needing an __init__.py in tests/ or any -m tricks.
#
# This file will start earning its keep on Day 2, when we add shared
# @pytest.fixture definitions here (sample notes, temp files, etc.)
# so every test file can reuse them without copy-pasting setup code.
