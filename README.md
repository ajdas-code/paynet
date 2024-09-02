# paynet

                          +---------------------------------------+
                          |          RIV = Research In Value      |
                          |         - RabbitMQ                    |
                          |         - SQLite                      |
                          |         - Postgres                    |
                          |         - Flask                       |
                          |         - ReST                        |
                          +---------------------------------------+
                                      /   |   \    \      \   
                                     /    |    \    \      \
                                    /     |     \    \      \
                                   /      |      \    \      \
                                  /       |       \    \      \
                                 /        |        \    \      \
+-----------------------+   +-----------------------+  +---------------------+
| #1  RivPay [Client]   |   |#2Settlement & Recon    |  |  RivMerchant        |
|  - mobile app         |   |  - Luigi               |  |  - Braian           |
|  - Braian             |   |  - PySpark             |  |                     |
|                       |   |  - Ajitesh             |  |                     |
+-----------------------+   +-----------------------+  +---------------------+
                                     |                        |
                                     |                        |
                                     |                        |
                                     |                        |
                                +-----------------------------+
                                |   Platform BC               |
                                |   - geth                    |
                                |   - Ajitesh                 |
                                +-----------------------------+
                                      |
                                      |
                                      |
                                +-----------------------------+
                                |   Data & Analytics          |
                                |   - Apache Iceberg          |
                                |   - Ajitesh                 |
                                +-----------------------------+
                                      |
                                      |
                                      |
                                +-----------------------------+
                                |   API ready to be hooked    |
                                |   with Online Store         |
                                |   - Braian                  |
                                +-----------------------------+

Legend:
1. Flask - API / Python - C and M
2. ReST
3. Demo/PoC - SQLite, Postgres
3.a Luigi
4. PyTorch and PySpark - not ready for demo
5. geth - Private
6. Solidity



Project A : PayNet :: RiVPay


1. Use Cases -
a>> **Functional** 
 
On-board and Initialize
   1. Consumer create a user account and Provides the KYC details (Account_State == "Created and KYC verification pending"
   2. Admin verifies and approves the user account - ( Account_State == "Active')
   2.a Consumer is able to login the user account
   3. Consumer Adds funding source to the account -[ Bank account ) 
   4. Consumer creates a wallet  and load funds [ 1 PN coins = 1 cents ]
   5. Consumer loads the fund from the funding source (Account_Status == 'Transactable )

Adding Contacts
   6. Consumer add a contact for sending (p2P) money 
   7. Consumer search a contact by [ name, email and phone number] and add as a contact to send p2p money 

Transactions [ PUSH]
   8. [PUSH] Constumer selects a contact to send money and enter amount and Note
   9. [PUSH] Consumer re-auths using 2A 
   10. [PUSH] Money sends to contact with confirmations [ Handle the overdraft case accordingly]

Transaction [PULL]
   11. [PULL] Consumer gets PUSH Notification on the APP with Invoice details, Merchant Details and Amount due. 
   12. [PULL] Consumer re-auths using 2A 
   13. [PULL] App generates a "LOCKER_BOX" as HTLC and float it on PayNet [ with details of invoice, consumer details and amount]
   14. [PULL] App upon approval of Consumer, sends the HTLC key to merchants as auth [Handles failure case accordingly]

Transaction Lookup/Lists
   15. Consumer looks up or search for transactions ( Pagination) - 
         - [Listing of all transactions] on Chronology order
            ODFIs
              - PULL transactions - created as pending 
              - PULL transactions - settled as posted 
              - PUSH transaction  
            RDFIs
              - Receives/RDFI PUSH transactions
              - PULL transactions - timed out as expired
              - "LOAD" ing events from funding sources
   16. Consumer selects a transaction/event and see the details 
   17. Consumer can lookup a transaction - search/filter by type, recever name/merchat name or date
   18. Consumer can see it's account prosition and account details page
   19. Raise a dispute on a transaction
   

b>> Non-Functional

1. System should be available for search functionalities 
2. DAU 10 mln concurrent user 
3. Strict consistency on transactions and add consumers  


2. Core Entities
    - Account [ id, kyc details, status, ... ].  {{ status: Created | Active | Transactable | InActive }}
    - Contact [ source_account1_id, sending_account_id2, note]
    - Wallet [ id, account_id, balance, key-sets ] 
    - Transaction [ id, wallet_id, timestamp, destination_wallet_id, tx_receiopt, amount, type, invoice = nullable] 
         {{ Type: {PUSH_ODFI, PULL_ODFI, PUSH_RDFI**, PULL_RDFI, LOAD }}
         {{ Status: Created | Pending | Settled | Expired }}
    - Statement [ id, month, year, account_id, wallet_id, <loc_of_pdf>]


3. API 
   a>> Account
       - POST  /accout
       - PUT.  /account [ @token_authorized ] 
       - GET. /account  [ @token_authorized ]
       - GET. /account/ALL? filter = status  [ Sys_admin ]
       - DELETE /account [ @token_authorized ] {{ Note: Delete will NOT delete account but make it InActive - Compliance reason }}
   b>> Contact  
       - POST /contact [ @token_authorized ] 
       - GET /contact/id [ @token_authorized ] 
       - GET /contact/ALL [ @token_authorized ] 
       - DELETE /contact [ @token_authorized ]  
   c>> Wallet
       - POST /wallet [ @token_authorized ] 
       - GET /wallet/id [ @token_authorized ] 
       - PUT /wallet [ @token_authorized ] 
   d>> Transaction 
       - POST /Transaction [ @token_authorized or Sys_admin] 
       - GET /Transaction/id [ @token_authorized or Sys_admin] 
       - GET /Transaction/ALL [ @token_authorized or Sys_admin]
       - PUT /Transaction/id [ @token_authorized or Sys_admin]
   e>> Statement 
       - POST /Statement  [ Sys_admin] 
       - GET /Statement ? filter = <> [ @token_authorized or Sys_admin]
       
  5. 

   
