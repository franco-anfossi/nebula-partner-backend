isort partner_backend/
flake8 partner_backend/
black partner_backend/
find partner_backend/ -name "*.py" -exec docformatter --in-place --wrap-summaries 88 --wrap-descriptions 88 {} +

isort posts/
flake8 posts/
black posts/
find posts/ -name "*.py" -exec docformatter --in-place --wrap-summaries 88 --wrap-descriptions 88 {} +

isort users/
flake8 users/
black users/
find users/ -name "*.py" -exec docformatter --in-place --wrap-summaries 88 --wrap-descriptions 88 {} +

isort manage.py
flake8 manage.py
black manage.py
find . -name "*.py" -exec docformatter --in-place --wrap-summaries 88 --wrap-descriptions 88 {} +

flake8 partner_backend/ posts/ users/ manage.py
