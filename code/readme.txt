WIP

run the process on the background


launchctl unload ~/Library/LaunchAgents/com.example.led_control.plist
launchctl load ~/Library/LaunchAgents/com.example.led_control.plist


You need two env variables:
IFTTT_KEY 
TOGGL_API_TOKEN


It looks for a .env file.