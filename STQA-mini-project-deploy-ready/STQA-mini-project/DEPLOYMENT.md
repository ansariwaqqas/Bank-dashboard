# Deploying the STQA Mini-Project

This project is a Python HTTP server that serves the dashboard, REST API, SQLite database, and STQA test lab from one web service.

## Recommended free demo deployment: Render

### 1. Prepare the source
1. Extract this ZIP on your computer.
2. Make sure the top level contains `render.yaml`, `requirements.txt`, `backend/`, `database/`, `frontend/`, and `docs/`.
3. Do not upload a local `.venv` folder or Python cache files.

### 2. Push the project to GitHub
Create a new repository at https://github.com/new. In a terminal opened in the extracted project folder, run:

```bash
git init
git add .
git commit -m "Prepare STQA mini project for deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own GitHub repository URL. GitHub may ask you to sign in.

### 3. Create the live service
1. Sign in at https://dashboard.render.com/.
2. Choose **New → Blueprint** and connect the GitHub repository containing this project.
3. Render will read `render.yaml`. Review the service and choose to apply/create it.
4. Open the service's **Events/Logs** page and wait for the deploy to report that it is live.
5. Open the service's `onrender.com` URL. The `/` page should show the banking dashboard.

The Blueprint config uses:
- Build command: `pip install -r requirements.txt`
- Start command: `python backend/app.py`
- Health check: `/api/stats`

The server reads the platform-provided `PORT`, so it can also be configured manually as a Render **Web Service** with those same build and start commands.

## Verify the live app
- Open the public dashboard.
- Check that the account list and statistics load.
- Create a throwaway demo account, then try a small deposit and withdrawal.
- Open the STQA Testing Lab and run the white-box, black-box, or combined tests. The expected local baseline is **8 passing tests**.

## Important demo limitations
- This is an educational simulation, not real banking software. Do not enter real personal, banking, or payment information.
- The free Render service uses an ephemeral filesystem. Account changes in the SQLite database can be lost after a restart, redeploy, or idle spin-down. The free service may also sleep when unused and take a little while to wake up. This is suitable for a college demo, not for data that needs to persist.
- A public demo has no user authentication. Treat all account names and balances as sample data.
