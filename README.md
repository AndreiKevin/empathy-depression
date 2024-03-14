## Description
This is a simple depression recommendation system with a NextJS React frontend and a Django Python backend. It uses Aceternity components, Shadcn components, and Tailwind CSS for the UI. 

The trained models are in the `models` folder. The frontend is in the `my-app` folder and the backend is in the `root` and `example` folder. 

## How to Run locally
1. Django Frontend Setup: From the `root` directory, create a venv and install the requirements
```bash
# Windows:
py -m venv myworld

# Unix/MacOS:
python -m venv myworld
```

2. Django Frontend Setup: Activate the venv 
```bash
source .venv/bin/activate 
```

3. Django Frontend Setup: Install the requirements
```bash
pip install -r requirements.txt
```

4. Django Frontend Setup: Run the server
```bash
python manage.py runserver
```
Note: Make sure the Django server runs on http://127.0.0.1:8000/

5. NextJS Frontend Setup: Change directory to the frontend
```bash
cd my-app
```

6. NextJS Frontend Setup: Install the dependencies
```bash
npm install
```

7. NextJS Frontend Setup: Run the server
```bash
npm run dev
```