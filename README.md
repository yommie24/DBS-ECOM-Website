# DBS-ECOM

## _An ecommerce platform

### Developers

- Yonatan Teklu
- Uriel Benitez
- Leah Cheong


### Project Structure

```md
• README.md                                             # You are here
• sprintdoc                                             # contains information about project sprints
• app
├── src
|   └── • prime.py                                      # contains the FastAPI app and event coroutines
|       ├── routers
|       |   ├── • main.py                               # contains the standard routes for the application
|       |   ├── • item.py                               # handles CRUD routes for items
|       |   └── • user.py                               # handles authentication and registration
|       ├── models
|       |   └── • datamodels.py                         # contains pydantic models for validation
|       ├── util
|       |   └── • utils.py                              # container any misc. utilities for reuse
|       └── tests                                       # contains testclient code
└──
```

## Installation

### Prepare a runtime environment

1. Install Python 3.10 or later
2. `git clone` this repo
3. Use `cd CSC-SWE-PrimeTime` to enter the local repo directory
4. Run `python -m venv venv` to create a virtual Python environment


### Get Required Dependencies

5. If not activated automatically, use `source venv/bin/activate` on Linux,
   `venv/scripts/activate.bat` on Windows CMD,
   or `venv/scripts/Activate.ps1` on Powershell for Windows
6. Run `python -m pip install -r requirements.txt` to get dependencies <br>
   (If your Python 3 binary isn't `python`, use what you have eg: for `py`, use `py -m pip ...`) <br>
   (If pip is installed to the system, leave off the call to Python)
   

### Configure

7. Copy `.env.example` to `.env`
8. Generate a secret using `openssl rand -hex 32`
9. Paste this secret next to the `OPENSSL_SECRET =` key and save the file


### Execute Uvicorn via the launcher

10. Run launch.py with `python launch.py`. 

*A production-ready execution method is planned for a later date*
