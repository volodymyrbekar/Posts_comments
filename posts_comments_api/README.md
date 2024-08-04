# Post Comments API

## APi

API for CRUD operations on posts and comments.
JWT authentication is used for user authentication.
Gemini AI is used for toxic words detection and blocking.
Auto replay for comment is implemented using Gemini as well.

Preconditions 
* python 3
* virtualenv
* pip
* etc.


## Installation

```bash
git clone <github>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py runserver


Link for docs: http://localhost:8000/api/docs#/
