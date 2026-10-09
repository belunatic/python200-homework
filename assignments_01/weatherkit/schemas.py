from pydantic import BaseModel, Field, model_validator

class HourlyBlock(BaseModel):
    ''' model for the daily observation
    
        Attribute:
            time: the timestamp of the observation
            temperature_2m: the temperature recorded at the given timestamp
            precipitation: precipitation recorded at the given timestamp
    '''
    time:list[str]
    temperature_2m:list[float]
    precipitation:list[float]


class WeatherResponse(BaseModel):
    ''' model for the daily observation
        
            Attribute:
                latitude: location in latitude
                longitude: location in longitude
                timezone: the timezone of the location
                elevation: location elevation
                hourly: daily observation records
        '''
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone:str
    elevation: float
    hourly: HourlyBlock

    @model_validator(mode='after')
    def check_same_length(self):
        ''' Same length from all the three lists'''
        if not (len(self.hourly.time) == len(self.hourly.temperature_2m) == len(self.hourly.precipitation)):
            raise ValueError("All hourly lists must have the same length")
        return self