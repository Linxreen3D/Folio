"""Write the site's public backend configuration from environment variables.
The Supabase anon key is public by design; all access is enforced by the row level security rules in supabase/schema.sql.
usage: python3 -I write_config.py OUT_FILE
"""
import json, os, sys

cfg = {
    "supabaseUrl": os.environ.get("SUPABASE_URL", "").strip(),
    "supabaseKey": os.environ.get("SUPABASE_ANON_KEY", "").strip(),
    # "off" until a payment provider (Stripe Connect / Mangopay) is connected; then "stripe"
    "payments": os.environ.get("PAYMENTS", "").strip() or "off",
}
open(sys.argv[1], "w").write("window.FOLIO_CONFIG=" + json.dumps(cfg) + ";\n")
print("backend", "configured" if cfg["supabaseUrl"] and cfg["supabaseKey"] else "not configured (preview mode)", "payments", cfg["payments"])
