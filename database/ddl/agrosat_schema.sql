-- =============================================================
-- AgroSat - Plataforma de Inteligência Agrícola por Satélite
-- Oracle 19c DDL - Database Design (FIAP GS 2026)
-- =============================================================

-- -------------------------------------------------------------
-- SEQUÊNCIAS
-- -------------------------------------------------------------
CREATE SEQUENCE seq_rural_owner     START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_property        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_crop_record     START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_satellite_obs   START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_climate_data    START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_risk_analysis   START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_credit_contract START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;


-- -------------------------------------------------------------
-- TABELA 1: RURAL_OWNER
-- Proprietários rurais cadastrados na plataforma AgroSat
-- -------------------------------------------------------------
CREATE TABLE RURAL_OWNER (
    id          NUMBER(10)    NOT NULL,
    name        VARCHAR2(150) NOT NULL,
    cpf_cnpj    VARCHAR2(18)  NOT NULL,
    email       VARCHAR2(100),
    phone       VARCHAR2(20),
    city        VARCHAR2(100),
    state       CHAR(2)       NOT NULL,
    created_at  DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_rural_owner
        PRIMARY KEY (id),
    CONSTRAINT uk_rural_owner_cpf
        UNIQUE (cpf_cnpj),
    CONSTRAINT chk_rural_owner_state
        CHECK (state IN (
            'AC','AL','AM','AP','BA','CE','DF','ES','GO','MA',
            'MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN',
            'RO','RR','RS','SC','SE','SP','TO'
        ))
);

COMMENT ON TABLE  RURAL_OWNER            IS 'Proprietários rurais pessoas físicas ou jurídicas cadastrados na plataforma';
COMMENT ON COLUMN RURAL_OWNER.id         IS 'Identificador único do proprietário (PK)';
COMMENT ON COLUMN RURAL_OWNER.name       IS 'Nome completo ou razão social';
COMMENT ON COLUMN RURAL_OWNER.cpf_cnpj   IS 'CPF (pessoa física) ou CNPJ (pessoa jurídica) - chave de unicidade';
COMMENT ON COLUMN RURAL_OWNER.email      IS 'E-mail para notificações de alerta e relatórios';
COMMENT ON COLUMN RURAL_OWNER.phone      IS 'Telefone de contato com DDD';
COMMENT ON COLUMN RURAL_OWNER.city       IS 'Município de residência ou sede';
COMMENT ON COLUMN RURAL_OWNER.state      IS 'UF do proprietário (sigla 2 letras)';
COMMENT ON COLUMN RURAL_OWNER.created_at IS 'Data de cadastro na plataforma';


-- -------------------------------------------------------------
-- TABELA 2: PROPERTY
-- Propriedades rurais monitoradas por satélite
-- -------------------------------------------------------------
CREATE TABLE PROPERTY (
    id           NUMBER(10)    NOT NULL,
    owner_id     NUMBER(10)    NOT NULL,
    area_ha      NUMBER(10,2)  NOT NULL,
    biome        VARCHAR2(50)  NOT NULL,
    municipality VARCHAR2(100) NOT NULL,
    state        CHAR(2)       NOT NULL,
    lat          NUMBER(9,6)   NOT NULL,
    lon          NUMBER(9,6)   NOT NULL,
    created_at   DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_property
        PRIMARY KEY (id),
    CONSTRAINT fk_property_owner
        FOREIGN KEY (owner_id) REFERENCES RURAL_OWNER(id),
    CONSTRAINT chk_property_area
        CHECK (area_ha > 0),
    CONSTRAINT chk_property_biome
        CHECK (biome IN ('Amazônia','Cerrado','Mata Atlântica','Caatinga','Pampa','Pantanal')),
    CONSTRAINT chk_property_state
        CHECK (state IN (
            'AC','AL','AM','AP','BA','CE','DF','ES','GO','MA',
            'MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN',
            'RO','RR','RS','SC','SE','SP','TO'
        ))
);

COMMENT ON TABLE  PROPERTY              IS 'Propriedades rurais georeferenciadas monitoradas via satélite';
COMMENT ON COLUMN PROPERTY.id           IS 'Identificador único da propriedade (PK)';
COMMENT ON COLUMN PROPERTY.owner_id     IS 'Referência ao proprietário (FK → RURAL_OWNER)';
COMMENT ON COLUMN PROPERTY.area_ha      IS 'Área total da propriedade em hectares (deve ser maior que 0)';
COMMENT ON COLUMN PROPERTY.biome        IS 'Bioma brasileiro onde a propriedade está localizada';
COMMENT ON COLUMN PROPERTY.municipality IS 'Município onde a propriedade está registrada';
COMMENT ON COLUMN PROPERTY.state        IS 'UF da propriedade (sigla 2 letras)';
COMMENT ON COLUMN PROPERTY.lat          IS 'Latitude do centroide da propriedade (graus decimais)';
COMMENT ON COLUMN PROPERTY.lon          IS 'Longitude do centroide da propriedade (graus decimais)';
COMMENT ON COLUMN PROPERTY.created_at   IS 'Data de cadastro da propriedade na plataforma';


-- -------------------------------------------------------------
-- TABELA 3: CROP_RECORD
-- Registros de plantio por safra e propriedade
-- -------------------------------------------------------------
CREATE TABLE CROP_RECORD (
    id                     NUMBER(10)   NOT NULL,
    property_id            NUMBER(10)   NOT NULL,
    crop_type              VARCHAR2(50) NOT NULL,
    planting_date          DATE         NOT NULL,
    harvest_date           DATE,
    expected_yield_bags_ha NUMBER(6,2),
    CONSTRAINT pk_crop_record
        PRIMARY KEY (id),
    CONSTRAINT fk_crop_property
        FOREIGN KEY (property_id) REFERENCES PROPERTY(id),
    CONSTRAINT chk_crop_type
        CHECK (crop_type IN (
            'Soja','Milho','Cana-de-Açúcar','Café','Algodão',
            'Arroz','Feijão','Trigo','Sorgo','Outro'
        )),
    CONSTRAINT chk_crop_dates
        CHECK (harvest_date IS NULL OR harvest_date > planting_date),
    CONSTRAINT chk_crop_yield
        CHECK (expected_yield_bags_ha IS NULL OR expected_yield_bags_ha > 0)
);

COMMENT ON TABLE  CROP_RECORD                      IS 'Registros de cultura plantada por safra em cada propriedade';
COMMENT ON COLUMN CROP_RECORD.id                   IS 'Identificador único do registro de plantio (PK)';
COMMENT ON COLUMN CROP_RECORD.property_id          IS 'Referência à propriedade rural (FK → PROPERTY)';
COMMENT ON COLUMN CROP_RECORD.crop_type            IS 'Tipo de cultura plantada nesta safra';
COMMENT ON COLUMN CROP_RECORD.planting_date        IS 'Data de plantio (início da safra)';
COMMENT ON COLUMN CROP_RECORD.harvest_date         IS 'Data prevista ou realizada de colheita (nulo se não concluída)';
COMMENT ON COLUMN CROP_RECORD.expected_yield_bags_ha IS 'Produtividade esperada em sacas por hectare';


-- -------------------------------------------------------------
-- TABELA 4: SATELLITE_OBS
-- Observações satelitais com índices de vegetação por propriedade
-- -------------------------------------------------------------
CREATE TABLE SATELLITE_OBS (
    id              NUMBER(10)  NOT NULL,
    property_id     NUMBER(10)  NOT NULL,
    obs_date        DATE        NOT NULL,
    satellite       VARCHAR2(30) NOT NULL,
    ndvi_mean       NUMBER(5,4)  NOT NULL,
    ndvi_std        NUMBER(5,4),
    evi_mean        NUMBER(5,4),
    cloud_cover_pct NUMBER(5,2)  NOT NULL,
    CONSTRAINT pk_satellite_obs
        PRIMARY KEY (id),
    CONSTRAINT fk_satobs_property
        FOREIGN KEY (property_id) REFERENCES PROPERTY(id),
    CONSTRAINT chk_satobs_satellite
        CHECK (satellite IN ('Sentinel-2','Landsat-8','Landsat-9','MODIS')),
    CONSTRAINT chk_satobs_ndvi
        CHECK (ndvi_mean BETWEEN -1 AND 1),
    CONSTRAINT chk_satobs_ndvi_std
        CHECK (ndvi_std IS NULL OR ndvi_std >= 0),
    CONSTRAINT chk_satobs_evi
        CHECK (evi_mean IS NULL OR evi_mean BETWEEN -1 AND 1),
    CONSTRAINT chk_satobs_cloud
        CHECK (cloud_cover_pct BETWEEN 0 AND 100)
);

COMMENT ON TABLE  SATELLITE_OBS                 IS 'Observações satelitais processadas com índices de vegetação por propriedade';
COMMENT ON COLUMN SATELLITE_OBS.id              IS 'Identificador único da observação (PK)';
COMMENT ON COLUMN SATELLITE_OBS.property_id     IS 'Referência à propriedade monitorada (FK → PROPERTY)';
COMMENT ON COLUMN SATELLITE_OBS.obs_date        IS 'Data de captura da imagem pelo satélite';
COMMENT ON COLUMN SATELLITE_OBS.satellite       IS 'Nome do satélite que capturou a imagem';
COMMENT ON COLUMN SATELLITE_OBS.ndvi_mean       IS 'NDVI médio do talhão - Normalized Difference Vegetation Index (-1 a 1, quanto maior mais saudável)';
COMMENT ON COLUMN SATELLITE_OBS.ndvi_std        IS 'Desvio padrão do NDVI dentro da propriedade (heterogeneidade da lavoura)';
COMMENT ON COLUMN SATELLITE_OBS.evi_mean        IS 'EVI médio - Enhanced Vegetation Index, corrige efeitos atmosféricos (-1 a 1)';
COMMENT ON COLUMN SATELLITE_OBS.cloud_cover_pct IS 'Percentual de cobertura de nuvens no momento da captura (0-100%)';


-- -------------------------------------------------------------
-- TABELA 5: CLIMATE_DATA
-- Dados climáticos históricos por município (fonte: INMET)
-- -------------------------------------------------------------
CREATE TABLE CLIMATE_DATA (
    id               NUMBER(10)    NOT NULL,
    municipality     VARCHAR2(100) NOT NULL,
    state            CHAR(2)       NOT NULL,
    obs_date         DATE          NOT NULL,
    temp_max_c       NUMBER(4,1)   NOT NULL,
    temp_min_c       NUMBER(4,1)   NOT NULL,
    precipitation_mm NUMBER(7,2)   NOT NULL,
    humidity_pct     NUMBER(5,2)   NOT NULL,
    CONSTRAINT pk_climate_data
        PRIMARY KEY (id),
    CONSTRAINT uk_climate_mun_date
        UNIQUE (municipality, state, obs_date),
    CONSTRAINT chk_climate_temp
        CHECK (temp_max_c >= temp_min_c),
    CONSTRAINT chk_climate_precip
        CHECK (precipitation_mm >= 0),
    CONSTRAINT chk_climate_humidity
        CHECK (humidity_pct BETWEEN 0 AND 100),
    CONSTRAINT chk_climate_state
        CHECK (state IN (
            'AC','AL','AM','AP','BA','CE','DF','ES','GO','MA',
            'MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN',
            'RO','RR','RS','SC','SE','SP','TO'
        ))
);

COMMENT ON TABLE  CLIMATE_DATA                  IS 'Dados climáticos diários por município, coletados do INMET (Instituto Nacional de Meteorologia)';
COMMENT ON COLUMN CLIMATE_DATA.id               IS 'Identificador único do registro climático (PK)';
COMMENT ON COLUMN CLIMATE_DATA.municipality     IS 'Município de coleta dos dados climáticos';
COMMENT ON COLUMN CLIMATE_DATA.state            IS 'UF do município (sigla 2 letras)';
COMMENT ON COLUMN CLIMATE_DATA.obs_date         IS 'Data da observação meteorológica';
COMMENT ON COLUMN CLIMATE_DATA.temp_max_c       IS 'Temperatura máxima do dia em graus Celsius';
COMMENT ON COLUMN CLIMATE_DATA.temp_min_c       IS 'Temperatura mínima do dia em graus Celsius';
COMMENT ON COLUMN CLIMATE_DATA.precipitation_mm IS 'Precipitação acumulada no dia em milímetros';
COMMENT ON COLUMN CLIMATE_DATA.humidity_pct     IS 'Umidade relativa do ar média do dia (0-100%)';


-- -------------------------------------------------------------
-- TABELA 6: RISK_ANALYSIS
-- Análises de risco geradas pelos modelos ML da plataforma
-- -------------------------------------------------------------
CREATE TABLE RISK_ANALYSIS (
    id              NUMBER(10)   NOT NULL,
    property_id     NUMBER(10)   NOT NULL,
    analysis_date   DATE         NOT NULL,
    risk_score      NUMBER(5,2)  NOT NULL,
    risk_class      VARCHAR2(10) NOT NULL,
    predicted_yield NUMBER(6,2),
    model_version   VARCHAR2(20) NOT NULL,
    created_at      DATE         DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_risk_analysis
        PRIMARY KEY (id),
    CONSTRAINT fk_risk_property
        FOREIGN KEY (property_id) REFERENCES PROPERTY(id),
    CONSTRAINT chk_risk_score
        CHECK (risk_score BETWEEN 0 AND 100),
    CONSTRAINT chk_risk_class
        CHECK (risk_class IN ('BAIXO','MÉDIO','ALTO')),
    CONSTRAINT chk_risk_yield
        CHECK (predicted_yield IS NULL OR predicted_yield > 0)
);

COMMENT ON TABLE  RISK_ANALYSIS                  IS 'Análises de risco agrícola geradas pelos modelos Random Forest e XGBoost da plataforma';
COMMENT ON COLUMN RISK_ANALYSIS.id               IS 'Identificador único da análise de risco (PK)';
COMMENT ON COLUMN RISK_ANALYSIS.property_id      IS 'Referência à propriedade analisada (FK → PROPERTY)';
COMMENT ON COLUMN RISK_ANALYSIS.analysis_date    IS 'Data de referência para a análise (janela de dados utilizada)';
COMMENT ON COLUMN RISK_ANALYSIS.risk_score       IS 'Score de risco calculado pelo modelo: 0 = risco mínimo, 100 = risco máximo';
COMMENT ON COLUMN RISK_ANALYSIS.risk_class       IS 'Classificação de risco consolidada: BAIXO (0-33), MÉDIO (34-66), ALTO (67-100)';
COMMENT ON COLUMN RISK_ANALYSIS.predicted_yield  IS 'Produtividade prevista pelo modelo LSTM em sacas/hectare';
COMMENT ON COLUMN RISK_ANALYSIS.model_version    IS 'Versão do modelo ML utilizado (ex: rf-v1.2, xgb-v2.0)';
COMMENT ON COLUMN RISK_ANALYSIS.created_at       IS 'Data/hora de geração da análise';


-- -------------------------------------------------------------
-- TABELA 7: CREDIT_CONTRACT
-- Contratos de crédito rural vinculados a análises de risco
-- -------------------------------------------------------------
CREATE TABLE CREDIT_CONTRACT (
    id               NUMBER(10)    NOT NULL,
    property_id      NUMBER(10)    NOT NULL,
    risk_analysis_id NUMBER(10)    NOT NULL,
    creditor         VARCHAR2(100) NOT NULL,
    amount_brl       NUMBER(15,2)  NOT NULL,
    interest_rate    NUMBER(5,4)   NOT NULL,
    term_months      NUMBER(3)     NOT NULL,
    status           VARCHAR2(20)  DEFAULT 'ATIVO' NOT NULL,
    created_at       DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_credit_contract
        PRIMARY KEY (id),
    CONSTRAINT fk_contract_property
        FOREIGN KEY (property_id) REFERENCES PROPERTY(id),
    CONSTRAINT fk_contract_risk
        FOREIGN KEY (risk_analysis_id) REFERENCES RISK_ANALYSIS(id),
    CONSTRAINT chk_contract_amount
        CHECK (amount_brl > 0),
    CONSTRAINT chk_contract_rate
        CHECK (interest_rate > 0),
    CONSTRAINT chk_contract_term
        CHECK (term_months > 0),
    CONSTRAINT chk_contract_status
        CHECK (status IN ('ATIVO','QUITADO','INADIMPLENTE','CANCELADO'))
);

COMMENT ON TABLE  CREDIT_CONTRACT                    IS 'Contratos de crédito rural emitidos com base em análise de risco da plataforma AgroSat';
COMMENT ON COLUMN CREDIT_CONTRACT.id                 IS 'Identificador único do contrato (PK)';
COMMENT ON COLUMN CREDIT_CONTRACT.property_id        IS 'Referência à propriedade financiada (FK → PROPERTY)';
COMMENT ON COLUMN CREDIT_CONTRACT.risk_analysis_id   IS 'Análise de risco que embasou a concessão do crédito (FK → RISK_ANALYSIS)';
COMMENT ON COLUMN CREDIT_CONTRACT.creditor           IS 'Nome da instituição financeira ou fintech credora';
COMMENT ON COLUMN CREDIT_CONTRACT.amount_brl         IS 'Valor do crédito concedido em Reais (deve ser maior que zero)';
COMMENT ON COLUMN CREDIT_CONTRACT.interest_rate      IS 'Taxa de juros anual em decimal (ex: 0.1250 = 12,50% a.a.)';
COMMENT ON COLUMN CREDIT_CONTRACT.term_months        IS 'Prazo do contrato em meses (deve ser maior que zero)';
COMMENT ON COLUMN CREDIT_CONTRACT.status             IS 'Situação atual do contrato: ATIVO, QUITADO, INADIMPLENTE ou CANCELADO';
COMMENT ON COLUMN CREDIT_CONTRACT.created_at         IS 'Data de emissão do contrato';


-- -------------------------------------------------------------
-- ÍNDICES (performance)
-- -------------------------------------------------------------
CREATE INDEX idx_property_owner        ON PROPERTY(owner_id);
CREATE INDEX idx_property_state        ON PROPERTY(state);
CREATE INDEX idx_crop_property         ON CROP_RECORD(property_id);
CREATE INDEX idx_crop_type             ON CROP_RECORD(crop_type);
CREATE INDEX idx_satobs_property_date  ON SATELLITE_OBS(property_id, obs_date);
CREATE INDEX idx_climate_mun_date      ON CLIMATE_DATA(municipality, obs_date);
CREATE INDEX idx_risk_property_date    ON RISK_ANALYSIS(property_id, analysis_date);
CREATE INDEX idx_risk_class            ON RISK_ANALYSIS(risk_class);
CREATE INDEX idx_contract_property     ON CREDIT_CONTRACT(property_id);
CREATE INDEX idx_contract_status       ON CREDIT_CONTRACT(status);
