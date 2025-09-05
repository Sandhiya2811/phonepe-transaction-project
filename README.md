# phonepe-transaction-project
## phonepay transaction details 2018-2024
### Announcements
  🌟 Data for Q3(July, August, September) and Q4(Octobar, November, December) of 2024 has been added and is available for consumption.

### Table of Contents
  This data has been structured to provide details of following three sections with data cuts on Transactions, Users and Insurance of PhonePe Pulse - Explore tab.
        1. Aggregated - Aggregated values of various payment categories as shown under Categories section
        2. Map - Total values at the State and District levels.
        3. Top - Totals of top States / Districts /Pin Codes

#### 1. Aggregated data
  This section provides state-level aggregated values of different categories. It gives a high-level summary of counts and amounts.
  ##### 1.1 Agg_Ins
     Description: 
            Aggregated insurance details by state, year, quarter, and type.Insurance data at country level.
     Columns:
            state → State name
            year → Year of record
            quarter → Quarter (1–4)
            Insurance_type → Type of insurance (e.g., Life, Health)        
            Insurance_count → Number of insurance policies
            Insurance_amount → Total insurance amount
  ##### 1.2 Agg_Trans
    Description:
            Aggregated mobile app usage and registered user data by state, year, and quarter.Transaction data broken down by type of payment at country level.
    Columns:
            state → State name
            year → Year of record
            quarter → Quarter (1–4)
            transaction_type → Category (e.g., Peer-to-Peer, Merchant Payments)
            transaction_count → Total number of transactions
            transaction_amount → Total value of transactions
  ##### 1.3 Agg_User
    Description: 
            Aggregated mobile app usage and registered user data by state, year, and quarter.Users data broken down by devices at country level.
    Columns:
            state → State name
            year → Year of record
            quarter → Quarter (1–4)
            install_mobile_brand → Brand of mobile used
            reg_user_brand → Number of registered users by brand
            user_percentage → Percentage share of brand among users
            registeredUsers → Total registered users
            appOpens → Number of times the app was opened  

#### 2. Map data
  This section provides state and district-level metrics, allowing geographical visualization of usage, transactions, and insurance.
  ##### 2.1 Map_Ins
     Description: 
            District-level insurance statistics.Total number of insurance and total value of all insurance at the state level.
     Columns:
            district_name → District name
            year → Year of record
            quarter → Quarter (1–4)
            insurance_count → Number of insurance policies
            insurance_amount → Total insurance value
  ##### 2.2 Map_Trans
    Description:
            District-level insurance statistics.Total number of transactions and total value of all transactions at the state level.
    Columns:
            state → State name
            year → Year of record            
            quarter → Quarter (1–4)            
            district_name → District name            
            transaction_count → Number of transactions            
            transaction_amount → Total transaction value
  ##### 2.3 Map_Ins_All
    Description:
            State-level insurance data with geographic coordinates for mapping.
    Columns:
            state → State name
            year → Year of record          
            quarter → Quarter (1–4)            
            latitude → Latitude (for map plotting)            
            longitude → Longitude (for map plotting)            
            metric_value → Insurance metric (count/amount)
            district_name → District name
  ##### 2.4 Map_User
    Description: 
            District-level registered users and app usage.Total number of registered users and number of app opens by these registered users at the state level.
    Columns:
            state → State name
            year → Year of record
            quarter → Quarter (1–4)
            district_name → District name 
            registeredUsers → Number of registered users 
            appOpens → Number of times app opened  

#### 3. Top data
  This section highlights the top-performing states, districts, and pincodes based on transactions, insurance, and user registrations.
  ##### 3.1 Top_Ins
     Description: 
            Top 10 states / districts / pin codes where the most number of the insurance happened for a selected year-quarter combination.
     Columns:
            state → State name
            year → Year of record            
            quarter → Quarter (1–4)            
            location → State/District/Pincode name            
            location_type → Location type (state/district/pincode)            
            insurance_count → Number of insurance policies            
            insurance_amount → Total insurance value
  ##### 3.2 Top_Trans
    Description:
            Top 10 states / districts / pin codes where the most number of the transactions happened for a selected year-quarter combination.
    Columns:
            state → State name
            year → Year of record            
            quarter → Quarter (1–4)            
            location → State/District/Pincode name            
            location_type → Location type (state/district/pincode)            
            transaction_count → Number of transactions            
            transaction_amount → Total transaction value
  ##### 3.3 Top_User
    Description: 
            Top 10 states / districts / pin codes where most number of users registered from, for a selected year-quarter combination.
    Columns:
            state → State name
            year → Year of record          
            quarter → Quarter (1–4)           
            location → State/District/Pincode name            
            location_type → Location type (state/district/pincode)            
            registered_users → Number of registered users








































































































            
