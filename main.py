import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

# Uncomment to get the first feature
# -------------------------------------------------------------done parsing the first part i.e. medicine name
# data = ""
# body = open('./file.html').read().replace('\n','').replace('\r','')
# stored_data = open('sample.html',"w")
# divs = Selector(text=body).xpath("//html/body/div/div["'"++"'"]/ul/li/a/text()")
# for index in range(len(divs)):
#     stored_data.writelines(divs[index].extract()+",")
# -----------------------------------------------------------------------------------------------------------

# Uncomment to get second feature
# -------------------------------------------------------------done parsing the second part i.e. medicine name and mg
# body = open('./file.html').read().replace('\n','').replace('\r','')
# stored_data = open('sample2.html',"w")
# divs = Selector(text=body).xpath("/html/body/div/div[1]/ul/li/div/div/ul/li["'"++"'"]/a/text()")
# for index in range(len(divs)):
#      stored_data.writelines(divs[index].extract()+",".strip())
  
# -------------------------------------------------------------------------------------------------------------------
   
# TODO Mix those two loops to get the appropriate data - Easy Part