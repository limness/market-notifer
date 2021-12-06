
import xlsxwriter
import random


class ExcelManager:
    """A class for Excel management"""

    def _generate_excel_graphic(self):
        """Method for generating a graph in xls format"""
        # Entry and exit points
        data_start_loc = [0, 0]
        data_end_loc = [data_start_loc[0] + len(self.y_pos), 0]
        
        # A chart requires data to reference data inside excel
        self.worksheet.write_column(*data_start_loc, data=self.y_pos)
        # The chart needs to explicitly reference data
        self.chart.add_series({
            'values': [self.worksheet.name] + data_start_loc + data_end_loc,
            'name': self.token,
        })
        self.worksheet.insert_chart(
            'B1',
            self.chart,
            {
                'x_scale': 3,
                'y_scale': 2
            }
        )

    def _create_excel_graphic(self):
        """Method for generating a graph in xls format"""
        # Creating a chart
        self.chart = self.workbook.add_chart({'type': 'line'})
        self.chart.set_title({'name': f'Суточное изменение цены {self.token}'})
        self.chart.set_x_axis({'name': 'Период'})
        self.chart.set_y_axis({'name': 'Цена'})

    def __init__(self, token, y_pos):
        self.workbook = xlsxwriter.Workbook('charts.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.y_pos = y_pos
        self.token = token

        self._create_excel_graphic()
        self._generate_excel_graphic()

        # Close and save xls
        self.workbook.close()
