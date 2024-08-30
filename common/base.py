######################################
# Models for Common Model
####################################
import enum
from app import db

## Domain Constants
##
## Account state
##


class AccountStatus(enum.Enum):
    Cr = "Cr: Created"
    Ac = "Ac: Active"
    Tr = "Tr: Transactable"
    In = "In: InActive"
    Er = "Er: Errored"  # system failture - Http Code - 5xx
    Re = "Lo: Locked"  # Business logic failure - Http code - 4xx

## Domain Constants
##
## Transaction state
##


class TransactionStatus(enum.Enum):
    Cr = "Cr: Created"
    Pr = "Pe: Pending"
    Se = "Se: Settled"
    Co = "Fi: Finalized"
    Ex = "Ex: Expired"
    Er = "Er: Errored"  # system failture - Http Code - 5xx
    Re = "Re: Reversed"  # Business logic failure - Http code - 4xx



## Domain Constants
##
## Transaction Type
##


class TransactionType(enum.Enum):
    PUSH_ODFI = "PUSH_ODFI"
    PULL_ODFI = "PULL_ODFI"
    PUSH_RDFI = "PUSH_RDFI"
    PULL_RDFI = "PULL_RDFI"
    LOAD = "LOAD"
    ERROR = "ERROR"  # system failture - Http Code - 5xx
    REVERSE = "REVERSE"  # Business logic failure - Http code - 4xx



##
## Platform Base Class
##


    


    
        


