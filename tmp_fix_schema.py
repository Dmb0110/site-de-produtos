import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
url = os.getenv('DATABASE_URL', '').strip()
if not url:
    raise SystemExit('DATABASE_URL is not configured')
print('Using DATABASE_URL:', url)
engine = create_engine(url)
with engine.connect() as conn:
    conn.execute(text('ALTER TABLE produtos ADD COLUMN IF NOT EXISTS foto_id VARCHAR(24);'))
    conn.commit()
    print('Ensured foto_id column exists on produtos')
