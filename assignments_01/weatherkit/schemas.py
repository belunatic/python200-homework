from pydantic import BaseModel, Field, model_validator

class HourlyBlock(BaseModel):
    time:list[str]
    temperature_2m:list[float]
    precipitation:list[float]

class WeatherResponse(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone:str
    hourly: HourlyBlock

    @model_validator(mode='after')
    def check_same_length(self):
        ''' Same length from all the three lists'''
        if not (len(self.hourly.time) == len(self.hourly.temperature_2m) == len(self.hourly.precipitation)):
            raise ValueError("All hourly lists must have the same length")
        return self