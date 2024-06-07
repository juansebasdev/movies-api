# Movies API

This is an REST API for users to share and recommend their favorite movies.

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