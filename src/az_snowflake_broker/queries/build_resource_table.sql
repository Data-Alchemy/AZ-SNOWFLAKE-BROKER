-- Only one sql statement at a time using base snowpark lib --

CREATE TABLE IF NOT EXISTS T_RESOURCE_INFO_FACT (
--
  id                    VARCHAR(40)     DEFAULT UUID_STRING()               NOT NULL,
  RESOURCE_ID           VARCHAR(255)                                        NOT NULL,
  RESOURCE_NAME         VARCHAR(255)                                        NOT NULL,
  CLOUD_PROVIDER        VARCHAR(40)                                         NOT NULL,
  ENVIRONMENT           VARCHAR(255)                                        NOT NULL,
  RESOURCE_GROUP        VARCHAR(255)                                        NOT NULL,        
  LOCATION              VARCHAR(255)                                        NOT NULL,
  DESCRIPTION           VARCHAR(1000)                                               ,
  TYPE                  VARCHAR(255)                                        NOT NULL,
  PROPERTIES            VARCHAR(16777216)                                           ,
  TAGS                  VARIANT                                                     ,
  ENABLED               BOOLEAN                                                     ,
  MOD_ACTION_TYPE       VARCHAR(255)    DEFAULT 'U'                         NOT NULL,
  RESOURCE_CREATION_TS  VARCHAR(255)                                                ,
  ETL_MODIFIED_TS       TIMESTAMP       DEFAULT CURRENT_TIMESTAMP()         NOT NULL,
  MODIFIED_BY_USER      VARCHAR(255)    DEFAULT CURRENT_USER()              NOT NULL,
  MODIFIED_BY_ROLE      VARCHAR(255)    DEFAULT CURRENT_ROLE()              NOT NULL,
  USER_DEFINED_TAGS     VARIANT                                                     ,
  IN_SYNC               BOOLEAN         DEFAULT FALSE
--
) 
  COMMENT = 'Table for tracking cloud resources and managing tagging' ;
