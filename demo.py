from black_friday.logger import logging
from black_friday.exception import USvisaException
import sys

from black_friday.pipeline.training_pipeline import TrainPipeline


pipeline = TrainPipeline()
pipeline.run_pipeline()