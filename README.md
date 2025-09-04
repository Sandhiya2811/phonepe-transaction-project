# phonepe-transaction-project
phonepay transaction details 2018-2024

Insights Generation Document
1. Aggregated Tables
🔹 Agg_Ins (Insurance)
Columns: state, year, quarter, Insurance_type, Insurance_count, Insurance_amount
Insights:
•	State-wise and quarter-wise insurance penetration.
•	Identify which insurance type (Life/Health/etc.) is most popular.
•	Compare premium (amount) vs policy count → average policy value.
Recommendations:
•	Promote low adoption insurance types in underperforming states.
•	Offer micro-insurance schemes where average ticket size is low.
•	Target awareness campaigns in states with high count but low premium amount.
________________________________________
🔹 Agg_Trans (Transactions)
Columns: state, year, quarter, transaction_type, transaction_count, transaction_amount
Insights:
•	Growth trend in UPI transactions over time.
•	Top transaction types (peer-to-peer, merchant, recharge, etc.).
•	Identify states contributing the highest share in transaction volume & value.
Recommendations:
•	Focus merchant onboarding in states with high P2P but low merchant transactions.
•	Special offers in high-value states during festive seasons.
•	Improve digital payment awareness in states with low adoption.
________________________________________
🔹 App_User
Columns: state, year, quarter, install_mobile_brand, reg_user_brand, user_percentage, registeredUsers, appOpens
Insights:
•	Which mobile brands dominate app usage.
•	State-wise adoption of registered users.
•	Engagement: AppOpens / RegisteredUsers → stickiness of users.
Recommendations:
•	Partner with top mobile brands (like Xiaomi, Samsung) for co-promotions.
•	Launch user retention campaigns in states where app opens are low.
•	Push regional language features in states with low adoption.
________________________________________
2. Map Tables
🔹 Map_Ins
Columns: district_name, year, quarter, insurance_count, insurance_amount
Insights:
•	Insurance penetration at district level.
•	Hotspot districts vs underperforming districts.
Recommendations:
•	District-level awareness drives.
•	Expand agent networks in low coverage districts.
________________________________________
🔹 Map_Ins_All
Columns: state, year, quarter, latitude, longitude, metric_value, district_name
Insights:
•	Geo-level distribution of insurance metrics.
•	Map visualization for quick hotspot identification.
Recommendations:
•	Use geo-marketing for awareness.
•	District-level campaigns where insurance values are below average.
________________________________________
🔹 Map_Trans
Columns: state, year, quarter, district_name, transaction_count, transaction_amount
Insights:
•	District-wise digital payment adoption.
•	Compare urban vs rural trends.
Recommendations:
•	Encourage rural adoption with cashback offers.
•	Improve merchant onboarding in rural areas.
________________________________________
🔹 Map_User
Columns: state, year, quarter, district_name, registeredUsers, appOpens
Insights:
•	District-wise adoption of PhonePe.
•	Identify high registered users but low active users.
Recommendations:
•	Run engagement campaigns in inactive user districts.
•	Add regional support features in low-usage districts.
________________________________________
3. Top Tables
🔹 Top_Ins
Columns: state, year, quarter, location, location_type, insurance_count, insurance_amount
Insights:
•	Top-performing states/districts for insurance.
•	Which location types (urban/rural) drive more adoption.
Recommendations:
•	Launch targeted products in rural where adoption is lower.
•	Focus retention on top locations with loyalty offers.
________________________________________
🔹 Top_Trans
Columns: state, year, quarter, location, location_type, transaction_count, transaction_amount
Insights:
•	Top districts/states in transactions.
•	Urban vs rural split in digital transactions.
Recommendations:
•	Partner with local kirana stores in rural areas.
•	Build more features for urban business transactions.
________________________________________
🔹 Top_User
Columns: state, year, quarter, location, location_type, registered_users
Insights:
•	Identify highest adoption locations.
•	Urban vs rural split of registered users.
Recommendations:
•	Provide referral bonuses to boost user base in rural.
•	Focus on feature-rich updates for urban users.







Scenario 1

Understanding Transaction Patterns on PhonePe (Aggregated_Transaction)
1. State-wise Transaction Trends
Insights:
•	Big states like Maharashtra, Karnataka, Tamil Nadu have the highest number of transactions.
•	Small states and North-East states have less usage.
•	Some states are growing slowly but not very high in numbers.
Recommendations:
•	Add more shops and merchants in low-usage states.
•	Give cashback offers to attract users in small states.
•	In top states, launch extra services like bill payments and insurance.
________________________________________
2. Year & Quarter-wise Trends
Insights:
•	Transactions are increasing every year.
•	Q3 & Q4 (festivals like Diwali) show the highest usage.
•	Q1 (start of year) has a small drop in usage.
Recommendations:
•	Run festival offers in Q3 & Q4 to use the high demand.
•	Give loyalty rewards in Q1 to keep users active.
•	Be ready for system load in festival season.
________________________________________
3. Transaction Type Trends
Insights:
•	Money transfers between people (P2P) are very high in number.
•	Merchant payments (P2M) have more value even if less in number.
•	Recharges and bill payments are growing slowly.
Recommendations:
•	Give offers to increase merchant payments.
•	Remind users about recharge and bill payment features.
•	Add insurance and investment options for big payments.
________________________________________
4. State vs Transaction Type
Insights:
•	In big cities/states (Maharashtra, Delhi, Karnataka), merchant payments are common.
•	In small states, people use more person-to-person transfers.
•	There is a big difference between urban and rural areas.
Recommendations:
•	Support small shops in rural areas with QR codes and training.
•	Give regional language awareness campaigns.
•	Onboard local kirana stores to increase merchant usage.
________________________________________
Overall Summary
•	PhonePe is growing strongly, but usage is not equal in all states.
•	Festivals and urban states give maximum growth.
•	Need to improve merchant payments in rural and small states.
•	With targeted offers and campaigns, PhonePe can balance growth everywhere.



Scenario 2

Device Dominance and User Engagement Analysis (Aggregated_User)
1. Which mobile brand has the most registered users
Insights:
•	Brands like Xiaomi, Samsung, and Vivo have the highest number of registered users.
•	Some small brands have fewer users overall.
Recommendations:
•	Partner with top brands for promotions (pre-installed app, cashback offers).
•	For small brands, give special offers to increase new registrations.
________________________________________
2. Compare brands → high registration but low engagement
Insights:
•	Some brands have many registered users, but their AppOpens (engagement) is low.
•	This means people download/register but do not use the app often.
Recommendations:
•	Run push notifications, reminders, or rewards to improve engagement.
•	Provide faster performance and updates for underperforming devices.
•	Give brand-specific campaigns (e.g., Samsung users → recharge offers).
________________________________________
3. Which brands are popular in each state
Insights:
•	In some states, Xiaomi is top, while in others, Samsung or Oppo is more common.
•	Regional differences are clear in brand usage.
Recommendations:
•	Create state-wise offers based on popular brands.
•	Do regional partnerships (e.g., local mobile stores).
•	Translate app features into local languages where needed.
________________________________________
4. How brand usage changes across years/quarters
Insights:
•	Xiaomi and Vivo are growing in recent years.
•	Some older brands (like Nokia) are declining in usage.
•	Seasonal changes also affect engagement (festival quarters = higher activity).
Recommendations:
•	Focus on fast-growing brands for marketing tie-ups.
•	For declining brands, keep support but reduce spend.
•	Launch festival campaigns during Q3/Q4 for higher engagement.
________________________________________
Overall Summary
•	Xiaomi, Samsung, Vivo are the main drivers of user adoption.
•	Some brands have high registrations but poor engagement → need action.
•	Brand popularity changes by state and over time, so strategies must be flexible.
•	With targeted offers, device optimization, and regional campaigns, PhonePe can improve user engagement.



Scenario 3
Insurance Transactions Analysis (Top_Insurance)
1. Top 10 States by Insurance Amount
Insights:
•	Big states like Maharashtra, Karnataka, Tamil Nadu, and Delhi contribute the highest insurance amounts.
•	Some states show very low contribution to insurance transactions.
Recommendations:
•	Continue premium products and marketing in top states.
•	In low-performing states, launch awareness campaigns and low-cost insurance options.
________________________________________
2. Top 10 Districts by Insurance Count
Insights:
•	Certain metro districts (like Bangalore Urban, Mumbai, Hyderabad) have the highest number of policies.
•	Rural and small districts contribute less.
Recommendations:
•	Focus on rural distribution channels and local agents.
•	Give incentives to agents in smaller districts to sell more policies.
________________________________________
3. Top 10 Pincodes by Insurance Amount
Insights:
•	Urban pincodes with high-income populations show the largest insurance amount.
•	Some pincodes have high policy counts but lower average value.
Recommendations:
•	Create custom plans for urban high-value customers.
•	In areas with many low-value policies, introduce micro-insurance or bundled plans.
________________________________________
4. Insurance Amount Growth by Year-Quarter
Insights:
•	Insurance amount is growing every year, with peaks in Q3 & Q4 (festive seasons, tax-saving time).
•	Some quarters show slower growth compared to others.
Recommendations:
•	Push tax-saving insurance campaigns in Q3 & Q4.
•	Maintain customer engagement in Q1 & Q2 with special offers.
•	Use seasonal insights to design yearly marketing plans.
________________________________________
Overall Summary
•	Top states, districts, and pincodes dominate insurance transactions, mostly urban-focused.
•	Rural and small districts are underpenetrated and need more awareness.
•	Growth is steady, but seasonal trends (festivals, tax time) make Q3 & Q4 most important.
•	With targeted marketing, rural penetration, and custom products, PhonePe can expand its insurance business.





Scenario 4
Transaction Analysis Across States and Districts
1. Where transactions are concentrated (high engagement)
Insights:
•	Transactions are mostly concentrated in urban areas and metro states like Maharashtra, Karnataka, Delhi, and Tamil Nadu.
•	Rural and small districts show low transaction activity.
Recommendations:
•	Strengthen merchant networks in rural and semi-urban areas.
•	Give cashback or referral offers to increase rural adoption.
•	Keep adding new services in urban areas to retain active users.
________________________________________
2. Top States by Transaction Amount
Insights:
•	A few states contribute the largest share of transaction value, showing strong digital adoption.
•	Other states have high user base but lower transaction value.
Recommendations:
•	In high-value states, introduce premium services (loans, investments).
•	In lower-value states, run awareness campaigns to improve trust in large-value transactions.
________________________________________
3. Top Districts by Transaction Count
Insights:
•	Districts like Bangalore Urban, Mumbai, Hyderabad lead in number of transactions.
•	Some districts have high count but low average value per transaction.
Recommendations:
•	Focus on district-level merchant tie-ups to boost higher-value usage.
•	For districts with small-value transactions, introduce easy EMI and bill pay features.
________________________________________
4. Top Pincodes by Transaction Amount
Insights:
•	Urban pincodes with high-income users contribute the highest transaction amounts.
•	Rural pincodes show much lower values.
Recommendations:
•	Provide customized offers for top pincodes (high-value customers).
•	Expand QR-code adoption and digital training in rural pincodes.
________________________________________
5. District vs Pincode Contribution (count & amount)
Insights:
•	Some districts are strong because of a few pincodes contributing most transactions.
•	In other districts, transactions are more evenly spread across pincodes.
Recommendations:
•	For concentrated pincodes: expand to neighboring areas to balance growth.
•	For evenly spread districts: scale up infrastructure to support steady adoption.
________________________________________




Overall Summary
•	Transactions are highly concentrated in metro states, districts, and urban pincodes.
•	Rural and semi-urban areas remain underutilized.
•	Focusing on merchant onboarding, rural awareness, and premium services in top states will balance growth and improve engagement.







Scenario 5

User Registration Analysis (Top_User)
1. Which states have the most users
Insights:
•	States like Maharashtra, Karnataka, and Uttar Pradesh have the highest number of registered users.
•	Smaller states and North-East regions have much fewer registrations.
Recommendations:
•	Focus new user acquisition campaigns in small states.
•	Give regional offers (cashback, referral bonuses) to attract more users.
•	In top states, launch advanced features to keep users engaged.
________________________________________
2. Which districts have the most users
Insights:
•	Big metro districts like Bangalore, Mumbai, Hyderabad, and Delhi show the highest registrations.
•	Rural districts have fewer new users.
Recommendations:
•	Expand awareness campaigns in rural districts.
•	Tie up with local shops and agents for easier onboarding.
•	Provide regional language support to improve adoption.
________________________________________
3. Which pincodes have the most users
Insights:
•	Urban pincodes (metro city areas) dominate in user registrations.
•	Some pincodes show fast growth, while others remain stagnant.
Recommendations:
•	For top pincodes: run exclusive promotions to retain high users.
•	For slow-growth pincodes: introduce discounts and referral rewards.
•	Target youth-focused campaigns in urban pincodes.
________________________________________
4. How registrations change over quarters in a state
Insights:
•	Registrations usually increase steadily year by year.
•	Festival quarters (Q3 & Q4) have higher registrations.
•	Some states show slow growth or flat trend in recent quarters.
Recommendations:
•	Run special registration drives during festivals to maximize growth.
•	Use advertisements in low-growth states to push adoption.
•	Monitor quarterly patterns and adjust marketing spend accordingly.
________________________________________
Overall Summary
•	Most users come from large states and metro cities, while rural and small regions are underrepresented.
•	Registrations peak during festival quarters, showing seasonal patterns.
•	With targeted rural campaigns, regional offers, and festival promotions, PhonePe can expand its user base across India.




