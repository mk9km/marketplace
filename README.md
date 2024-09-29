
EVENT MARKETPLACE
==============================

1.Synopsis
------------------------------
This is an event marketplace specification - a platform where event makers (partners) can sell tickets to the platform users using 
different selling models with autoscaling and separate worker process and queue for selling.

- Standard (FIFO);
- "*Early bird*";
- "*Lottery*";
- "*Auction*".

3.Backend architecture
------------------------------

The architecture suggests API microservices and should have such services:
- Selling logic services (task manager, selling models handling) (API service);
- User panel (API service);
- Partner panel (API service);
- Admin management panel (API service);
- Infrastructure management service (API service);
- Monitoring service (API service);
- Report and Statistic service (API service);
- Billing service (API service);


2.Features (requirements):
------------------------------
 - Separate worker (process) and queue for each partner for scaling;
 - Each service should support OpenAPI