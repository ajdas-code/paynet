######################################
# Models for RivPay ( Consumers App)
####################################
from app import db
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
import ulid
import datetime
from ..common import base

class BaseModel:
    @staticmethod
    def idGenerator( ):
        return str(ulid.new())
    @staticmethod
    def symmetric_key ():
        # on production read from the env variable
        return "ResearchInValue"
    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()


class Account(BaseModel,db.Model):
    __tablename__ = 'account'
    __table_args__ = (
        PrimaryKeyConstraint('id',),
    )


    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    #Attribute cols
    #
    # Uniquely identify an account
    #
    accountkey = db.Column(db.String(32), nullable = False, unique = True, default= BaseModel.idGenerator)
    #
    # Account holder Identity
    #
    #name
    name = db.Column(db.String(100),nullable = False) #1
    #email
    email = db.Column(db.String(50),nullable = False, unique = True)
    #phone
    phone = db.Column(db.String(24), nullable = False, unique = True)
    #address
    address = db.Column(db.String(256),nullable = False) #1 - email
    # date of birth
    dob = db.Column(db.DateTime,nullable = False) #1
    #Driving licence/state id number
    dl = db.Column(db.String(12),nullable = False, unique = True) #1
    #Driving license/state id state
    dlState = db.Column(db.String(2), default=0)  # 0
    #ssn number
    ssn = db.Column(db.String(12),nullable = False, unique = True) #1
    #
    # Access details
    #
    login = db.Column(db.String(12), default = "account") #2
    password = db.Column(db.String(12), default = "password") #2
    #
    #compliance
    #
    kyc = db.Column(db.Boolean, default = False) #0
    #
    # Foreign key - one to many relations
    wallet = db.relationship('Wallet', backref='account', lazy=True, cascade='all, delete, delete-orphan')
    contact = db.relationship('Contact', backref='account', lazy=True, cascade='all, delete, delete-orphan')
    #
    # Status of the account
    status = db.Column(db.Enum(AccountStatus), nullable = False, default= AccountStatus.Cr  )

    ##many to many
    #wallet = db.relationship('Account', secondary = 'transaction', back_populates = 'account'
                              

    def __init__(self, name="tester", address="101 2nd Street, San Francisco, CA 94105",
                 dob="1/1/1970", dl="D1234567", dlstate = "CA",ssn="999999999",
                 email="joker@acme.com", phone="+91.96405.556467", status = AccountStatus.Cr):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.dob = dob
        self.dl = dl
        self.dlState = dlstate
        self.ssn = ssn
        self.kyc = False
        self.login = "account"
        self.password = "password"
        self.status = status

     def __repr__(self):
        return (f"<Account: accountkey={self.accountkey}, name={self.name}, "
                f"age={self.age}, address={self.address}, dob={self.dob}, DL={self.dl}, "
                f"SSN={self.ssn}, Kyc={self.kyc}, Position={self.position}, login={self.login}>")




class Wallet(BaseModel,db.Model):
    __tablename__ = 'wallet'
    __table_args__ = (
        PrimaryKeyConstraint('id',),
    )


    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    #application attribute
    walletkey = db.Column(db.String(32), nullable = False, unique = True, default= BaseModel.idGenerator)    
    balance = db.Column(db.Integer, default = 0)
    available_balance = db.Column(db.Integer, default = 0)
    pending_balance = db.Column(db.Integer, default = 0)
    priv_key = db.Column(db.String(300), default = None)
    pub_key  = db.Column(db.String(300), default = None)


    # foreign key to
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)
    transactions = db.relationship('Transaction', backref='wallet', lazy=True, cascade='all, delete, delete-orphan')

    ##many to many
    #account = db.relationship('Account', secondary = 'transaction', back_populates = 'wallet')

    

    def __init__(self, accountId, balance):
        self.account_id = accountId
        self.balance = balance
        self.available_balance = balance
        self.pending_balance = 0

    def __repr__(self):
        return f"<Wallet: walletkey={self.walletkey}, balance={self.balance}, available_balance={self.available_balance}, prending_balance={self.pending_balance}, pub_key={self.pub_key}>"    
    

## act as auxiliary table for user and group table
#transaction = db.Table(
#    "transaction",
#    db.Column("account_id", db.Integer, db.ForeignKey("account.id")),
#    db.Column("wallet_id", db.Integer, db.ForeignKey("wallet.id")),
#    db.Column("status", db.Enum(PlatformModel.TransactionState), nullable=False, default = PlatformModel.TransactionStat.Cr ),
#)


class Transaction(BaseModel,db.Model):
    __tablename__ = 'transaction'
    __table_args__ = (
        PrimaryKeyConstraint('id',),
    )


    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    #Attribute cols
    transactionkey = db.Column(db.String(32), nullable = False, unique = True, default= BaseModel.idGenerator)
    status = db.Column(db.Enum(PlatformModel.TransactionState), nullable=False, default = PlatformModel.TransactionStat.Cr )
    amount = db.Column(db.Integer, default = 0)
    comment = dbColumn(db.String(256), default="A comment on the transaction")
    invoice = dbColumn(db.String(64), nullable = True, default = None)
    lastupdated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # foreign key 
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable = False)

    def __init__(self, walletId, amount=0,comment = None , invoice = None  ):
        self.wallet_id = walletId
        self.amount = amount
        self.invoice = invoice
        if comment:
            self.comment = comment

    def __repr__(self):
        return f"<Transaction: walletkey={self.walletkey}, balance={self.balance}, available_balance={self.available_balance}, prending_balance={self.pending_balance}, pub_key={self.pub_key}>"    
    


########
##
##

class Contacts (BaseModel,db.Model):
    __tablename__ = 'contacts'
    __table_args__ = (
        PrimaryKeyConstraint('id',),
    )


    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    #application attribute
    accountkey =  db.Column(db.String(32), nullable = False, unique = True)
    address = db.Column(db.String(256),nullable = False, unique= True) #1 - email

    #foreign key
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)

    def __init__(self, accountId, accountKey, address  ):
        self.account_id = accountId
        self.accountkey = accountkey
        self.address = address 

    def __repr__(self):
        return f"<Contacts: accountkey={self.accountkey}, address={self.address}>"    
    

    



if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print "Creating database tables..."
    db.create_all()
    print "Done!"
