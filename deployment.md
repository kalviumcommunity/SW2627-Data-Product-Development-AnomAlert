# Deploy — AnomAlert Dashboard

## Run Locally
```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at http://localhost:8501. Requires `AnomAlert.sqlite` in the project root.

## Deploy (Streamlit Community Cloud — recommended, free)
1. Push repo to GitHub.
2. Go to share.streamlit.io → sign in with GitHub.
3. "New app" → select repo/branch → set main file to `app.py`.
4. Click Deploy. Auto-installs `requirements.txt`, gives you a public `.streamlit.app` URL.
5. Every push to the branch auto-redeploys.

**Note:** Streamlit Cloud's storage is ephemeral — fine for a read-only SQLite file, but any runtime writes won't persist across restarts.

## Alternative: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
```bash
docker build -t anomalert .
docker run -p 8501:8501 anomalert
```
Deploy the image to Render/Railway/Fly.io/etc.


## Known Limitations
- Filter bar: **Risk Band** and **Search User** actually filter the data. **User Role**, **Country**, and **Time Range** are UI-only for now — the dataset has no columns backing them yet.
- "Recent Authentication Events" shows the last N rows of the dataset as-is, not a true time-ordered feed, since there's no timestamp column yet.

## How to Test This PR
1. Follow "Run Locally" above.
2. Confirm all sections load with no errors: KPI cards, filter bar, Risk Distribution, Top 10 Risky Users, Recent Authentication Events, Risk Formula, User Investigation search.
3. Try the Risk Band filter and Search User box — confirm the tables below update accordingly.


## Checklist
- [ ] `requirements.txt` up to date
- [ ] App runs with no errors
- [ ] `.gitignore` excludes `venv/`, `__pycache__/`
- [ ] No hardcoded secrets
- [ ] `AnomAlert.sqlite` committed (if meant to ship with the app)