from sqlalchemy import Column, Integer, String, ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()
class ChemicalCompositions(Base):
    __tablename__ = "chemical_compositions"

    id = Column(Integer,primary_key=True)
    formula = Column(String,unique=True)
    def __repr__(self):
        return "<ChemicalCompositions(formula='%s')>" % (self.formula)

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
