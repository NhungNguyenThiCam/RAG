from sqlalchemy import create_engine

connection_string = "postgresql+psycopg://Rag_user:Agents%40123@127.0.0.1:5432/ragdatabase"
engine = create_engine(connection_string)
try:
    with engine.connect() as conn:
        print("✅ SQLAlchemy connected successfully!")
except Exception as e:
    print("❌ SQLAlchemy connection failed:", e)