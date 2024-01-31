from pytimedinput import timedInput
userText, timedOut = timedInput("Send to a different mail? (default: chrisvy4895@gmail.com) [y/n]: ", timeout=5)
if(timedOut):
    print("Continuing...")
else:
    print(f"User-input: '{userText}'")

userText2, timedOut = timedInput("Send to a different mail? (default: chrisvy4895@gmail.com) [y/n]: ", timeout=5)
if(timedOut):
    print("Continuing...")
else:
    print(f"User-input: '{userText2}'")


