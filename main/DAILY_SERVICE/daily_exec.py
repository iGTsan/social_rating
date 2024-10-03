def dailyTasks(isProdigy, isLocal, sendQueue, pipeQueue, debug):
    print("dailyTasks")
    try:
        tasks = daily.Daily(isProdigy, isLocal, sendQueue, pipeQueue, debug)
        tasks.start()
    except Exception as shit:
        print("dailyTasks", shit)
