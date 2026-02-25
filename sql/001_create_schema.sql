IF OBJECT_ID('dbo.etl_watermark', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.etl_watermark (
    process_name NVARCHAR(100) NOT NULL PRIMARY KEY,
    last_update_time DATETIME2(0) NOT NULL,
    updated_at DATETIME2(0) NOT NULL
  );
END;
GO

IF OBJECT_ID('dbo.dim_stage', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.dim_stage (
    stage_id INT NOT NULL PRIMARY KEY,
    stage_name NVARCHAR(150) NOT NULL,
    stage_order INT NULL,
    pipeline_id INT NULL,
    updated_at DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME()
  );
END;
GO

IF OBJECT_ID('dbo.dim_user', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.dim_user (
    user_id INT NOT NULL PRIMARY KEY,
    user_name NVARCHAR(200) NOT NULL,
    updated_at DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME()
  );
END;
GO

IF OBJECT_ID('dbo.dim_org', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.dim_org (
    org_id INT NOT NULL PRIMARY KEY,
    org_name NVARCHAR(200) NOT NULL,
    updated_at DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME()
  );
END;
GO

IF OBJECT_ID('dbo.fact_deal_current', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.fact_deal_current (
    deal_id INT NOT NULL PRIMARY KEY,
    title NVARCHAR(300) NOT NULL,
    value DECIMAL(18,2) NULL,
    currency NVARCHAR(10) NULL,
    status NVARCHAR(30) NULL,
    stage_id INT NULL,
    user_id INT NULL,
    org_id INT NULL,
    update_time DATETIME2(0) NULL,
    raw_payload NVARCHAR(MAX) NULL,
    updated_at DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_fact_deal_current_stage FOREIGN KEY (stage_id) REFERENCES dbo.dim_stage(stage_id),
    CONSTRAINT FK_fact_deal_current_user FOREIGN KEY (user_id) REFERENCES dbo.dim_user(user_id),
    CONSTRAINT FK_fact_deal_current_org FOREIGN KEY (org_id) REFERENCES dbo.dim_org(org_id)
  );
END;
GO

IF OBJECT_ID('dbo.fact_deal_stage_event', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.fact_deal_stage_event (
    event_id BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    deal_id INT NOT NULL,
    stage_id INT NULL,
    status NVARCHAR(30) NULL,
    event_update_time DATETIME2(0) NULL,
    value DECIMAL(18,2) NULL,
    currency NVARCHAR(10) NULL,
    captured_at DATETIME2(0) NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_fact_stage_event_stage FOREIGN KEY (stage_id) REFERENCES dbo.dim_stage(stage_id)
  );
END;
GO
