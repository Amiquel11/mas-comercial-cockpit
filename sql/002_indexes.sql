IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_fact_deal_current_stage_status' AND object_id = OBJECT_ID('dbo.fact_deal_current'))
  CREATE INDEX IX_fact_deal_current_stage_status
  ON dbo.fact_deal_current(stage_id, status)
  INCLUDE (value, currency, update_time);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_fact_deal_current_user_update' AND object_id = OBJECT_ID('dbo.fact_deal_current'))
  CREATE INDEX IX_fact_deal_current_user_update
  ON dbo.fact_deal_current(user_id, update_time DESC)
  INCLUDE (stage_id, status, value);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_fact_deal_stage_event_deal_time' AND object_id = OBJECT_ID('dbo.fact_deal_stage_event'))
  CREATE INDEX IX_fact_deal_stage_event_deal_time
  ON dbo.fact_deal_stage_event(deal_id, event_update_time DESC)
  INCLUDE (stage_id, status, value, currency);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_fact_deal_stage_event_stage_time' AND object_id = OBJECT_ID('dbo.fact_deal_stage_event'))
  CREATE INDEX IX_fact_deal_stage_event_stage_time
  ON dbo.fact_deal_stage_event(stage_id, event_update_time DESC)
  INCLUDE (deal_id, status, value);
GO
