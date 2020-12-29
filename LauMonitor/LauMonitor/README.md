![Alt-Tag](https://i.imgur.com/V5ERvU4.png)
### About:
NERYS will monitor specified sites for keywords and sends a Discord alert when a page has a specified keyword. This can be used to monitor any site on a product release date to automatically detect when a product has been uploaded. Useful when monitoring hundreds of sites for shops in different timezones.


### Usage:
Add your Discord webhook URL in the appropriate fields (line 143 on other-sites.py and line 204 on shopify-sites.py), surrounded by quotation marks. You can set keywords you want to monitor at the bottom of each of the scripts, following the same format as the example. Seperate keywords with a '-' instead of a ' ' on other-sites.py. Add sites to monitor to each of the respective text files, following the same format as the examples (I suggest using Notepad++, Notepad does something weird). Proxies should also be one per line, following the same format as the examples provided in <proxies.txt>. For the Supreme monitor, all you have to do is add your webhook to <supreme.py> on line 81. I have it set on an 8 second delay, meaning you won't need proxies to run it at all. If you use proxies though, you can shorten this delay. Make sure to use proxies based on region (ex. North American proxies for Supreme US). It will build the database and send all new products and restocks to your Discord server. It will spam your Discord when it first starts up so mute the Discord channel for a few minutes while it catches up.

### Complete:
- find all products on Shopify site by keyword
- send discord notifications
- monitor for new products
- optimization for Shopify to return product checkout links by size
- find all products on other sites by keyword
- attempt to get product page links for universal sites
- supreme new products
- supreme restocks

Have suggestions on how to make the monitor better? Let me know via Twitter (@snivynGOD)!

#### This is the first version of the monitor (let's call it the 'lite' version). Check out the latest version here: https://www.sharanga.io/shop/nerys

### Credits:
Niveen Jegatheeswaran - That's Me! - https://github.com/snivyn/, https://twitter.com/snivynGOD

kyb3r - Discord Embed - https://github.com/kyb3r/
