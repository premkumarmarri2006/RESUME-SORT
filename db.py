"""
Local JSON history storage. No Firebase, no credentials needed.
"""
import os
import json
from datetime import datetime
from typing import List, Dict
 
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_history.json")
 
 
class HistoryDB:
    def __init__(self):
        self._ensure()
        print(f"✅ History file: {HISTORY_FILE}")
 
    def _ensure(self):
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w") as f:
                json.dump([], f)
 
    def save_search(self, job_description: str, candidate_count: int, top_candidate: str):
        record = {
            "id": str(int(datetime.now().timestamp())),
            "timestamp": datetime.now().isoformat(),
            "job_description_snippet": job_description[:100] + ("..." if len(job_description) > 100 else ""),
            "candidate_count": candidate_count,
            "top_candidate": top_candidate,
        }
        try:
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
            data.insert(0, record)
            with open(HISTORY_FILE, "w") as f:
                json.dump(data[:20], f, indent=2)
        except Exception as e:
            print(f"History save error: {e}")
 
    def get_recent_searches(self) -> List[Dict]:
        try:
            self._ensure()
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)[:20]
        except Exception as e:
            print(f"History load error: {e}")
            return []
 
 
db_client = HistoryDB()