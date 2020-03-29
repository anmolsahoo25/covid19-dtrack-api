COVID-19 India Dtrack Api
---
Backend server for the distributed tracking app for making contact
tracing easier

Overview
---
This is a simple Flask app, that serves as a thin API for a Postgres
database. A sample can be deployed on Heroku. 

Roadmap
---
* Add phone number auth
  + While we do not want to collect any personally identifiable info,
  we need to still ensure that at-least, people with phones are uploading
  the data
* Update databases for Wifi data, GPS data
* Implement paging so that users don't have to download entire database
