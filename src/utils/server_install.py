import time
import requests
from pick import pick
import os
from utils.cosmetics import cprint
from utils.file import download
from configs.config_manager import CONFIG

PAPER_LINK = "https://papermc.io/api/v2/projects/{project}"
PAPER_V2_API_VERSION = "https://papermc.io/api/v2/projects/{project}/versions/{version}"
PAPER_V2_API = "https://papermc.io/api/v2/projects/{project}/versions/{version}/builds/{build}/downloads/{download}"


def install_paper() -> str:
    '''
    Downloads a papermc server
    '''
    json_reply = requests.get(PAPER_LINK.format(project="paper")).json()

    versions = json_reply["versions"]
    versions.reverse()

    # We now create a picker to easily select the version we want
    selected = pick(versions, "Select the version you want to download (Enter to Select)",
                    indicator="⟶", multiselect=False)
    version = selected[0]
    return install_with_paperv2_api("paper", version)


def install_waterfall() -> str:
    '''
    Downloads a waterfall server
    '''
    json_reply = requests.get(PAPER_LINK.format(project="waterfall")).json()
    versions = json_reply["versions"]
    versions.reverse()
    
    return install_with_paperv2_api("waterfall", versions[0])


def install_with_paperv2_api(project: str, version: str) -> str:
    try:
        start = time.time()
        _, json_reply = download(PAPER_V2_API_VERSION.format(
            project=project, version=version), return_json=True, no_download=True)
        build = str(json_reply["builds"][len(json_reply["builds"])-1])
        print(f"{project} {version} {build}")

        file_name = f"{project}-{version}-{build}.jar"

        if os.path.isfile(CONFIG.cache_directory+"/"+file_name):
            cprint(f'&b{file_name} already exists in cache using cached version')
        else:
            download_url = PAPER_V2_API.format(
                project=project, version=version, build=build, download=file_name)
            cprint(
                f'&bDownloading {file_name}:{version}:{build} from {download_url}')
            download(download_url, file_name)

        end = time.time()
        cprint(f"&bDownload {file_name} took {round(end-start, 3)} seconds")

        return file_name
    except Exception as e:
        print(e)
        return ""
