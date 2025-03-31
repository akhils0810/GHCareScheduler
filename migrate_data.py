import os
import json
from datetime import datetime
from models import db, Caregiver, Shift
from data_manager import DataManager
from config import Config, ShiftConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_data():
    """Migrate data from SQLite database to JSON files."""
    try:
        # Initialize data manager
        data_manager = DataManager()
        
        # Migrate caregivers
        caregivers = Caregiver.query.all()
        caregivers_data = []
        for caregiver in caregivers:
            caregivers_data.append({
                'id': caregiver.id,
                'name': caregiver.name
            })
        data_manager._save_caregivers(caregivers_data)
        logger.info(f"Migrated {len(caregivers_data)} caregivers")
        
        # Migrate shifts
        shifts = Shift.query.all()
        shifts_data = []
        for shift in shifts:
            shifts_data.append({
                'id': shift.id,
                'date': shift.date.strftime('%Y-%m-%d'),
                'shift_type': shift.shift_type,
                'caregiver_id': shift.caregiver_id
            })
        data_manager._save_shifts(shifts_data)
        logger.info(f"Migrated {len(shifts_data)} shifts")
        
        logger.info("Data migration completed successfully")
        
    except Exception as e:
        logger.error(f"Error during data migration: {e}")
        raise

if __name__ == '__main__':
    migrate_data() 