// Public Supabase project URL and publishable/anon key only. Never use a secret/service_role key.
window.THINK_CP_CONFIG = {
  supabaseUrl: 'https://njedykefqzlkomhuywcv.supabase.co',
  supabaseKey: 'sb_publishable_Am1HlpP-4LnmCZX-IZqERA_a32ZNLqt',
  // 038/039 use existing catalog permissions for native documents.
  // Optional separate-table and bulk-import backends 033/034 remain gated.
  problemBackendVersion: 32,
  problemStatementStorage: 'catalog-inline-v1',
  problemEditorialStorage: 'catalog-inline-v1',
  adminProfileEditorEnabled: true
};
