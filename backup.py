import pdb; 
import scrapy
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
import MySQLdb

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db', echo=True)
base = declarative_base()
base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

pdb.set_trace()

class MedicineTypes(base):
    __tablename__ = 'medicine_list'
    id = Column(Integer,primary_key=True)
    medicine_name = Column(String,unique=True)
    medicine_variations = Column(String)
    medicine_variation_links = Column(String)
    
    def __repr__(self):
         return "<MedicineTypes(medicine_name='%s',medicine_variations='%s', medicine_variation_links='%s')>" % (
             self.medicine_name, self.medicine_variations,self.medicine_variation_links)

class MedicineType(scrapy.Spider):
    name = "MedicineTypes"
    start_urls=['http://www.netmeds.com/prescriptions/alpha/all']
    
    def parse(self, response):
        body = open('./file.html').read().replace('\n','').replace('\r','')
        divs = Selector(text=body).xpath('//html/body/div/div')
        
        # base.metadata.create_all(engine)
        # Session = sessionmaker(bind=engine)
        # session = Session()

        for div in divs:
            title = div.xpath("./ul/li/a/text()").extract_first()
            desc = []
            desc_links = []
            lis = div.xpath("./ul/li/div/div/ul/li")
            for li in lis:
                desc.append(li.xpath("./a/text()").extract_first())
                desc_links.append(li.xpath("./a/@href").extract_first())
            
            var_title = title.encode('ascii','ignore')
            var_desc = ''
            var_desc_links = ''
            
            for des in desc:
                var_desc+=des+','
            for des_link in desc_links:
                var_desc_links+=des_link+','

            var_desc = var_desc[:-1]
            var_desc_links = var_desc_links[:-1]
            
            medicine = MedicineTypes(medicine_name=var_title,medicine_variations=var_desc,medicine_variation_links=var_desc_links)
            # print(medicine)
            session.add(medicine)
        session.commit()
        abc = session.query(MedicineTypes).filter_by(medicine_name="AB NUT").first()
        print(abc.id)

class MedicineDetails(base):
    __tablename__ = 'medicine_details'
    id = Column(Integer,primary_key=True)
    name = Column(String,unique=True)
    price = Column(String)
    manufacturer = Column(String)
    manufacturer_link = Column(String)
    substitute_count = Column(String)
    substitute_data = Column(String)
    substitute_data_links = Column(String)

    def __repr__(self):
        return "<MedicineDetails(name='%s',price='%s',manufacturer='%s',manufacturer_link='%s',substitute_count='%s',substitute_data='%s',substitute_data_links='%s')>" % (
            self.name,self.price,self.manufacturer,self.manufacturer_link,self.substitute_count,self.substitute_data,self.substitute_data_links)

class MedicineDetail(scrapy.Spider):
    name = 'MedicineDetail'
    start_urls = ["http://www.netmeds.com/prescriptions/aricep-sr/23mg"]
    body = open("netmed1.html","r").read()

    base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    def parse(self, response):
        name = Selector(text=self.body).xpath('//*[@id="topBrandname"]/text()').extract_first()
        price = Selector(text=self.body).xpath('//*[@id="lblBmrp"]/text()').extract_first()
        manufacturer = Selector(text=self.body).xpath('//*[@id="BManu"]/text()').extract_first()
        manufacturer_link = Selector(text=self.body).xpath('//*[@id="BManu"]/@href').extract_first()
        substitute_count = Selector(text=self.body).xpath('//*[@id="topBSubscount"]/text()').extract_first()
        # print(name+" : "+price+" : "+manufacturer+" : "+manufacturer_link+" : "+substitute_count) 
        substitutes_data = []
        substitutes_data_links = []
        if(substitute_count!='No'):
            substitute = Selector(text=self.body).xpath('//*[@id="divforsubstitutues"]/table/tbody/tr')
            for sub in substitute:
                substitutes_data.append(sub.xpath('./td[2]/div/a/h4/text()').extract_first())
                substitutes_data_links.append(sub.xpath('./td[2]/div/a/@href').extract_first())
            substitutes_data = substitutes_data[1:]
            substitutes_data_links = substitutes_data_links[1:]
        var_sub=""
        var_sub_links=""
        for sub_data in substitutes_data:
            var_sub += sub_data+","
        for sub_data_links in substitutes_data_links:
            var_sub_links = sub_data_links+","
        var_sub = var_sub[:-1]
        var_sub_links = var_sub_links[:-1]
        medicine_details = MedicineDetails(name=name,price=price,manufacturer=manufacturer,manufacturer_link=manufacturer_link,substitute_count=substitute_count,substitute_data=var_sub,substitute_data_links=var_sub_links)
        self.session.add(medicine_details)
        self.session.commit()
        
        method_name = 'parse'
        med_type = MedicineType()
        method = getattr(med_type,method_name)
        method(response)
        