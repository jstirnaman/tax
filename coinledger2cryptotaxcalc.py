# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 22:26:35 2022

@author: stirn
"""

import pandas as pd

def advanced_import():
    VOYAGER_TRXNS = "C:/Users/stirn/Downloads/Transactions.csv"
        
    trxns = pd.read_csv(VOYAGER_TRXNS)
    trxns = trxns.rename(columns = { "Internal Id": "ID" })
    trxns["Type"] = trxns["Type"].map({
                           "Deposit": "deposit",
                           "Income": "income",
                           "Interest Income": "interest",
                           "Fiat Buy": "buy",
                           "Fiat Sell": "sell",
                           "Withdrawal": "withdrawal"
                         })
    debits = trxns[trxns["Record Type"] == "Debit"]
    debits = trxns.rename(columns = { "Asset": "Quote Currency", "Amount": "Quote Amount"})
    
    credits = trxns[trxns["Record Type"] == "Credit"]
    credits = credits.rename(columns = { "Amount": "Base Amount",
                                         "Asset": "Base Currency",
                                         "Timestamp (UTC)": "Credit Timestamp (UTC)"
                                       })
    one_line_trxns = pd.merge(debits, credits, on="ID").rename(columns = { "Type_x": "Type" })

    return one_line_trxns[
    ['Credit Timestamp (UTC)',
      'Type',
      'Base Amount',
      'Base Currency',
      'Quote Currency',
      'Quote Amount',
      'ID']
    ]

def simple_import():
    VOYAGER_TRXNS = "C:/Users/stirn/Downloads/Transactions.csv"
    
    trxns = pd.read_csv(VOYAGER_TRXNS)
    trxns = trxns[trxns["Type"] != "Deposit"]
    
    debits = trxns[trxns["Record Type"] == "Debit"]
    debits = trxns.rename(columns = { "Asset": "Asset Traded", "Amount": "Amount Traded"})
    
    credits = trxns[trxns["Record Type"] == "Credit"]
    credits = credits.rename(columns = {"Amount": "Amount Received",
                              "Asset": "Asset Received",
                              "Timestamp (UTC)": "Credit Timestamp (UTC)"})
    
    one_line_trxns = pd.merge(debits, credits, on="Internal Id")

    return one_line_trxns[
        ['Timestamp (UTC)',
         'Asset Traded',
         'Asset Received',
         'Amount Traded',
         'Amount Received']
        ]
    

CRYPTO_TAX_CALC_TRXNS = "2022-voy-trxns-crypto-tax-simple.csv"
simple_import().to_csv(CRYPTO_TAX_CALC_TRXNS)

    
CRYPTO_TAX_CALC_TRXNS = "2022-voy-trxns-crypto-tax-advanced.csv"
advanced_import().to_csv(CRYPTO_TAX_CALC_TRXNS)