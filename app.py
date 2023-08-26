from flask import Flask, request
import pystray
from PIL import Image
import playsound
import threading
import os
import vdf
import winreg
import shutil

app = Flask(__name__)


def write_cfg():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\Valve\Steam', 0, winreg.KEY_READ)
    value, type = winreg.QueryValueEx(key, 'SteamPath')
    data = vdf.parse(open(f'{value}/steamapps/libraryfolders.vdf'))
    for key, value in data['libraryfolders'].items():
        for i in data['libraryfolders'][key]['apps']:
            if i == '730':
                csPath = os.path.join(data['libraryfolders'][key]['path'], 'steamapps', 'common', 'Counter-Strike Global Offensive')
                cfgPath = os.path.join(csPath, 'csgo', 'cfg', 'gamestate_integration_announcer.cfg')
                if not os.path.exists(cfgPath):
                    shutil.copyfile('config.cfg', cfgPath)
                    print('WE HAVE CSGO IN')
                    print(csPath)
                    print('Config in')
                    print(cfgPath)


def play_sound(file):
    playsound.playsound(file, False)


@app.route('/gsi', methods=['POST'])
def incoming_data():
    data = request.json
    print(data)
    if 'previously' in data:
        if 'player' in data['previously']:
            if 'state' in data['previously']['player']:
                if 'round_kills' in data['previously']['player']['state']:
                    if data['player']['state']['round_kills'] == 1:
                        threading.Thread(target=play_sound, args=('1.mp3',)).start()
                    elif data['player']['state']['round_kills'] == 2:
                        threading.Thread(target=play_sound, args=('2.mp3',)).start()
                    elif data['player']['state']['round_kills'] == 3:
                        threading.Thread(target=play_sound, args=('3.mp3',)).start()
                    elif data['player']['state']['round_kills'] == 4:
                        threading.Thread(target=play_sound, args=('4.mp3',)).start()
                    elif data['player']['state']['round_kills'] == 5:
                        threading.Thread(target=play_sound, args=('5.mp3',)).start()
    return 'OK', 200


def shutdown_server():
    import os
    os.kill(os.getpid(), 2)


def exit_action(icon, item):
    icon.stop()
    shutdown_server()


def run_server():
    app.run(host='localhost', port=9001)


def main():
    image = Image.open('2x.ico')
    print(image)
    menu = (
        pystray.MenuItem('Exit', exit_action),
    )
    print(menu)

    icon = pystray.Icon('name', image, 'buh', menu)
    print(icon)
    icon.run_detached()
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    write_cfg()


if __name__ == '__main__':
    main()
