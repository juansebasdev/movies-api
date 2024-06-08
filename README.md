# Movies API

This is an REST API for users to share and recommend their favorite movies.

## Usage
Movies API is available in 

[https://movies-api-dev-service-2q7oct76la-ue.a.run.app](https://movies-api-dev-service-2q7oct76la-ue.a.run.app)

> [!NOTE]
> There's a swagger documentation you can use to test the API in
> [https://movies-api-dev-service-2q7oct76la-ue.a.run.app/docs](https://movies-api-dev-service-2q7oct76la-ue.a.run.app/docs)

### Login Action
> [!IMPORTANT]
> 

This endpoint [https://movies-api-dev-service-2q7oct76la-ue.a.run.app/login]([https://movies-api-dev-service-2q7oct76la-ue.a.run.app/login) will return an url that will redirect the user to google auth window, copy it in the browser and after that it will return a JWT in the field `idToken`

This is a Bearer token that the API will request in order to authenticate users in the endpoints which require it.

### Database
Movies API support SQL (with SQLite) and NoSQL (with MongoDB) connections, you __MUST__ set `DATA_REPOSITORY` env variable with `SQL` or `NOSQL`


## Development
> [!IMPORTANT]
> Use Python Version 3.12

1. Create a virtualenv
   
   You can use 
   ```sh
   python3 -m venv .venv
   ```
   Or use the Makefile
   ```sh
   make venv
   ```

2. Activate virtualenv
   
   You can do it using `source` command
   ```sh
   source .venv/bin/activate
   ```

3. Install Dependencies (Requirements)

    For development, it is recommended to install dev and test requirements
    ```sh
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -r requirements-test.txt
    ```
    or using the `make` command
    ```sh
    make install
    ```

4. Setup environment variables
   
   Copy .env.example file and fill the fields with the values, following the description

   ```sh
   cp .env.example .env
   ```

   > [!NOTE]
    > To setup `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`, you __MUST__ create a project in google console to be able to manage and create this credentials

5. Setup database and sample data
   
   This step will setup the database with the necessary tables/collections and fill columns/properties with sample data, you must run

   ```sh
   make setup
   ```
   > [!NOTE]
   > It will setup an SQL or NoSQL database according to the value of `DATA_REPOSITORY` variable in `.env` file


6. Run project

    To run the project, use this command
    ```sh
    uvicorn src.main:app --reload
    ```

    > [!NOTE]
    > If you are using `VSCode` editor, there's a launch.json file in the project for debugging

## Testing
Unit tests are included in the project. To run them, just execute

```sh
pytest tests
```

or using the `make` command within the Makefile

```sh
make test
```

## Continuous Integration
Github Actions is used to run tests and verify the operation of the API. This pipeline is available in [ci.yml](/.github/workflows/ci.yml).

## Continuous Deployment
Github Actions is used to deploy the API in GCP, where Infrastructure is also managed using `Terraform`. This pipeline is available in [cd.yml](/.github/workflows/cd.yml).

## Docs
The API documentation is generate automatically because of the framework: `FastAPI`, therefore it updates dynamically and can be requested locally in

```sh
http://{HOST}:{PORT}/docs
```