# ETC Pipeline & Cloud Architecture (GCP / AWS)

## Extract → Transform → Consume Data Pipeline

---

## 📥 EXTRACT LAYER

### Cloud Storage / Object Store
**GCP:** Cloud Storage (GCS) | **AWS:** S3
- Batch files, logs, archives
- Landing zone for raw data
- Supports all file formats (CSV, JSON, Parquet, Avro)

### Streaming & Messaging
**GCP:** Pub/Sub | **AWS:** Kinesis Data Streams
- Real-time event streaming
- IoT sensors, clickstreams, application logs
- At-least-once delivery, ordering guarantees

### Change Data Capture (CDC)
**GCP:** Datastream | **AWS:** Database Migration Service (DMS)
- Real-time replication from RDBMS
- Supports MySQL, PostgreSQL, Oracle, SQL Server
- Minimal impact on source systems

### Data Migration
**GCP:** Transfer Service | **AWS:** DataSync
- Cross-cloud and on-premises migration
- Scheduled transfers, incremental sync
- Bandwidth optimization

### SaaS Integration
**GCP:** BigQuery Data Transfer | **AWS:** AppFlow
- Pre-built connectors for SaaS apps
- Google Analytics, YouTube, Ads, Salesforce, SAP
- Automated scheduled imports

---

## ⚙️ TRANSFORM LAYER

### Unified ETL Processing
**GCP:** Dataflow (Apache Beam) | **AWS:** Glue + Kinesis Data Analytics
- Unified batch and streaming with same code (GCP)
- Separate services for batch vs stream (AWS)
- Auto-scaling, serverless execution
- Python, Java, Go SDKs

### Big Data Processing
**GCP:** Dataproc | **AWS:** Elastic MapReduce (EMR)
- Managed Spark and Hadoop clusters
- Ephemeral clusters, auto-scaling
- Support for Hive, Pig, Presto, Flink
- Cost-effective for large-scale transformations

### Serverless Functions
**GCP:** Cloud Functions | **AWS:** Lambda
- Event-driven transformations
- Languages: Python, Node.js, Go, Java, .NET
- Triggers from storage, Pub/Sub, HTTP
- Sub-second billing, auto-scaling

### Workflow Orchestration
**GCP:** Cloud Composer | **AWS:** Managed Workflows for Apache Airflow (MWAA)
- Apache Airflow managed service
- DAG-based workflow definitions
- Complex dependencies, scheduling, retries
- Integration with all cloud services

### Visual Data Preparation
**GCP:** Dataprep | **AWS:** Glue DataBrew
- No-code data wrangling
- Visual interface for cleaning, normalization
- Profile and quality checks
- Generate transformation recipes

---

## 💾 STORAGE LAYER

### Data Warehouse
**GCP:** BigQuery | **AWS:** Redshift / Redshift Serverless
- Serverless, petabyte-scale analytics
- Columnar storage, automatic optimization
- Standard SQL, geospatial, ML functions
- Pay-per-query (BQ) vs cluster-based (Redshift)

### Relational Database (OLTP)
**GCP:** Cloud SQL | **AWS:** RDS (Relational Database Service)
- Managed MySQL, PostgreSQL, SQL Server
- Automated backups, point-in-time recovery
- Read replicas, high availability
- ACID transactions, referential integrity

### NoSQL Wide-Column
**GCP:** Bigtable | **AWS:** DynamoDB
- Sub-10ms latency, millions of QPS
- Bigtable: HBase API, scan operations
- DynamoDB: Key-value, single-digit ms
- Time-series, IoT, real-time analytics

### NoSQL Document Store
**GCP:** Firestore | **AWS:** DocumentDB (MongoDB-compatible)
- JSON document storage
- Real-time synchronization
- Offline support, mobile SDKs
- ACID transactions, indexing

### Globally Distributed SQL
**GCP:** Cloud Spanner | **AWS:** Aurora Global Database
- Horizontal scaling with SQL semantics
- Multi-region, strong consistency
- 99.999% availability SLA
- Global transactions, automatic sharding

### Data Lake
**GCP:** Cloud Storage | **AWS:** S3
- Store raw, semi-structured, unstructured data
- Parquet, ORC, Avro for analytics
- Lifecycle policies, versioning
- Foundation for lakehouse architecture

---

## 📊 CONSUME / ANALYTICS LAYER

### Business Intelligence Platform
**GCP:** Looker | **AWS:** QuickSight
- Enterprise BI with semantic layer
- Looker: LookML modeling language
- QuickSight: SPICE in-memory engine
- Embedded analytics, dashboards, alerts

### Data Visualization
**GCP:** Data Studio (Looker Studio) | **AWS:** QuickSight
- Free interactive dashboards
- Drag-and-drop report builder
- Real-time data connections
- Sharing and collaboration

### Machine Learning Platform
**GCP:** Vertex AI | **AWS:** SageMaker
- End-to-end ML lifecycle
- AutoML for no-code model training
- Custom model development (TensorFlow, PyTorch, scikit-learn)
- Model deployment, monitoring, versioning
- Feature store, pipelines, experiments

### ML Model Training
**GCP:** Vertex AI Training | **AWS:** SageMaker Training
- Distributed training on GPUs/TPUs
- Hyperparameter tuning
- Built-in algorithms
- Bring your own container

### ML Model Serving
**GCP:** Vertex AI Predictions | **AWS:** SageMaker Endpoints
- REST API for predictions
- Auto-scaling, A/B testing
- Batch and online inference
- Model monitoring and drift detection

### Data APIs
**GCP:** Cloud Endpoints, API Gateway | **AWS:** API Gateway, AppSync
- RESTful and GraphQL APIs
- Authentication, rate limiting
- Serving data to applications
- Real-time subscriptions

### Notebooks & Analysis
**GCP:** Vertex AI Workbench | **AWS:** SageMaker Notebooks
- Jupyter-based data exploration
- Pre-configured kernels
- Git integration, collaboration
- Direct access to data sources

---

## 🔒 SECURITY & GOVERNANCE

### Identity & Access Management
**GCP:** Cloud IAM | **AWS:** IAM
- Fine-grained access control
- Role-based access (RBAC)
- Service accounts, temporary credentials
- Policy inheritance, conditional access

### Secrets Management
**GCP:** Secret Manager | **AWS:** Secrets Manager
- Encrypted credential storage
- Automatic rotation
- Version management
- Audit logging

### Data Loss Prevention
**GCP:** Cloud DLP API | **AWS:** Macie
- PII detection and redaction
- Sensitive data discovery
- De-identification techniques
- Compliance scanning (GDPR, HIPAA, PCI-DSS)

### Network Security
**GCP:** VPC Service Controls | **AWS:** VPC, Security Groups
- Network perimeter protection
- Private service access
- VPC peering, shared VPC
- Firewall rules, NACLs

### Data Catalog & Metadata
**GCP:** Data Catalog | **AWS:** Glue Data Catalog
- Centralized metadata repository
- Data discovery and search
- Schema registry
- Lineage tracking

### Data Governance
**GCP:** Dataplex | **AWS:** Lake Formation
- Data mesh architecture support
- Data quality monitoring
- Access policies and permissions
- Security and compliance enforcement

### Audit Logging
**GCP:** Cloud Logging | **AWS:** CloudTrail
- Comprehensive audit trails
- Admin activity, data access logs
- Real-time log analysis
- Long-term retention

### Monitoring & Observability
**GCP:** Cloud Monitoring | **AWS:** CloudWatch
- Metrics, logs, traces
- Alerting and dashboards
- SLI/SLO tracking
- Cost monitoring

---

## 🎯 COMMON ARCHITECTURE PATTERNS

### 1. Batch Processing Pattern
**GCP:** GCS → Dataflow → BigQuery → Looker  
**AWS:** S3 → Glue → Redshift → QuickSight

**Use Cases:**
- Daily/weekly reports and analytics
- Historical data analysis
- Data warehouse ETL pipelines
- Large-scale data transformations

**Characteristics:**
- Scheduled execution
- High throughput
- Cost-effective for large volumes
- Eventual consistency

---

### 2. Real-time Streaming Pattern
**GCP:** Pub/Sub → Dataflow → BigQuery → Data Studio  
**AWS:** Kinesis → Lambda/Flink → Redshift → QuickSight

**Use Cases:**
- IoT sensor data processing
- Clickstream analytics
- Application monitoring
- Fraud detection
- Real-time dashboards

**Characteristics:**
- Sub-second latency
- Continuous processing
- Windowing and aggregations
- At-least-once processing

---

### 3. Machine Learning Pattern
**GCP:** BigQuery → Vertex AI → Model → Predictions API  
**AWS:** Redshift → SageMaker → Model → Endpoint

**Use Cases:**
- Recommendation engines
- Demand forecasting
- Customer churn prediction
- Image/text classification
- Anomaly detection

**Characteristics:**
- Feature engineering from DW
- AutoML or custom training
- Model versioning and A/B testing
- Real-time and batch predictions

---

### 4. Data Lake Pattern
**GCP:** GCS (raw) → Dataproc → GCS (processed) → BigQuery  
**AWS:** S3 (raw) → EMR → S3 (processed) → Redshift/Athena

**Use Cases:**
- Multi-structured data storage
- Schema-on-read analytics
- Data science exploration
- Long-term data retention
- Compliance and archival

**Characteristics:**
- Store raw data indefinitely
- Separate storage from compute
- Support all data formats
- Cost-optimized storage tiers

---

### 5. Change Data Capture (CDC) Pattern
**GCP:** MySQL/PostgreSQL → Datastream → BigQuery → Dashboard  
**AWS:** RDS → DMS → Redshift → QuickSight

**Use Cases:**
- Real-time analytics from operational DBs
- Data warehouse synchronization
- Event-driven architectures
- Audit and compliance tracking

**Characteristics:**
- Minimal source system impact
- Low-latency replication
- Insert, update, delete tracking
- Incremental data sync

---

### 6. Hybrid Cloud Pattern
**GCP:** On-prem → Transfer Service → GCS → Dataflow → BigQuery  
**AWS:** On-prem → DataSync → S3 → Glue → Redshift

**Use Cases:**
- Cloud migration projects
- Hybrid data analytics
- Disaster recovery
- Multi-cloud architectures

**Characteristics:**
- Incremental data transfer
- Bandwidth optimization
- Encryption in transit
- Compliance with data residency

---

## 🔑 KEY TECHNICAL CONCEPTS

### Serverless Computing
**GCP:** BigQuery, Dataflow, Cloud Functions  
**AWS:** Redshift Serverless, Lambda, Glue

- No infrastructure management
- Automatic scaling (scale to zero)
- Pay-per-use pricing model
- Event-driven architectures
- Faster time to production

---

### Unified Streaming & Batch
**GCP:** Dataflow handles both with same Apache Beam code  
**AWS:** Separate services (Glue for batch, Kinesis for streaming)

**Benefits:**
- Single codebase for batch and stream
- Consistent processing logic
- Easier testing and maintenance
- Reduced operational complexity

---

### Columnar Storage
**Technology:** BigQuery, Redshift, Parquet, ORC

**Advantages:**
- 10-100x faster for analytics queries
- Better compression ratios (3-10x)
- Efficient for selective column reads
- Predicate pushdown optimization
- Vectorized query execution

---

### Change Data Capture (CDC)
**Tools:** Datastream, DMS, Debezium

**How it works:**
- Read database transaction logs
- Capture inserts, updates, deletes
- Stream changes in real-time
- Minimal performance impact
- Enable event-driven architectures

---

### Data Lake vs Data Warehouse
**Data Lake (GCS/S3):**
- Store raw, unprocessed data
- Schema-on-read
- Support all data types
- Lower storage costs
- Exploratory analytics

**Data Warehouse (BigQuery/Redshift):**
- Store processed, structured data
- Schema-on-write
- Optimized for SQL queries
- Higher performance
- Production reporting

---

### Lakehouse Architecture
**Combines best of both:**
- Data lake flexibility
- Data warehouse performance
- ACID transactions on data lake
- BI tools query directly
- Technologies: Delta Lake, Apache Iceberg, Apache Hudi

---

### Global Distribution
**GCP Spanner / AWS Aurora Global:**
- Strong consistency across regions
- Sub-100ms replication
- Automatic failover
- 99.999% availability
- Use cases: Global apps, disaster recovery

---

### Data Partitioning
**Benefits:**
- Query performance optimization
- Cost reduction (scan less data)
- Easier data lifecycle management
- Common strategies: Time-based, hash, range

---

### Data Clustering
**BigQuery Clustering / Redshift Sort Keys:**
- Co-locate related data
- Faster query execution
- Automatic maintenance
- Combine with partitioning

---

## 📋 SERVICE COMPARISON MATRIX

| Category | GCP | AWS | Key Difference |
|----------|-----|-----|----------------|
| **Object Storage** | Cloud Storage (GCS) | S3 | Similar features, S3 has more storage classes |
| **Streaming** | Pub/Sub | Kinesis Data Streams | Pub/Sub: global, auto-scaling; Kinesis: shard-based |
| **Batch ETL** | Dataflow | Glue | Dataflow: unified batch+stream; Glue: batch only |
| **Stream Processing** | Dataflow | Kinesis Data Analytics | Dataflow: Apache Beam; Kinesis: Flink/SQL |
| **Big Data** | Dataproc | EMR | Very similar, both managed Spark/Hadoop |
| **Serverless Functions** | Cloud Functions | Lambda | Similar, Lambda has broader ecosystem |
| **Orchestration** | Cloud Composer | MWAA | Both managed Airflow |
| **Data Warehouse** | BigQuery | Redshift | BQ: fully serverless; Redshift: cluster or serverless |
| **OLTP Database** | Cloud SQL | RDS | Similar managed relational DB |
| **NoSQL Wide-Column** | Bigtable | DynamoDB | Bigtable: HBase API; DynamoDB: simpler key-value |
| **Global SQL** | Cloud Spanner | Aurora Global | Spanner: true global consistency |
| **BI Platform** | Looker | QuickSight | Looker: more enterprise features |
| **ML Platform** | Vertex AI | SageMaker | Both comprehensive, similar capabilities |
| **CDC** | Datastream | DMS | Similar capabilities |
| **Data Catalog** | Data Catalog | Glue Catalog | AWS tighter integration with Glue jobs |
| **Data Governance** | Dataplex | Lake Formation | Lake Formation: more mature |

---

## 💡 BEST PRACTICES

### Data Ingestion
- Use appropriate ingestion method (batch vs streaming)
- Implement retry logic and dead-letter queues
- Validate data quality at ingestion
- Use compression for network transfer
- Implement idempotency for duplicate handling

### Data Processing
- Partition data for parallel processing
- Use appropriate instance types (compute vs memory)
- Implement checkpointing for fault tolerance
- Monitor job performance and costs
- Use spot/preemptible instances for cost savings

### Data Storage
- Choose right storage based on access patterns
- Implement data lifecycle policies
- Use appropriate compression (Snappy, Gzip, Zstandard)
- Partition and cluster tables
- Regular maintenance (VACUUM, ANALYZE)

### Security
- Principle of least privilege
- Encrypt data at rest and in transit
- Regular access reviews
- Enable audit logging
- Implement data classification
- Use private endpoints for sensitive data

### Performance Optimization
- Materialize frequently accessed aggregations
- Use caching layers (Redis, Memcached)
- Implement query result caching
- Optimize table schemas and indexes
- Monitor and tune query performance

### Cost Optimization
- Right-size compute resources
- Use committed use discounts / reserved instances
- Implement auto-scaling policies
- Archive cold data to cheaper storage
- Monitor and set budget alerts
- Use spot instances for non-critical workloads

---

## 🚀 EMERGING TRENDS

### Data Mesh
- Decentralized data ownership
- Domain-oriented data products
- Self-serve data infrastructure
- Federated governance

### Real-time Analytics
- Sub-second query latency
- Streaming-first architectures
- Materialized views
- Real-time ML inference

### Data Fabric
- Unified data management layer
- Active metadata
- Knowledge graphs
- Automated data integration

### MLOps & DataOps
- CI/CD for ML models
- Automated testing and deployment
- Model monitoring and drift detection
- Feature stores

### Privacy-Preserving Analytics
- Differential privacy
- Federated learning
- Homomorphic encryption
- Secure multi-party computation

---

## 📚 INTERVIEW TALKING POINTS

### Architecture Design
- Start with requirements (latency, scale, cost)
- Choose appropriate pattern (batch, streaming, ML)
- Consider data characteristics (volume, velocity, variety)
- Design for scalability and fault tolerance
- Plan for monitoring and observability

### Service Selection
- Compare GCP vs AWS offerings
- Discuss trade-offs (cost, features, complexity)
- Consider team expertise and existing infrastructure
- Evaluate managed vs self-managed options
- Think about vendor lock-in and portability

### Data Modeling
- Dimensional modeling for DW (star/snowflake schema)
- Denormalization for performance
- Partitioning and clustering strategies
- Slowly Changing Dimensions (SCD) handling
- Data quality and validation rules

### Performance & Scale
- Horizontal vs vertical scaling
- Caching strategies
- Query optimization techniques
- Distributed processing patterns
- Handling skewed data

### Security & Compliance
- Data encryption requirements
- Access control mechanisms
- Audit logging and monitoring
- Compliance standards (GDPR, HIPAA, SOC2)
- Data retention and deletion policies

---

**Document Version:** 1.0  
**Last Updated:** December 2024  
**Purpose:** Interview preparation and technical reference
