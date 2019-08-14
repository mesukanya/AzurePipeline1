from dotenv import load_dotenv
import os


project_folder = os.path.expanduser("/home/admin1/Desktop/TwitterLiveData") # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

print(os.environ.get('AZURE_TENANT_ID'))