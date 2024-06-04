pip install .[dev]
if [ "--coverage" = "$1" ]
then
    coverage run --source=skelebot -m pytest && coverage report -m
else
    pytest .
fi
