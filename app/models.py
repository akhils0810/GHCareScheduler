from datetime import datetime
from .config import ShiftConfig
from .data_manager import DataManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Caregiver:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.shifts = []

    @classmethod
    def get_all(cls):
        data_manager = DataManager()
        caregivers_data = data_manager.get_caregivers()
        return [cls(**data) for data in caregivers_data]

    @classmethod
    def get_by_id(cls, caregiver_id: int):
        data_manager = DataManager()
        caregiver_data = data_manager.get_caregiver(caregiver_id)
        if caregiver_data:
            return cls(**caregiver_data)
        return None

class Shift:
    def __init__(self, id: int, date: str, shift_type: str, caregiver_id: int):
        self.id = id
        self.date = datetime.strptime(date, '%Y-%m-%d').date()
        self.shift_type = shift_type
        self.caregiver_id = caregiver_id
        self._caregiver = None

    @property
    def caregiver(self):
        if self._caregiver is None:
            self._caregiver = Caregiver.get_by_id(self.caregiver_id)
        return self._caregiver

    @property
    def time_range(self):
        return ShiftConfig.SHIFTS[self.shift_type]['time']
    
    @property
    def start_hour(self):
        return ShiftConfig.SHIFTS[self.shift_type]['start_hour']
    
    @property
    def duration_hours(self):
        return ShiftConfig.SHIFTS[self.shift_type]['duration']

    @classmethod
    def get_all(cls, start_date=None, end_date=None):
        data_manager = DataManager()
        shifts_data = data_manager.get_shifts(start_date, end_date)
        return [cls(**data) for data in shifts_data]

    @classmethod
    def get_by_caregiver(cls, caregiver_id: int, start_date=None, end_date=None):
        data_manager = DataManager()
        shifts_data = data_manager.get_shifts_by_caregiver(caregiver_id, start_date, end_date)
        return [cls(**data) for data in shifts_data]

    @classmethod
    def get_by_date(cls, date):
        data_manager = DataManager()
        shifts_data = data_manager.get_shifts_by_date(date)
        return [cls(**data) for data in shifts_data]

    @classmethod
    def get_by_type(cls, shift_type: str, date):
        data_manager = DataManager()
        shifts_data = data_manager.get_shifts_by_type(shift_type, date)
        return [cls(**data) for data in shifts_data]

    @classmethod
    def add(cls, date: str, shift_type: str, caregiver_id: int):
        data_manager = DataManager()
        shift_data = {
            'date': date,
            'shift_type': shift_type,
            'caregiver_id': caregiver_id
        }
        new_shift = data_manager.add_shift(shift_data)
        return cls(**new_shift)

    @classmethod
    def remove(cls, shift_id: int):
        data_manager = DataManager()
        return data_manager.remove_shift(shift_id)

def init_data():
    """Initialize the data store with default caregivers if none exist."""
    data_manager = DataManager()
    caregivers = data_manager.get_caregivers()
    
    if not caregivers:
        logger.info("No caregivers found. Initializing caregivers...")
        caregivers_data = []
        for i, name in enumerate(ShiftConfig.CAREGIVERS, 1):
            caregivers_data.append({
                'id': i,
                'name': name
            })
        data_manager._save_caregivers(caregivers_data)
        logger.info(f"Successfully initialized {len(caregivers_data)} caregivers")
    else:
        logger.info(f"Found {len(caregivers)} existing caregivers") 