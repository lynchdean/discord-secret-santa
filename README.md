# discord-kris-kindle

# TODO (in order of priority)
v1.0 - 21/11 (Evening sometime)
- All done :) 

v1.1 - AKA future features
- !join prompt on server join
- self kick function
- help command with list of functions
- Limit command accessibility (ie. certain commands only accessible in main server and not in DMs)
- Add max limit to redraws to prevent max recursion errors where draw is not possible, or too complicated for the 
current random-order implementation. (Maybe add a limit to the entries or exclusions instead?)

Issue found during live testing:
- If !exclude @User is entered on a mobile device, it doesnt seem to pass the username value/ID through, 
so you need to use the discord ID of that person in place of their @.
