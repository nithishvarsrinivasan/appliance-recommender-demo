# Appliance Energy Efficiency Recommender (Python + Flask)
## A simple demo system crunches simulated appliance usage data to generate energy‑saving upgrade suggestions, for households. It spots the appliance that hogs the power and recommends an efficient model to lower electricity consumption and costs. Users can submit feedback, which the system uses to refine its recommendations.

### Features
+ Simulated user-appliance usage dataset
+ Recommendations based on usage frequency and power consumption
+ Energy-efficient upgrade suggestions
+ Feedback collection (helpful/not helpful)
+ Flask API with endpoints:
  - `/recommend?user_id=U1` (Get recommendation)
  - `/feedback` (POST JSON feedback)
  - `/users` (List users)
  - `/` (Web UI for testing)
