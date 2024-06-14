isort partner_backend/
flake8 partner_backend/
black partner_backend/

isort posts/
flake8 posts/
black posts/

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place users/
isort users/
flake8 users/
black users/
docformatter --in-place --wrap-summaries 88 --wrap-descriptions 88 users/

isort manage.py
flake8 manage.py
black manage.py