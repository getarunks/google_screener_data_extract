"""

This script extracts compID and compFormatted required to parse business-standard.com.

How-To
=======
Download the http://www.business-standard.com/api-handler/article/get-company-json.

Format the get-company-json using website https://jsonformatter.curiousconcept.com/#

Then copy paste the data in following format
{
"searchresults" :
---copy-paste the json---
}

Now run this script. It wil generate bussiness-std.csv

"""
import os, re, sys, time, datetime, copy, calendar
import pandas
import json

stockList = []
class GoogleStockDataExtract(object):
    """
        Target url need to be rotate and join separately.
    """
    def __init__(self):
        """

        """
        ## parameters
        self.saved_json_file = r'data.json'
#        self.saved_json_file = r'test.json'
        self.target_tag = 'searchresults' #use to identify the json data needed

        ## Result dataframe
        self.result_google_ext_df = pandas.DataFrame()

    def form_full_url(self):
        """ Form the url"""
        self.target_full_url = self.target_url_start + self.temp_url_mid + self.target_url_end

    def retrieve_stockdata(self):
        """ Retrieve the json file based on the self.target_full_url"""
        ds = WebJsonRetrieval()
        ds.set_url(self.target_full_url)
        ds.download_json() # default r'c:\data\temptryyql.json'

    def get_json_obj_fr_file(self):
        """ Return the json object from the .json file download.
            Returns:
                (json obj): modified json object fr file.
        """

        with open(self.saved_json_file) as f:
            data_str = f.read()
        # replace all the / then save back the file
        update_str = re.sub(r"\\",'',data_str)
#	print update_str
        update_str = re.sub(r"<div class=",':',update_str)
#	print update_str
        update_str = re.sub(r"stock_symb",',"stock_symb',update_str)
#	print update_str
	update_str = re.sub(r"stock_name",',"stock_name',update_str)
#	print update_str
        update_str = re.sub(r"</div>:",'',update_str)
#	print update_str
        update_str = re.sub(r"\"clrBoth\"></div>\"",'"',update_str)
#	print update_str
	update_str = re.sub(r">",':"',update_str)
#	print update_str
        json_raw_data = json.loads(update_str)
        return json_raw_data

    def convert_json_to_df(self):
        """ Convert the retrieved data to dataframe
            Returns:
                (Dataframe obj): df formed from the json extact.
        """
        json_raw_data = self.get_json_obj_fr_file()
#	print json_raw_data

        new_data_list = []
        for n in json_raw_data['searchresults']:
            stockName = n['compFormatted']+'-'+n['compId']
            temp_stock_dict={'SYMBOL':n['compId'],
                             'CompanyName':n['stock_name'],
                             'compId' :n['compId'],
                             'compFormat' :n['compFormatted'],
			     'linkId' :stockName,
                            }
#            for col_dict in n['columns']:
#                if not col_dict['value'] == '-':
#                    temp_stock_dict[col_dict['field']] = col_dict['value']
#            for col_dict in n['columns']:
#                 temp_stock_dict[col_dict['field']] = col_dict['value']

#            stockList.append(stockName)
            new_data_list.append(temp_stock_dict)

#        print stockList
        return pandas.DataFrame(new_data_list)


    def retrieve_all_stock_data(self):
        """ Retreive all the stock data. Iterate all the target_url_mid1 """
        temp_data_df = self.convert_json_to_df()
        if len(self.result_google_ext_df) == 0:
            self.result_google_ext_df = temp_data_df
        else:
            self.result_google_ext_df =  pandas.merge(self.result_google_ext_df, temp_data_df, on=['SYMBOL','CompanyName'])


if __name__ == '__main__':

    choice  = 2

    if choice == 2:
        hh = GoogleStockDataExtract()
        hh.retrieve_all_stock_data()

#        print hh.result_google_ext_df
        hh.result_google_ext_df.to_csv(r'bussiness-std.csv', index =False)

