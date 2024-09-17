import sys
print("Python path:", sys.path)
sys.path.append('/app')

from data_pipeline.pipeline_manager import DataPipeline
from utils.ELTL import OpenWeatherCity

if __name__ == '__main__':
    city_manager = DataPipeline(OpenWeatherCity())
    city_manager.run()
