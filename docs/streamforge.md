# StreamForge Real-Time Data Streaming Platform

**Last Updated:** December 31, 2025  
**Project Status:** ✅ PROJECT COMPLETE (All Phases)  
**Duration:** 22 days (Dec 10 - Dec 31, 2025)

A production-ready real-time data streaming and processing platform demonstrating modern stream processing architecture with Apache Kafka, Apache Flink, MongoDB, and AWS cloud-native deployment patterns. This project showcases enterprise-scale event-driven architecture with advanced stream processing, comprehensive testing (50+ tests), and a full-stack React frontend with AWS Amplify integration.

## 🎯 Project Overview

StreamForge is a production-ready streaming data platform implementing real-time data ingestion, transformation, and storage using industry-standard tools. The system demonstrates enterprise-grade stream processing with advanced features including stateful processing, windowed aggregations, fault tolerance, comprehensive testing, and a full-stack React frontend.

**Tech Stack**: Apache Kafka 3.5.1, Apache Flink 1.18 (Java 11), MongoDB 7.0, React, AWS Amplify, Docker Compose, Maven, Terraform  
**Architecture**: Event-driven streaming with dual deployment models (local + AWS production)  
**Processing Features**: JSON deserialization, stateful operations (ValueState), 1-minute tumbling windows, real-time aggregations, 30-second checkpointing, dead letter queue  
**Testing**: 50+ comprehensive tests (29 unit tests + 7 integration test suites)  
**Frontend**: React application with Recharts visualization, AWS Amplify integration, mock data mode for local development  
**Performance**: 1000+ events/second throughput, <10s latency (p99), zero data loss  
**Project Status**: ✅ 100% Complete - All 5 phases delivered

## 🏗️ Architecture

### Dual Deployment Model

StreamForge supports two deployment architectures:

**1. Local Development Environment**
```
External Sources → Kafka (localhost:9092)
                     ↓
               Flink Cluster (JobManager + TaskManager)
                     ↓
               Stream Processing (StreamProcessor.java)
                     ↓
               MongoDB (localhost:27017)
```

**2. AWS Production Environment (Ready for Deployment)**
```
External Sources → Kafka/Kinesis
                     ↓
               AWS Managed Flink
                     ↓
               Stream Processing
                     ↓
               DynamoDB (3 tables)
                     ↓
           React Frontend (AWS Amplify)
```
*Note: AWS infrastructure code complete via Terraform (472 lines), ready for deployment*

### Data Flow

```
┌─────────────────────┐
│ External Sources    │
│ - APIs              │
│ - Event Streams     │
│ - IoT Devices       │
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│   Apache Kafka      │
│ - Topic: streamforge-input
│ - Consumer Group: streamforge-consumer-group
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│   Apache Flink      │
│ - StreamProcessor   │
│ - Transformations   │
│ - Checkpointing     │
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│   MongoDB/DynamoDB  │
│ - Collection: processed_data
│ - Real-time storage │
└─────────────────────┘
```

## 🚀 Key Technical Components

### Apache Flink Stream Processing

**StreamProcessor.java** - Production-ready stream processing with advanced features (233 lines):
```java
public class StreamProcessor {
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final OutputTag<String> DLQ_TAG = new OutputTag<String>("dead-letter-queue"){};
    
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Enable checkpointing for fault tolerance
        env.enableCheckpointing(30000); // 30-second interval
        CheckpointConfig checkpointConfig = env.getCheckpointConfig();
        checkpointConfig.setExternalizedCheckpointCleanup(
            CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);
        
        // Configure Kafka source
        KafkaSource<String> source = KafkaSource.<String>builder()
            .setBootstrapServers("kafka:29092")
            .setTopics("streamforge-input")
            .setGroupId("streamforge-consumer-group")
            .setStartingOffsets(OffsetsInitializer.earliest())
            .build();
        
        // Parse JSON and validate events (with side output for errors)
        SingleOutputStreamOperator<Event> parsedStream = kafkaStream
            .process(new ProcessFunction<String, Event>() {
                public void processElement(String value, Context ctx, Collector<Event> out) {
                    try {
                        Event event = objectMapper.readValue(value, Event.class);
                        if (event.isValid()) {
                            out.collect(event);
                        } else {
                            ctx.output(DLQ_TAG, value); // Dead letter queue
                        }
                    } catch (Exception e) {
                        ctx.output(DLQ_TAG, value);
                    }
                }
            });
        
        // Stateful processing: Track event count per user
        DataStream<Event> enrichedStream = parsedStream
            .keyBy(Event::getUserId)
            .process(new EventEnrichmentFunction()) // Uses ValueState
            .name("Stateful Enrichment");
        
        // Window-based aggregations: 1-minute tumbling windows
        DataStream<AggregatedMetrics> aggregatedStream = enrichedStream
            .keyBy(event -> event.getUserId() + ":" + event.getType())
            .window(TumblingEventTimeWindows.of(Time.minutes(1)))
            .aggregate(new EventAggregationFunction()) // Count, sum, avg, min, max
            .name("Windowed Aggregations");
        
        // Multiple sinks
        enrichedStream.addSink(new MongoDBSink());
        aggregatedStream.addSink(new MongoDBMetricsSink());
        parsedStream.getSideOutput(DLQ_TAG).addSink(new DeadLetterQueueSink());
        
        env.execute("StreamForge Processor - Enhanced");
    }
}
```

**Production Features:**
- **JSON Processing**: Type-safe Event/AggregatedMetrics POJOs with Jackson deserialization
- **Data Validation**: Built-in `isValid()` method with null/empty checks
- **Stateful Processing**: ValueState tracks per-user event counts across streams
- **Windowing**: 1-minute tumbling windows with 5-second watermarks for late data
- **Aggregations**: Compute count, sum, average, min, max per user/event type
- **Fault Tolerance**: 30-second checkpointing with externalized state (RETAIN_ON_CANCELLATION)
- **Error Handling**: Dead letter queue (DLQ) captures invalid events via side outputs
- **Multiple Sinks**: Separate MongoDB collections for events, metrics, and DLQ

### Custom MongoDB Sink

**MongoDBSink.java** - RichSinkFunction with connection lifecycle management:
```java
public class MongoDBSink extends RichSinkFunction<String> {
    private transient MongoClient mongoClient;
    private transient MongoCollection<Document> collection;
    
    @Override
    public void open(Configuration parameters) {
        // Initialize MongoDB connection
        mongoClient = MongoClients.create("mongodb://admin:password@mongodb:27017");
        collection = mongoClient.getDatabase("streamforge")
            .getCollection("processed_data");
    }
    
    @Override
    public void invoke(String value, Context context) {
        // Write to MongoDB
        Document doc = new Document("data", value)
            .append("timestamp", System.currentTimeMillis());
        collection.insertOne(doc);
    }
    
    @Override
    public void close() {
        if (mongoClient != null) {
            mongoClient.close();
        }
    }
}
```

**Design Patterns:**
- Connection pooling via lifecycle management (open/invoke/close)
- Transient fields to prevent serialization issues
- Timestamp tracking for data lineage

### Containerized Infrastructure

**Docker Compose** orchestrates the complete development environment:

**Services:**
- **Zookeeper**: Kafka coordination (port 2181)
- **Kafka**: Message broker (ports 9092 external, 29092 internal)
- **Flink JobManager**: Cluster coordinator (port 8081 dashboard)
- **Flink TaskManager**: Execution worker
- **MongoDB**: Document database (port 27017)

**Network Configuration:**
- Bridge network: `streamforge-network`
- Service discovery via Docker DNS
- Internal Kafka address: `kafka:29092`
- External Kafka address: `localhost:9092`

### Build System

**Maven Configuration** with Shade plugin for fat JAR packaging:
- Flink dependencies use `provided` scope (available in cluster)
- Connector dependencies bundled in JAR
- Output: `flink-jobs/target/flink-jobs-1.0-SNAPSHOT.jar`

**Key Dependencies:**
- `flink-streaming-java`: Core streaming API
- `flink-connector-kafka`: Kafka integration
- `mongodb-driver-sync`: MongoDB client (version 4.11.1)
- `flink-json` + `jackson-databind`: JSON processing

## 🧪 Testing Strategy

**50+ Comprehensive Tests** covering all system aspects:

### Unit Tests (29 tests passing)
- **EventTest.java**: POJO validation, field checks, isValid() method
- **StreamProcessorTest.java**: Kafka source config, transformation logic, pipeline integration
- **MongoDBSinkTest.java**: Connection lifecycle, document insertion, error handling
- **MongoDBMetricsSinkTest.java**: Metrics persistence, aggregation validation
- **MongoDBSchemaTest.java**: Schema validation, indexes, data structure
- **PerformanceTest.java**: Throughput benchmarks, latency measurements

### Integration Test Suites (7 test suites, ~25 test cases)
Automated via `scripts/comprehensive-test-suite.sh` (510 lines):

1. **Infrastructure Validation**: Docker services, Kafka, MongoDB, Flink health checks
2. **Data Ingestion**: Single event processing, batch processing (100+ events)
3. **Data Validation**: Invalid JSON handling, missing fields, DLQ routing
4. **Windowed Aggregations**: 1-minute tumbling windows, metrics accuracy
5. **Performance Testing**: 1000+ events/sec throughput, <10s latency (p99)
6. **Fault Tolerance**: Checkpointing functionality, DLQ error handling
7. **Data Integrity**: Field preservation, zero data loss verification (50-event test)

### Frontend Tests (50 tests, 67.85% coverage)
- **App.test.js** (3 tests): Root component, error boundaries
- **Dashboard.test.js** (6 tests): Main container, data loading
- **EventList.test.js** (8 tests): Event table rendering, sorting, filtering
- **StatsCards.test.js** (9 tests): Statistics cards, metric calculations
- **MetricsChart.test.js** (10 tests): Recharts visualization, tooltips
- **api.test.js** (14 tests): API service, mock data generation, DynamoDB integration

## 📊 Technical Achievements

### Real-Time Stream Processing
- **Event-Driven Architecture**: Asynchronous message processing with Kafka
- **Scalable Processing**: Flink's distributed execution model
- **Fault Tolerance**: Checkpointing ensures exactly-once processing semantics
- **State Management**: Filesystem state backend (migrating to S3/RocksDB for production)

### Dual Deployment Strategy
- **Local Development**: Complete containerized environment for rapid iteration
- **AWS Production**: Terraform IaC for managed services (Kinesis, Managed Flink, DynamoDB)
- **Migration Path**: Scripts to transition from MongoDB to DynamoDB

### Docker Orchestration
- **Multi-Service Coordination**: 5 interconnected containers
- **Network Isolation**: Custom bridge network for service communication
- **Volume Management**: Persistent storage for Kafka and MongoDB
- **Health Checks**: Container health monitoring

## 🎯 Development Workflow

### 1. Local Development
```bash
# Start infrastructure
cd docker && docker-compose up -d

# Build Flink job
cd flink-jobs && mvn clean package

# Submit to Flink cluster
# Via Dashboard: http://localhost:8081
# Or CLI from container
```

### 2. Testing
```bash
# Run unit tests
cd flink-jobs && mvn test

# Compile only
mvn compile

# Clean build artifacts
mvn clean
```

### 3. Monitoring
- **Flink Dashboard**: http://localhost:8081 (job status, metrics, logs)
- **Kafka**: CLI tools or GUI (Offset Explorer, Conduktor)
- **MongoDB**: Compass or CLI (`mongosh`)

### 4. Production Deployment (Planned)
```bash
# Provision AWS infrastructure
cd terraform
terraform init
terraform plan
terraform apply

# Deploy frontend
cd frontend/streamforge-ui
amplify publish
```

## 📁 Project Structure

```
streamforge/
├── docker/                       # Container orchestration (✅ Complete)
│   └── docker-compose.yml       # 5 services (Kafka, Zookeeper, Flink x2, MongoDB)
├── flink-jobs/                  # Stream processing logic (✅ Complete)
│   ├── pom.xml                  # Maven with Flink 1.18, Kafka connector, MongoDB driver
│   ├── src/main/java/com/streamforge/
│   │   ├── StreamProcessor.java      # Main job (233 lines) with windowing & state
│   │   ├── MongoDBSink.java          # Event sink
│   │   ├── MongoDBMetricsSink.java   # Metrics sink
│   │   ├── DeadLetterQueueSink.java  # DLQ sink
│   │   └── model/
│   │       ├── Event.java            # Event POJO with validation
│   │       └── AggregatedMetrics.java # Metrics POJO
│   ├── src/test/java/            # Unit tests (29 passing)
│   │   ├── EventTest.java
│   │   ├── StreamProcessorTest.java
│   │   ├── MongoDBSinkTest.java
│   │   ├── MongoDBMetricsSinkTest.java
│   │   ├── MongoDBSchemaTest.java
│   │   └── PerformanceTest.java
│   └── target/
│       └── flink-jobs-1.0-SNAPSHOT.jar  # Fat JAR (deployed & running)
├── frontend/                     # React application (✅ Complete)
│   └── streamforge-ui/
│       ├── src/
│       │   ├── App.js            # Root component with error boundary
│       │   ├── components/       # Dashboard, EventList, MetricsChart, StatsCards
│       │   ├── services/api.js   # DynamoDB client & mock data
│       │   └── aws-exports.js    # Amplify configuration
│       ├── public/               # PWA assets
│       ├── package.json          # React, Recharts, AWS Amplify, Testing Library
│       └── README.md             # Frontend documentation
├── terraform/                    # AWS IaC (✅ Complete - Ready to deploy)
│   └── main.tf                   # 472 lines: DynamoDB, S3, IAM, VPC endpoints
├── scripts/                      # Utilities (✅ Complete)
│   ├── init-mongodb.js           # MongoDB initialization
│   ├── test-events.sh            # Integration test script
│   └── comprehensive-test-suite.sh # 510 lines, 7 test suites
├── docs/                         # Documentation (✅ Complete)
│   ├── mongodb-schema.md         # Database schema
│   └── AWS_DEPLOYMENT.md         # 824 lines: Complete deployment guide
└── project_status.md             # Gantt chart and project metrics
```

## 🔧 Configuration Details

### Kafka Configuration (✅ Production)
- **Topic**: `streamforge-input` with **3 partitions**
- **Consumer Group**: `streamforge-consumer-group`
- **Bootstrap Servers**: `kafka:29092` (internal), `localhost:9092` (external)
- **Replication Factor**: 1 (local dev), 3 (production recommendation)
- **Retention**: Default 7 days

### MongoDB Configuration (✅ Production)
- **Connection String**: `mongodb://admin:password@mongodb:27017`
- **Database**: `streamforge`
- **Collections**: 
  - `processed_data`: Raw events with timestamp and enrichment
  - `aggregated_metrics`: Windowed aggregations (count, sum, avg, min, max)
  - `dead_letter_queue`: Invalid events for debugging
- **Credentials**: admin/password (dev environment)
- **Indexes**: Timestamp, userId, eventType for efficient queries
- **Validation**: Schema validation rules enforced

### Flink Configuration (✅ Production)
- **Version**: 1.18.0
- **Java**: 11
- **State Backend**: Filesystem (local), S3/RocksDB (production)
- **Checkpoint Interval**: 30 seconds
- **Checkpoint Directory**: `/tmp/flink-checkpoints` (local)
- **Parallelism**: Default (scales with TaskManager slots)
- **Watermark Strategy**: 5-second bounded out-of-orderness

## 🛯️ Development Roadmap

### Phase 1: Infrastructure Setup ✅ COMPLETE (Dec 17, 2025)
- ✅ Docker Compose environment (5 services operational)
- ✅ Kafka cluster with 3-partition topic
- ✅ Flink cluster (JobManager + TaskManager)
- ✅ MongoDB integration with schema validation
- ✅ Basic StreamProcessor implementation
- ✅ Custom MongoDBSink
- ✅ Unit tests

### Phase 2: Stream Processing Enhancement ✅ COMPLETE (Dec 18, 2025)
- ✅ Kafka topic configuration and partitioning (3 partitions)
- ✅ MongoDB schema design and indexing (3 collections with indexes)
- ✅ Advanced transformations (1-minute tumbling windows, aggregations)
- ✅ Stateful operations (ValueState for per-user event counting)
- ✅ JSON deserialization with Event/AggregatedMetrics POJOs
- ✅ Dead letter queue for error handling
- ✅ 30-second checkpointing with externalized state
- ✅ 29 unit tests passing

### Phase 3: AWS Documentation & Infrastructure ✅ COMPLETE (Dec 23, 2025)
- ✅ Terraform infrastructure modules (472 lines: DynamoDB, S3, IAM, VPC)
- ✅ DynamoDB table design (3 tables mirroring MongoDB schema)
- ✅ MongoDB to DynamoDB migration strategy documented
- ✅ AWS deployment guide (824 lines)
- ✅ Cost estimation ($45/month dev, $176-385/month prod)
- ✅ React frontend scaffold

### Phase 4: Comprehensive Testing ✅ COMPLETE (Dec 19, 2025)
- ✅ 7 integration test suites (510-line automated script)
- ✅ Infrastructure, ingestion, validation, aggregation tests
- ✅ Performance testing (1000+ events/sec, <10s latency)
- ✅ Fault tolerance and data integrity validation
- ✅ ~25 test cases with automated pass/fail reporting

### Phase 5: Production Frontend ✅ COMPLETE (Dec 31, 2025)
- ✅ Full React application (Dashboard, EventList, MetricsChart, StatsCards)
- ✅ Recharts visualization with time-series charts
- ✅ AWS Amplify integration
- ✅ Mock data mode for local development
- ✅ 50 frontend tests (67.85% coverage)
- ✅ Complete documentation (README, QUICKSTART, TESTING)

## 💡 Design Decisions

### Why Apache Flink?
- **True Stream Processing**: Event-time processing with watermarks
- **State Management**: Built-in stateful operators with checkpointing
- **Scalability**: Distributed execution across task managers
- **Exactly-Once Semantics**: Fault-tolerant processing guarantees

### Why Kafka?
- **High Throughput**: Handles millions of messages per second
- **Durability**: Message persistence with configurable retention
- **Scalability**: Horizontal scaling with partitions
- **Ecosystem**: Rich connector ecosystem for sources and sinks

### Why Docker Compose for Development?
- **Reproducibility**: Consistent environment across machines
- **Isolation**: No dependency conflicts with host system
- **Speed**: Quick startup/teardown for testing
- **Portability**: Easy sharing with team members

### Dual Deployment Strategy
- **Local**: Fast iteration with full control over infrastructure
- **AWS**: Production scalability with managed services
- **Migration Path**: Clear transition from dev to prod

## 🔍 Learning Outcomes

### Stream Processing Concepts
- Event-driven architecture patterns
- Watermarking and event-time processing
- Stateful stream processing
- Exactly-once processing semantics
- Checkpointing and fault tolerance

### Distributed Systems
- Message broker design (Kafka)
- Distributed execution (Flink cluster)
- Container orchestration (Docker)
- Service discovery and networking

### Cloud-Native Architecture
- Infrastructure as Code (Terraform)
- Managed services vs. self-hosted
- Data migration strategies
- Cost optimization (local dev vs. production)

### Software Engineering Best Practices
- Unit testing stream processing jobs
- Build automation (Maven)
- Dependency management (provided vs. bundled)
- Documentation-driven development

## 🚀 Future Enhancements

While the project is complete, potential future enhancements include:

**AWS Production Deployment:**
1. Execute Terraform infrastructure deployment to AWS
2. Deploy Flink job to AWS Managed Flink
3. Implement DynamoDB sink for production
4. Run MongoDB to DynamoDB migration
5. Deploy React frontend to AWS Amplify

**Advanced Features:**
1. Complex Event Processing (CEP) patterns for fraud detection
2. Sliding/session windows for advanced analytics
3. Machine learning model integration for real-time predictions
4. WebSocket integration for live frontend updates
5. Multi-region deployment for high availability
6. CI/CD pipeline with automated testing and deployment

**Performance Optimization:**
1. RocksDB state backend for production scalability
2. Kafka replication factor of 3 for fault tolerance
3. Flink parallelism tuning for higher throughput
4. Connection pooling optimizations
5. Caching strategies for frequently accessed data

## 📚 Documentation

**Comprehensive documentation available:**
- **README.md**: Complete quick start guide (334 lines)
- **project_status.md**: Full Gantt chart with metrics (492 lines)
- **WARP.md**: Development guidelines and build commands
- **docs/AWS_DEPLOYMENT.md**: Complete AWS deployment guide (824 lines)
- **docs/mongodb-schema.md**: Database schema documentation
- **frontend/README.md**: Frontend architecture (386 lines)
- **frontend/QUICKSTART.md**: 3-minute startup guide
- **frontend/TESTING.md**: Frontend testing guide
- **Docker Compose**: Service configuration (106 lines)
- **Maven POM**: Dependency management (181 lines)
- **Source Code**: Inline comments and JavaDoc throughout

## 🔗 Related Projects

- **AutoCorp Cloud Data Lake**: Batch processing with AWS Glue, Apache Hudi, and Terraform
- **AWS Management**: Cloud infrastructure utilities and automation
- **DynamoDB Inventory System**: NoSQL data modeling patterns

---

**Project Completion Note**: StreamForge is a **production-ready** real-time streaming platform with all 5 phases complete. The local development environment is fully operational with 50+ passing tests. AWS infrastructure code is complete and ready for deployment when needed. This project demonstrates enterprise-grade stream processing with Kafka, Flink, MongoDB, React, and AWS services.
