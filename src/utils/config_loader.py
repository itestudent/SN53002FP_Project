from configparser import ConfigParser

class ServerConfig:
    ip_address: str
    folder: str
    zip_folder: str

class ClientConfig:
    folder: str
    image_folder: str
    text_folder: str
    virus_folder: str
    zip_folder: str

class Config:
    server: ServerConfig
    client: ClientConfig

    def __init__(self):
        self.server = ServerConfig()
        self.client = ClientConfig()

def load_config(config_filename: str) -> Config:
    # parse config file
    parser = ConfigParser()
    parser.read(config_filename)
    parsed = parser['global']
    
    #region create configuration
    config = Config()

    # load client configuration
    config.client.folder = parsed['client_folder']
    config.client.folder = parsed['client_folder']
    config.client.image_folder = parsed['client_image_folder']
    config.client.text_folder = parsed['client_text_folder']
    config.client.virus_folder = parsed['client_virus_folder']
    config.client.zip_folder = parsed['client_zip_folder']

    # load server configuration
    config.server.ip_address = parsed['Ipaddress']
    config.server.folder = parsed['server_folder']
    config.server.zip_folder = parsed['server_zip_folder']
    #endregion
    
    return config