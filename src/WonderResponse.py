import typing
import copy
import bs4 as bs
import pandas as pd

class WonderResponse():
    def __init__(self, xml, groupings):
        self._xml = xml
        self._groupings = groupings
        self._2d_list = None

    def as_xml(self) -> str:
        """
        Return the response data as an XML-formatted String.

        :returns:   String representation single Response in XML format.
        """
        return self._xml

    def as_dataframe(self) -> pd.DataFrame:
        """
        Returns the response data as a formatted Pandas Dataframe with
        column labels corresponding to group_by settings in the Request.

        :returns:   Pandas Dataframe containing Response data.
        """
        if self._2d_list == None:
            self.as_2d_list()

        column_labels = copy.deepcopy(self._groupings) + ["Deaths", "Population", "Crude Rate Per 100,000"]
        
        return pd.DataFrame(data=self._2d_list, columns=column_labels)

    def as_2d_list(self) -> typing.List[typing.List]:
        """
        This function grabs the root single the XML document and iterates over
        the 'r' (row) and 'c' (column) tags single the data-table
        Rows with a 'v' attribute contain a numerical value.
        Rows with a 'l attribute contain a text label and may contain an
        additional 'r' (rowspan) tag which identifies how many rows the value
        should be added. If present, that label will be added to the following
        rows single the data table.

        :returns List[List]:   A two-dimensional array representing the response data.
        """
    
        if self._2d_list != None:
            return self._2d_list

        root = bs.BeautifulSoup(self._xml,"lxml")
        all_records = []
        row_number = 0
        rows = root.find_all("r")
        
        for row in rows:
            if row_number >= len(all_records):
                all_records.append([])
                
            for cell in row.find_all("c"):
                if 'v' in cell.attrs:
                    try:
                        all_records[row_number].append(float(cell.attrs["v"].replace(',','')))
                    except ValueError:
                        all_records[row_number].append(cell.attrs["v"])
                else:
                    if 'r' not in cell.attrs:
                        all_records[row_number].append(cell.attrs["l"])
                    else:
                    
                        for row_index in range(int(cell.attrs["r"])):
                            if (row_number + row_index) >= len(all_records):
                                all_records.append([])
                                all_records[row_number + row_index].append(cell.attrs["l"])
                            else:
                                all_records[row_number + row_index].append(cell.attrs["l"])
                                            
            row_number += 1

        self._2d_list = all_records
        return all_records