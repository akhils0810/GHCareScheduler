import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DataManager:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.caregivers_file = os.path.join(data_dir, 'caregivers.json')
        self.shifts_file = os.path.join(data_dir, 'shifts.json')
        self._ensure_data_directory()
        self._initialize_data_files()

    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _initialize_data_files(self):
        """Initialize data files if they don't exist."""
        if not os.path.exists(self.caregivers_file):
            self._save_caregivers([])
        if not os.path.exists(self.shifts_file):
            self._save_shifts([])

    def _load_caregivers(self) -> List[Dict]:
        """Load caregivers from file."""
        try:
            with open(self.caregivers_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading caregivers: {e}")
            return []

    def _save_caregivers(self, caregivers: List[Dict]):
        """Save caregivers to file."""
        try:
            with open(self.caregivers_file, 'w') as f:
                json.dump(caregivers, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving caregivers: {e}")
            raise

    def _load_shifts(self) -> List[Dict]:
        """Load shifts from file."""
        try:
            with open(self.shifts_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading shifts: {e}")
            return []

    def _save_shifts(self, shifts: List[Dict]):
        """Save shifts to file."""
        try:
            with open(self.shifts_file, 'w') as f:
                json.dump(shifts, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving shifts: {e}")
            raise

    def get_caregivers(self) -> List[Dict]:
        """Get all caregivers."""
        return self._load_caregivers()

    def get_caregiver(self, caregiver_id: int) -> Optional[Dict]:
        """Get a specific caregiver by ID."""
        caregivers = self._load_caregivers()
        for caregiver in caregivers:
            if caregiver['id'] == caregiver_id:
                return caregiver
        return None

    def get_shifts(self, start_date: datetime.date = None, end_date: datetime.date = None) -> List[Dict]:
        """Get shifts, optionally filtered by date range."""
        shifts = self._load_shifts()
        if start_date and end_date:
            return [
                shift for shift in shifts
                if start_date <= datetime.strptime(shift['date'], '%Y-%m-%d').date() < end_date
            ]
        return shifts

    def add_shift(self, shift_data: Dict) -> Dict:
        """Add a new shift."""
        shifts = self._load_shifts()
        shift_data['id'] = len(shifts) + 1
        shifts.append(shift_data)
        self._save_shifts(shifts)
        return shift_data

    def remove_shift(self, shift_id: int) -> bool:
        """Remove a shift by ID."""
        shifts = self._load_shifts()
        original_length = len(shifts)
        shifts = [shift for shift in shifts if shift['id'] != shift_id]
        if len(shifts) < original_length:
            self._save_shifts(shifts)
            return True
        return False

    def get_shifts_by_caregiver(self, caregiver_id: int, start_date: datetime.date = None, end_date: datetime.date = None) -> List[Dict]:
        """Get shifts for a specific caregiver."""
        shifts = self._load_shifts()
        filtered_shifts = [shift for shift in shifts if shift['caregiver_id'] == caregiver_id]
        if start_date and end_date:
            filtered_shifts = [
                shift for shift in filtered_shifts
                if start_date <= datetime.strptime(shift['date'], '%Y-%m-%d').date() < end_date
            ]
        return filtered_shifts

    def get_shifts_by_date(self, date: datetime.date) -> List[Dict]:
        """Get all shifts for a specific date."""
        shifts = self._load_shifts()
        return [
            shift for shift in shifts
            if datetime.strptime(shift['date'], '%Y-%m-%d').date() == date
        ]

    def get_shifts_by_type(self, shift_type: str, date: datetime.date) -> List[Dict]:
        """Get shifts of a specific type for a date."""
        shifts = self._load_shifts()
        return [
            shift for shift in shifts
            if shift['shift_type'] == shift_type
            and datetime.strptime(shift['date'], '%Y-%m-%d').date() == date
        ] 