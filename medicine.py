import scrapy

from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()
start_urls = [""]
class Medicines(Base):
    __tablename__ = 'medicines'
    id = Column(Integer,primary_key=True)
    medicine_name = Column(String,unique=True)
    chemical_formula_id = Column(Integer)
    ForeignKeyConstraint(['chemical_formula_id'], ['ChecmicalCompositions.id'])

    def __repr__(self):
        return "<Medicines(medicine_name='%s',chemical_formula_id='%s')>" % (
            self.medicine_name,self.chemical_formula_id)



class MedicineVariants(Base):
    __tablename__ = 'medicine_variants'
    id = Column(Integer,primary_key=True)
    variant_name = Column(String)
    variant_link = Column(String)
    medicine_id = Column(Integer)
    ForeignKeyConstraint(['medicine_id'], ['medicines.id'])

    def __repr__(self):
        return "<MedicineVariants(variant_name='%s',variant_link='%s',medicine_id='%s')>" % (
            self.variant_name,self.variant_link,self.medicine_id)

class Medicine(scrapy.Spider):
    name = 'Medicine'
    start_urls = ["http://netmeds.com/prescriptions"]
    body = open('./file.html').read().replace('\n','').replace('\r','')
    def parse(self,response):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()

        divs = Selector(text=self.body).xpath('//html/body/div/div')
        for div in divs:
            medicine_name = div.xpath("./ul/li/a/text()").extract_first()
            var_medicine_name = medicine_name.encode('ascii','ignore')
            medicine = Medicines(medicine_name=var_medicine_name, chemical_formula_id="-1")
            session.add(medicine)
            session.commit()
            lis = div.xpath("./ul/li/div/div/ul/li")
            for li in lis:
                medicine_variant_name = li.xpath("./a/text()").extract_first()
                medicine_variant_link = li.xpath("./a/@href").extract_first()
                med_id = session.query(Medicines).filter_by(medicine_name=medicine_name).first()
                medicine_variant = MedicineVariants(variant_name=medicine_variant_name,variant_link=medicine_variant_link,medicine_id=med_id.id)
                session.add(medicine_variant)
                session.commit()
                
        # url_list = session.query(MedicineVariants).all()
        # for everyUrl in url_list.variant_link:
        #     start_urls += "http://netmeds.com"+everyUrl