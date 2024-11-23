
MARKETPLACE
==============================

1.Synopsis
------------------------------
This is an event marketplace specification - a platform where event makers (partners) can sell tickets to the platform users using 
different selling models with autoscaling and separate worker process and queue for selling.

- Standard (FIFO);
- "*Early bird*";
- "*Lottery*";
- "*Auction*".

2.Backend architecture
------------------------------

The architecture suggests modularity and should have such services:
- Selling logic services (selling models handling);
- User service;
- Partner service;
- Administrator management service;
- Monitoring service;
- Report and Statistic service;
- Billing service;


3.Features (requirements):
------------------------------
 - OpenAPI support;

4.How to build and run
------------------------------

```commandline
make build
make run
```

or 

```commandline
docker-compose up -d
```