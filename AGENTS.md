# Cloud and Supabase work

Before using Supabase in a cloud task, read [start/SKILL.md](start/SKILL.md).
Use the tracked `tools/supabase_mcp.py` client and injected environment variables.
Never store or print tokens or session IDs. Do not infer missing schema from an
empty migration history; audit the actual catalog before preparing new migrations.
