CREATE OR ALTER VIEW dbo.vw_powerbi_deal_base
AS
SELECT
  d.deal_id,
  d.title,
  d.value,
  d.currency,
  d.status,
  d.stage_id,
  s.stage_name,
  s.stage_order,
  d.user_id,
  u.user_name,
  d.org_id,
  o.org_name,
  d.update_time,
  d.updated_at
FROM dbo.fact_deal_current d
LEFT JOIN dbo.dim_stage s ON d.stage_id = s.stage_id
LEFT JOIN dbo.dim_user u ON d.user_id = u.user_id
LEFT JOIN dbo.dim_org o ON d.org_id = o.org_id;
GO
