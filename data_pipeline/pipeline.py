from data_pipeline.pipeline_manager import DataPipeline
from utils.ELTL import OpenWeatherCurrentAirPollution, OpenWeatherCurrentWeather

if __name__ == '__main__':
    air_pollution_manager = DataPipeline(OpenWeatherCurrentAirPollution())
    air_pollution_manager.run()

    weather_manager = DataPipeline(OpenWeatherCurrentWeather())
    weather_manager.run()
