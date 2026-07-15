"""
Run this locally (python test_connection.py) to see the REAL error
that Streamlit Cloud is hiding/redacting.
"""
import psycopg2

try:
    conn = psycopg2.connect(
        host='dpg-d9bhnm7aqgkc739e2fc0-a.singapore-postgres.render.com',
        user="phonepe_azst_user",
        password='cqDPwTuKyebyTKZsDk2wof1y37ngovSK',
        database='phonepe_azst',
        connect_timeout=10,
    )
    print("✅ Connection successful")

    cur = conn.cursor()

    # List all tables that actually exist in the public schema
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = [r[0] for r in cur.fetchall()]
    print("📋 Tables found:", tables)

    if "top_transaction" in tables:
        cur.execute('SELECT * FROM top_transaction LIMIT 3;')
        cols = [desc[0] for desc in cur.description]
        print("📊 Columns in top_transaction:", cols)
        print("Sample rows:", cur.fetchall())
    else:
        print("⚠️ 'top_transaction' table not found. Check the exact name/case above.")

    cur.close()
    conn.close()

except Exception as e:
    print("❌ REAL ERROR:", type(e).__name__, "-", e)
