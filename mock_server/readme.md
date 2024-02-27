# StorageManager Mock Server
> Mock Server for testing of StorageManager

The mock test FTP server for the parent project.
This is used as a quick and easy way to test the StorageManager script.

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

Unzip the mock server resources, and move `do_not_touch` folder into `server_root`,
such that it is in this structure  
```
mock_server
├── __main__.py
└── server_root
    └── do_not_touch
```

### Running
Activate the environment first as per the above section.  
Then run the server with:  
```sh
$ python .
```
