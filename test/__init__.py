test_requirements = [
    'pytest',
    'flake8',
    'coverage'
]
try:
    modules = map(__import__, test_requirements)
except ImportError as e:
    err_msg = e.message.replace("No module named ", "")
    msg = "%s is not installed. Install your test requirments." % err_msg
    raise ImportError(msg)
