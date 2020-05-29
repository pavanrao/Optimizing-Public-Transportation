"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)

BROKER_URL = "PLAINTEXT://localhost:9092"
SCHEMA_REGISTRY_URL = "http://localhost:8081"


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        #
        #
        #  Configure the broker properties below. Make sure to reference the project README
        # and use the Host URL for Kafka and Schema Registry!
        #
        #
        self.broker_properties = {
            "bootstrap.servers": BROKER_URL,
            "schema.registry.url": SCHEMA_REGISTRY_URL,
        }

        self.admin_client = AdminClient({"bootstrap.servers": BROKER_URL})

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        #  Configure the AvroProducer
        # self.producer = AvroProducer(
        # )
        self.producer = AvroProducer(self.broker_properties,
                                    default_key_schema=self.key_schema, 
                                    default_value_schema=self.value_schema)


    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
        #
        #
        #  Write code that creates the topic for this producer if it does not already exist on
        # the Kafka Broker.
        #
        #
        #logger.info("topic creation kafka integration incomplete - skipping")

        topic_metadata = self.admin_client.list_topics(timeout=5)
        topics = list(t.topic for t in iter(topic_metadata.topics.values()))
        if self.topic_name in topics:
            logger.info(f"{self.topic_name} already exists.")
            return
        
        self.client = AdminClient({'bootstrap.servers':  BROKER_URL})

        futures = self.client.create_topics(
            [NewTopic(
                topic=self.topic_name,
                replication_factor=self.num_replicas,
                num_partitions=self.num_partitions),
            ]
        )
        
        for topic, future in futures.items():
            try:
                future.result()
                logger.info(f"{self.topic_name} is created")
            except Exception as e:
                logger.error(f"{self.topic_name} is not created: {e}")
  

    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        #
        #
        #  Write cleanup code for the Producer here
        #
        #
        logger.info("producer close  - flush producer")
        if self.producer is not None:
            self.producer.flush()

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
