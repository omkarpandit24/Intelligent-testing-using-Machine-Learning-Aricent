import pandas as pd
import numpy as np

# Import Dataset
dec_pst = pd.read_csv("Dec17_ISS.CSV", encoding='latin1')
df = pd.read_csv('CSR_title_text.csv', error_bad_lines=False);

dec_pst.rename(columns={'From: (Name)': 'From_Name'
                        ,'From: (Address)': 'From_Address'
                        ,'To: (Name)': 'To_Name'
                        ,'To: (Address)': 'To_Address'
                        ,'CC: (Name)': 'CC_Name'
                        ,'CC: (Address)': 'CC_Address'}, inplace=True)

dec_pst = dec_pst[['From_Name', 'From_Address', 'To_Name', 'To_Address', 'CC_Name', 'CC_Address','Subject', 'Body']]
dec_pst['Email_no'] = range(1, len(dec_pst) + 1)
dec_pst = dec_pst[['Email_no','From_Name', 'From_Address', 'To_Name', 'To_Address', 'CC_Name', 'CC_Address','Subject', 'Body']]


subject_series = pd.Series(dec_pst['Subject'])

#Seperating emails only related to ISS and CSRs
dec_pst_csr = dec_pst[subject_series.str.contains("CSR", na = False)]

#Extracting CSR numbers from subject line of an email
dec_pst_csr['CSR_No']= dec_pst_csr.Subject.str.extract('(\d+)')
dec_pst_csr['CSR_No_1'] = dec_pst_csr['CSR_No'].str[-6:]

dec_pst_csr.dtypes
dec_pst_csr = dec_pst_csr.convert_objects(convert_numeric=True)
dec_pst_csr.dtypes

#Merge CSR email data with CSR matrix defect data based on CSR number. 
merged_dec_pst = pd.merge(left=dec_pst_csr,right=df, left_on='CSR_No_1', right_on='CSR_no')

#Focusing on important columns
merged_dec_pst = merged_dec_pst[['CSR_No_1','CSR_no','SR_title','Subject', 'Body']]


dec_csr_count = dec_pst_csr.CSR_No_1.value_counts()
dec_csr_count.sum()