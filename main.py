# Copyright (C) 2024  CZnavody19

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from rich import print
from rich.progress import Progress
from questionary import checkbox, path
from os import listdir, mkdir
from os.path import join, exists
from ffmpeg import input as ff_input, output as ff_output, overwrite_output as ff_overwrite
from threading import Thread
from time import sleep

directory_ask = path("Select the directory with the videos")
supported_formats = ["mp4", "avi", "mkv"]

global_errors_encountered = False
global_finished_processes = 0

def get_all_video_files(path: str) -> list[str]:
    out = []

    for file in listdir(path):
        if file.split(".")[-1] in supported_formats:
            out.append(file)

    return out

def set_conversion_params(directory: str, file: str) -> any:
    return ff_overwrite(ff_output(
        ff_input(join(directory, file)),
    join(directory, "converted", ".".join(file.split(".")[:-1]) + ".mp4"),
    vcodec="mpeg4", acodec="flac"
    ))

def run_conversion(conversion: any, progress: Progress, directory: str) -> None:
    global global_finished_processes
    task_id = progress.add_task("Converting", total=None)
    try:
        conversion.run(quiet=True)
    except Exception as e:
        global global_errors_encountered
        global_errors_encountered = True

        with open(join(directory, "error.log"), "a") as f:
            f.write(str(e) + "\n")
    finally:
        global_finished_processes += 1
        progress.remove_task(task_id)

def main() -> None:
    directory = directory_ask.ask()
    files = get_all_video_files(directory)
    selection = checkbox("Select videos to convert", choices=files)
    selected = selection.ask()

    if not exists(join(directory, "converted")):
        mkdir(join(directory, "converted"))

    to_convert = []
    for file in selected:
        to_convert.append(set_conversion_params(directory, file))

    input("Press enter to start the conversion")

    with Progress(transient=True) as progress:
        for conversion in to_convert:
            th = Thread(target=run_conversion, args=(conversion,progress,directory,))
            th.start()

        total_processes = len(to_convert)
        while global_finished_processes < total_processes:
            sleep(1)

    print("[green][bold]Conversion(s) finished[/bold][/green]")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[red][bold]Conversion(s) aborted[/bold][/red]")
    finally:
        if global_errors_encountered:
            print("[red]Some errors were encountered during the conversion, check the error.log file in your selected directory[/red]")