"""Contains functionality related to Weather"""
import logging


logger = logging.getLogger(__name__)


class Weather:
    """Defines the Weather model"""

    def __init__(self):
        """Creates the weather model"""
        self.temperature = 70.0
        self.status = "sunny"

        #
        #
        # Process incoming weather messages. Set the temperature and status.
        #
        #
        
    def process_message(self, message):
        """Handles incoming weather data"""
        try:
            value = message.value()
            self.temperature = value['temperature']
            self.status = value['status']
        except Exception as e:
            logger.info(f"Error processing weather data: {e}")
