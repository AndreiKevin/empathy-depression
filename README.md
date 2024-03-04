## Description
Note that pushing to the main branch will automatically deploy the changes to the vercel server.
Make branches for features first. Go to branch feature/front-end first.
Website can be accessed here: https://empathy-depression.vercel.app/

## How to Run locally
1. Create a venv and install the requirements
```bash
# Windows:
py -m venv myworld

# Unix/MacOS:
python -m venv myworld
```
2. Activate the venv 
```bash
source .venv/bin/activate 
```

3. Run the server
```bash
python manage.py runserver
