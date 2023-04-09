import shutil

# remove build, dist, logs, TrimLog.egg-info folders
shutil.rmtree("build")
shutil.rmtree("dist")
shutil.rmtree("TrimLog.egg-info")
shutil.rmtree("logs")
