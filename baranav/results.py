import os
import webbrowser

os.chdir(os.path.dirname(__file__))

def get_results(query: str) -> list:
    """
    Key to list returned:
    [<icon e.g. /icon/firefox.png>,
    <action_name e.g. Firefox>,
    <subtext e.g. Web Browser>,
    <type 1=url;2=app;3=desktop_action;4=google;>,<execute e.g. 'subprocess.run("/bin/firefox")'>]
    :param query:
    :return list:
    """
    results = []
    web_results = []
    app_results = []
    ggl_results = []

    if query.startswith(("https://","http://","www.",)):
        web_results.append(["icons/url.svg",f'Open "{query}" in browser',"Web",1,lambda: webbrowser.open(query)])
    results += app_results + web_results + ggl_results
    results = list(filter(None, results))
    return results
hii = [["/home/nur/Downloads/1544x1544_circle.png","hii","a word used by me in greeting.","0"],["/home/nur/Downloads/1544x1544_circle.png","Firefox","Web Browser"]]