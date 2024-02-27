# StorageManager
> ITE SN53002FP Project

A maintainence automation script for a certain cloud hosting company.  
This project is based on the specifications in `.specs/SN53002FP_Project.pdf`.  

It contains:
- `mock_server` -> Local Test FTP Server
- `src` -> StorageManager source code

## Usage

### Environment Setup
Generate Python Env:
```sh
$ python -m venv env
```

Activate Env (Windows Powershell):
```sh
$ .\env\Scripts\activate
```

Install Dependencies:
```sh
$ python -m pip install -r requirements.txt
```

### Configuration
The StorageManager script should be run in a directory containing a `config.txt`.  
This file should have a `.ini` format, following `example.config.txt` as an example.  

A `config.txt` has been provided for ease of use.
Which is compatible with the `mock_server` given.

### Running
Activate the environment first as per the above section.  
Make sure a `config.txt` file is available wherever the script is run as well.  
```sh
$ python ./src/main.py
```

## Project Structure
```
.
├── readme.md
├── .specs
│   ├── project_resource.zip <-- sample resources given
│   └── SN53002FP_Project.pdf <-- project specification
├── mock_server
│   ├── readme.md <-- description of the mock server
│   ├── __main__.py <-- entrypoint for the sample server
│   └── server_root <-- folder that is served via ftp
└── src <-- source code of StorageManager script
    ├── main.py <-- entrypoint of the StorageManager script
    └── utils <-- module containing utilities
```
