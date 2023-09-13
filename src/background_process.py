# Performance:
# 1. When loading a file to preview, we only load a small part of the file example 1400 characters
# 2. We will apply the Colors to the preview text
# 3. If the user is still waching the preview after x amount of milliseconds, we will load the full file

# Performance:
# To make the application run fast and smooth we will:
# - Have a timer, that works as an EventLoop
# The Timer will fire every X milliseconds and check the state of the application.

# I general we will try to perform as little work as possible.
# But when 