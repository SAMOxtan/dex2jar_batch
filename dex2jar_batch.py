from multiprocessing import Pool
import sys
import os
import zipfile
import subprocess
from rich import progress

d2jpath = 'd2j-dex2jar.bat'
d2joutput = 'd2j-output'
d2jerror = 'error'
d2jzip = 'd2j-output.zip'
poolsize = 4

def cmd(dir, file, output):
    cmd_string = f'{d2jpath} --skip-exceptions {dir}/{file} -o {output}/{file[:-4]}.jar -e {output}/{d2jerror}/{file[:-4]}-error.zip'
    process = subprocess.Popen(cmd_string, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk')
    process.wait()
    return f'{output}/{file[:-4]}.jar'

if __name__ == '__main__':
    pool = Pool(poolsize)
    output = f'{sys.argv[1]}/{d2joutput}'
    result = []
    if not os.path.exists(output):
        os.mkdir(output)
    
    if not os.path.exists(f'{output}/{d2jerror}'):
        os.mkdir(f'{output}/{d2jerror}')

    listdir = [file for file in os.listdir(sys.argv[1]) if file.endswith('.dex')]

    with progress.Progress(
        "[progress.description]{task.description}",
        progress.BarColumn(complete_style = 'green', finished_style='red'),
        progress.MofNCompleteColumn(),
        progress.TimeRemainingColumn(),
        progress.TimeElapsedColumn(),
        refresh_per_second=1,  # bit slower updates
    ) as progress:
        task1 = progress.add_task('[red]Dex2Jar', total=len(listdir))
        for file in listdir: 
            result.append(pool.apply_async(func=cmd, args=(sys.argv[1], file, output)))
        
        for i in result:
            if i.get():
                progress.advance(task1, advance=1)
            
        pool.close()
        pool.join()

        listoutput = [file for file in os.listdir(output) if file.endswith('.jar')]
        task2 = progress.add_task('[red]ZipFile', total=len(listoutput))
        with zipfile.ZipFile(d2jzip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=3) as zip_obj:
            for file in listoutput:
                zip_obj.write(f'{output}/{file}', arcname=file)
                progress.advance(task2, advance=1)
        
    print(f'Completed! --> {d2jzip}')
