import os
import json
import sqlite3
from datetime import datetime
from app.data_manager import DataManager
from app.config import Config, ShiftConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_data():
    """Migrate data from SQLite database to JSON files."""
    try:
        # Initialize data manager
        data_manager = DataManager()
        
        # Connect to SQLite database
        db_path = os.path.join('Instance', 'schedule.db')
        if not os.path.exists(db_path):
            logger.warning("No SQLite database found to migrate from")
            return
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Migrate caregivers
        cursor.execute("SELECT id, name FROM caregiver")
        caregivers = cursor.fetchall()
        caregivers_data = []
        for caregiver_id, name in caregivers:
            caregivers_data.append({
                'id': caregiver_id,
                'name': name
            })
        data_manager._save_caregivers(caregivers_data)
        logger.info(f"Migrated {len(caregivers_data)} caregivers")
        
        # Migrate shifts
        cursor.execute("SELECT id, date, shift_type, caregiver_id FROM shift")
        shifts = cursor.fetchall()
        shifts_data = []
        for shift_id, date, shift_type, caregiver_id in shifts:
            shifts_data.append({
                'id': shift_id,
                'date': datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d'),
                'shift_type': shift_type,
                'caregiver_id': caregiver_id
            })
        data_manager._save_shifts(shifts_data)
        logger.info(f"Migrated {len(shifts_data)} shifts")
        
        conn.close()
        logger.info("Data migration completed successfully")
        
        # Remove the old database file
        try:
            os.remove(db_path)
            logger.info("Removed old SQLite database")
        except Exception as e:
            logger.warning(f"Could not remove old database: {e}")
        
    except Exception as e:
        logger.error(f"Error during data migration: {e}")
        raise

if __name__ == '__main__':
    migrate_data() 