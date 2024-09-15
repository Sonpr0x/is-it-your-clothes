## How to contribute
1. Clone the repo.
2. Install app.
3. Create a new branch.
4. Make changes and test.
5. Submit pulls request with clear description of changes.

## How to install
### 1. Install Python `venv` Module and Activate

1. Ensure Python is installed on your system.
2. Run the following command to create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    - On Linux/MacOS:
    
      ```bash
      source venv/bin/activate
      ```

    - On Windows:
    
      ```bash
      venv\Scripts\activate
      ```

   ⚠️ Create virtual env outside webapp directory or add filename to .gitgnore

### 2. Install Python Libraries from `requirements.txt`

Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```
### 3. Run webapp server

```bash
python app.py
```

Now feel free and dev ur suck app.

## Acknowledgements
