def eventManager(eventQueue, isProdigy, isLocal, sendQueue, pipeQueue, debug):
    print("eventManager")
    executor = events.Events(isProdigy, isLocal,sendQueue, pipeQueue)
    threadPool = concurrent.futures.ThreadPoolExecutor(max_workers=32)

    if debug:
        test_event = {'message': {'date': 1669403763, 'from_id': 231688699, 'id': 0, 'out': 0, 'attachments': [], 'conversation_message_id': 610, 'fwd_messages': [], 'important': False, 'is_hidden': False, 'peer_id': 2000000001, 'random_id': 0, 'text': '/топ'}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback', 'intent_subscribe', 'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}}
        threadPool.submit(executor.start_event, executor.delta, test_event)
        threadPool.submit(executor.start_event, executor.top, test_event)
        threadPool.submit(executor.start_event, executor.top_all, test_event)
        threadPool.submit(executor.start_event, executor.roll, test_event)
        threadPool.submit(executor.start_event, executor.summarry, test_event)
        threadPool.submit(executor.start_event, executor.sound, test_event)
        threadPool.submit(executor.start_event, executor.my_cock, test_event)
        threadPool.submit(executor.start_event, executor.remove_cock, test_event)

    while True:
        try:
            while True:

                event = eventQueue.get(True)

                #   if not(isLocal):
                #   print(os.getpid(), event)



                if debug and event["message"]["text"][0] == "/":
                    threadPool.submit(executor.start_event, executor.TechRab, event)
                    continue

                if event["message"]["text"].lower() == "/писюн":
                    threadPool.submit(executor.start_event, executor.delta, event)
                elif event["message"]["text"].lower() == "/топ":
                    threadPool.submit(executor.start_event, executor.top, event)
                elif event["message"]["text"].lower() == "/топ_все":
                    threadPool.submit(executor.start_event, executor.top_all, event)
                elif event["message"]["text"].lower() == "/ролл":
                    threadPool.submit(executor.start_event, executor.roll, event)
                elif event["message"]["text"].lower() == "/чат":
                    threadPool.submit(executor.start_event, executor.summarry, event)
                elif event["message"]["text"].lower() == "/микс":
                    threadPool.submit(executor.start_event, executor.sound, event)
                elif event["message"]["text"].lower() == "/мой_писюн":
                    threadPool.submit(executor.start_event, executor.my_cock, event)
                elif event["message"]["text"].lower() == "/кострация":
                    threadPool.submit(executor.start_event, executor.remove_cock, event)
                break
        except Exception as shit:
            print("eventManager", shit, event)
