# GH Scheduler

A Flask-based web application for managing caregiver schedules and shifts using a file-based storage system.

> **Note:** This branch contains the migration from SQLite to JSON-based storage for improved portability and easier data management.

## Features

- Calendar view of weekly schedules
- Hourly view of shifts
- Caregiver management
- Shift assignment and removal
- Error handling and logging
- JSON-based data storage for easy portability

## Setup

1. Clone the repository:
```bash
git clone https://github.com/akhils0810/GHScheduler.git
cd GHScheduler
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Data Storage

The application uses a file-based storage system with JSON files:

- `data/caregivers.json`: Stores caregiver information
- `data/shifts.json`: Stores shift assignments and schedules

The data directory is automatically created when the application starts. You can backup your data by simply copying these JSON files.

## Deployment on Render

1. Create a new account on [Render](https://render.com) if you don't have one
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: `gh-scheduler` (or your preferred name)
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Add the following environment variables:
     - `FLASK_ENV=production`
     - `SECRET_KEY=your-secret-key-here`
     - `DATA_DIR=/data` (Optional: custom directory for JSON files)

5. Click "Create Web Service"

The application will be deployed and available at `https://your-app-name.onrender.com`

## Project Structure

- `app.py`: Main application file
- `models.py`: Data models and business logic
- `data_manager.py`: JSON file storage management
- `routes.py`: Route handlers
- `config.py`: Configuration settings
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS)
- `wsgi.py`: WSGI entry point for production
- `Procfile`: Process file for Render deployment
- `data/`: Directory containing JSON data files

## Data Migration

If you're migrating from the old SQLite version:

1. Ensure your old database (`schedule.db`) is in the root directory
2. Run the migration script:
```bash
python migrate_data.py
```

This will convert all your existing data to the new JSON format.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 