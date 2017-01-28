import scrapy
# from models import MedicineVariants, Medicines, ChemicalCompositions
from medicine import Medicines, MedicineVariants
from scrapy.selector import Selector
from sqlalchemy import Column, Integer, String, ForeignKeyConstraint

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()

class ChemicalCompositions(Base):
    __tablename__ = "chemical_compositions"

    id = Column(Integer,primary_key=True)
    formula = Column(String,unique=True)
    def __repr__(self):
        return "<ChemicalCompositions(formula='%s')>" % (self.formula)

class ChemicalComposition(scrapy.Spider):

    name = 'ChemicalComposition'
    # start_urls = ['http://www.netmeds.com/prescriptions']
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    def start_requests(self):
        

        start_urls = []
        med_user = self.session.query(MedicineVariants).all()
        for eachData in med_user:
            start_urls.append("http://www.netmeds.com"+eachData.variant_link)
        # for each in start_urls:
        #     print each
        # import pdb; pdb.set_trace()
        # start_urls = [
        #     "http://www.netmeds.com/prescriptions/a-phyl/100mg"
        # ]
        for each_url in start_urls:
            yield scrapy.Request(url=each_url, callback=self.parse)
        #yield scrapy.Request(url="http://www.netmeds.com/prescriptions",callback=self.parse)
        # engine = create_engine('sqlite:///data.db', echo=True)
        # base = declarative_base()
        # base.metadata.create_all(engine)
        # Session = sessionmaker(bind=engine)
        # session = Session()
    def parse(self,response):
        # body = open("netmed1.html","r").read()
        # medicine_variant_name = Selector(text=body).xpath('//*[@id="topBrandname"]/text()').extract_first()
        medicine_variant_name = response.xpath('//*[@id="topBrandname"]/text()').extract_first()
        var_mvn = medicine_variant_name.encode('ascii','ignore')
        # chem_comp = Selector(text=body).xpath('//*[@id="topBGeneric"]/text()').extract_first()
        chem_comp = response.xpath('//*[@id="topBGeneric"]/text()').extract_first()
        var_cc = chem_comp.encode('ascii','ignore')
        var_session = self.session.query(ChemicalCompositions).filter_by(formula=var_cc).first()
        print(var_session)
        if var_session is not None:
            print 'hello'
            cc_temp = self.session.query(ChemicalCompositions).filter_by(formula=var_cc).first()
            medicine_variant_obj = self.session.query(MedicineVariants).filter_by(variant_name=var_mvn).first()
            obj = self.session.query(Medicines).filter_by(id=medicine_variant_obj.medicine_id).first()
            print obj
        
            obj.chemical_formula_id = int(cc_temp.id)
            self.session.commit()
        else:
            print 'dollo'
            abc = self.session.query(ChemicalCompositions).filter_by(formula=var_cc)
            print abc
            cct = ChemicalCompositions(formula=var_cc)
            self.session.add(cct)
            self.session.commit()
            print var_cc
            cc_temp = self.session.query(ChemicalCompositions).filter_by(formula=var_cc).first()
            medicine_variant_obj = self.session.query(MedicineVariants).filter_by(variant_name=var_mvn).first()
            obj = self.session.query(Medicines).filter_by(id=medicine_variant_obj.medicine_id).first()
            print obj
        
            obj.chemical_formula_id = int(cc_temp.id)
            self.session.commit()
