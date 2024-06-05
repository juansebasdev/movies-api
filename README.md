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

4. Run project

    To run the project, use this command
    ```sh
    uvicorn src.main:app --reload
    ```

    > [!NOTE]
    > If you are using `VSCode` editor, there's a launch.json file in the project for debugging