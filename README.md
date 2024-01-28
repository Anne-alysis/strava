# Introduction

This is a sandbox for analysis of my Strava data. 

## Strava API Client
Install Swagger Codegen via Homebrew: `brew install swagger-codegen` (Mac).

Then, generate the Python API:
```bash 
swagger-codegen generate -i https://developers.strava.com/swagger/swagger.json -l python -o generated
```

Copy the `swagger_client` module into an accessible place.  Simpler way is just to use `requests` with headers.