if [ $2 = 'y' ] 
then
    coverage run --source=skelebot setup.py test && coverage report
else
    python setup.py test
fi
