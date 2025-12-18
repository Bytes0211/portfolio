# StreamForge Real-Time Data Streaming Platform

**Last Updated:** December 18, 2025  
**Project Status:** Phase 1 Complete (40% overall)  
**Duration:** 2 weeks (Dec 4 - Dec 18, 2025)

A real-time data streaming and processing platform demonstrating modern stream processing architecture with Apache Kafka, Apache Flink, and cloud-native deployment patterns. This project showcases enterprise-scale event-driven architecture with dual deployment models (local and AWS production).

## 🎯 Project Overview

StreamForge is a comprehensive streaming data platform that implements real-time data ingestion, transformation, and storage using industry-standard tools. The system demonstrates end-to-end stream processing capabilities with both local development infrastructure and production-ready AWS deployment.

**Tech Stack**: Apache Kafka, Apache Flink (Java), MongoDB, Docker, Maven, AWS (DynamoDB, Amplify), Terraform  
**Architecture**: Event-driven streaming with dual deployment models  
**Processing Engine**: Apache Flink 1.18.0 with Java 11  
**Messaging**: Apache Kafka 3.5.1 (Confluent Platform 7.5.0)  
**Build System**: Maven with Shade plugin for JAR packaging  
**Testing**: JUnit with embedded test harnesses  
**Project Status**: Phase 1 Complete (40% overall)

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

**2. AWS Production Environment (Planned)**
```
External Sources → Kafka/Kinesis
                     ↓
               AWS Managed Flink
                     ↓
               Stream Processing
                     ↓
               DynamoDB
                     ↓
           React Frontend (AWS Amplify)
```

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

**StreamProcessor.java** - Main entry point for stream processing:
```java
public class StreamProcessor {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Configure Kafka source
        KafkaSource<String> source = KafkaSource.<String>builder()
            .setBootstrapServers("kafka:29092")
            .setTopics("streamforge-input")
            .setGroupId("streamforge-consumer-group")
            .setValueOnlyDeserializer(new SimpleStringSchema())
            .build();
        
        // Stream processing pipeline
        DataStream<String> stream = env.fromSource(source, 
            WatermarkStrategy.noWatermarks(), "Kafka Source");
        
        // Apply transformations
        DataStream<String> processed = stream
            .map(value -> value.toUpperCase());
        
        // Sink to MongoDB
        processed.addSink(new MongoDBSink());
        
        env.execute("StreamForge Processor");
    }
}
```

**Key Features:**
- Kafka integration with consumer group management
- Custom sink implementation for MongoDB
- Filesystem state backend with checkpointing at `/tmp/flink-checkpoints`
- Extensible transformation pipeline (map/filter/window operations)

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

Comprehensive unit tests for all components:

**StreamProcessorTest.java:**
- Validates Kafka source configuration
- Tests transformation logic
- Verifies sink integration

**MongoDBSinkTest.java:**
- Connection lifecycle testing
- Document insertion validation
- Error handling scenarios

**MongoDBSchemaTest.java:**
- Schema validation
- Data structure verification
- Index configuration testing

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
├── docker/                       # Container orchestration
│   └── docker-compose.yml       # 5 services (Kafka, Flink, MongoDB)
├── flink-jobs/                  # Stream processing logic
│   ├── pom.xml                  # Maven configuration
│   ├── src/
│   │   ├── main/java/com/streamforge/
│   │   │   ├── StreamProcessor.java    # Main entry point
│   │   │   └── MongoDBSink.java        # Custom sink
│   │   └── test/java/com/streamforge/
│   │       ├── StreamProcessorTest.java
│   │       ├── MongoDBSinkTest.java
│   │       └── MongoDBSchemaTest.java
│   └── target/
│       └── flink-jobs-1.0-SNAPSHOT.jar  # Fat JAR output
├── frontend/                    # React application (planned)
│   └── streamforge-ui/
├── terraform/                   # AWS IaC (planned)
│   ├── dynamodb.tf
│   ├── amplify.tf
│   └── variables.tf
├── scripts/                     # Utilities
│   └── mongodb-to-dynamodb/    # Migration scripts
└── docs/                        # Documentation
```

## 🔧 Configuration Details

### Kafka Configuration
- **Topic**: `streamforge-input`
- **Consumer Group**: `streamforge-consumer-group`
- **Bootstrap Servers**: `kafka:29092` (internal), `localhost:9092` (external)
- **Partitioning Strategy**: TBD (Phase 2)

### MongoDB Configuration
- **Connection String**: `mongodb://admin:password@mongodb:27017`
- **Database**: `streamforge`
- **Collection**: `processed_data`
- **Credentials**: admin/password (dev environment)
- **Schema Design**: Flexible document structure (Phase 2)

### Flink Configuration
- **Version**: 1.18.0
- **Java**: 11
- **State Backend**: Filesystem
- **Checkpoint Directory**: `/tmp/flink-checkpoints`
- **Parallelism**: Default (configurable per job)

## 🛣️ Development Roadmap

### Phase 1: Infrastructure Setup ✅ (40% Complete)
- ✅ Docker Compose environment
- ✅ Kafka cluster
- ✅ Flink cluster (JobManager + TaskManager)
- ✅ MongoDB integration
- ✅ Basic StreamProcessor implementation
- ✅ Custom MongoDBSink
- ✅ Unit tests

### Phase 2: Stream Processing Enhancement (In Progress)
- [ ] Kafka topic configuration and partitioning
- [ ] MongoDB schema design and indexing
- [ ] Advanced transformations (windowing, aggregations)
- [ ] Stateful operations (keyed state, operator state)
- [ ] Complex event processing patterns

### Phase 3: AWS Deployment (Planned)
- [ ] Terraform infrastructure modules
- [ ] DynamoDB table design
- [ ] DynamoDB sink implementation
- [ ] MongoDB to DynamoDB migration scripts
- [ ] AWS Managed Flink job deployment

### Phase 4: Frontend & Visualization (Planned)
- [ ] React chatbot UI
- [ ] AWS Amplify hosting
- [ ] Real-time data visualization
- [ ] REST API for data queries
- [ ] User authentication

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

## 🚀 Next Steps

**Immediate (Phase 2):**
1. Implement windowed aggregations (tumbling, sliding windows)
2. Add stateful operations (keyed state for session tracking)
3. Design MongoDB schema with indexing strategy
4. Configure Kafka topics with replication factor

**Mid-Term (Phase 3):**
1. Complete Terraform modules for AWS deployment
2. Implement DynamoDB sink with optimistic concurrency
3. Create migration scripts with validation
4. Set up CI/CD pipeline for Flink job deployment

**Long-Term (Phase 4):**
1. Build React chatbot UI with WebSocket updates
2. Integrate AWS Amplify for hosting and auth
3. Add real-time dashboards with data visualization
4. Implement complex event processing (CEP) patterns

## 📚 Documentation

- **README.md**: Quick start and project overview
- **WARP.md**: Development guidelines and build commands
- **Docker Compose**: Service configuration and networking
- **Maven POM**: Dependency management and build configuration
- **Source Code**: Inline comments and JavaDoc

## 🔗 Related Projects

- **AutoCorp Cloud Data Lake**: Batch processing with AWS Glue and Hudi
- **AWS Management**: Cloud infrastructure utilities
- **DynamoDB Inventory System**: NoSQL data modeling patterns

---

**Note**: This project is in active development. Stream processing logic is currently placeholder implementation (`.toUpperCase()`) and will be replaced with domain-specific transformation logic in Phase 2.
