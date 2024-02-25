from csv import reader
from datetime import datetime
from typing import List

from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename

    def startReading(self, *args, **kwargs):
        # Open files
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        # read files
        self.accelerometer_reader = reader(self.accelerometer_file)
        self.gps_reader = reader(self.gps_file)

        # Skip headers
        self.accelerometer_file.seek(1)
        self.gps_file.seek(1)

    def stopReading(self, *args, **kwargs):
        # Will never work because we restart files after reading the end
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()

    def read(self) -> List[AggregatedData]:
        aggregated_data_list = []
        try:
            # Create a batch of 5 rows with the same timestamp
            batch_timestamp = datetime.now()
            # For each row in the batch
            for _ in range(7):
                accelerometer_data = next(self.accelerometer_reader)
                gps_data = next(self.gps_reader)

                accelerometer = Accelerometer(*map(int, accelerometer_data))
                gps = Gps(*map(float, gps_data))
                aggregated_data_list.append(AggregatedData(accelerometer, gps, batch_timestamp))

        # After the end of file start again
        except StopIteration:
            # Skip headers
            self.accelerometer_file.seek(1)
            self.gps_file.seek(1)
            # Start again reading
            return self.read()

        # Other exceptions
        except Exception as e:
            print(f"An error occurred while reading data: {e}")

        return aggregated_data_list
