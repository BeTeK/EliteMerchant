### 'Elite Merchant' is a trade route calculator for Elite: Dangerous.

#####Reddit release thread:
http://www.reddit.com/r/EliteDangerous/comments/38k4ss/elite_merchant_trade_route_calculator/

### GETTING STARTED / CONFIGURATION
 
On Windows, download the binary ( http://mahti.serv.fi/~elite/EliteMerchantInstaller_latest.exe )

Install - Run - Profit!


Or on Linux, MacOS (or for the adventurous)...

Download the source ( https://github.com/BeTeK/EliteMerchant )

Install **Python 3.4** ( https://www.python.org/ )

Install **PyQt5** ( http://www.riverbankcomputing.com/software/pyqt/download5 )

Some systems also require the packages **libsqlite3-0** and **sqlite3**

Optional: Download **EDCE** for automatic market data download ( https://github.com/Andargor/edce-client )

**EDCE** and building an installer require the **requests** python package

In /src run **python3 ./main.py**
 
 
The database is downloaded on first launch and updated hourly, if an updated database is detected.

The tool does function without access to ED, but connecting to it is recommended.  
The first thing you should do after starting up is setting up your ED installation path so the automatic player location detection feature is activated.  
You can open the options screen from the top 'edit/options' menu.  
Click "..." to browse for your ED installation path.  
This refers to the PRODUCT path and not the LAUNCHER path.  
This would look something like:  
> [elite install path]/Products/FORC-FDEV-D-10xx/     ( where xx varies )

This screen also has entries for EDCE path, and your ED login credentials.  
These fields are ONLY used to interface with EDCE and are not required for other use.
 
"Market expire days" sets a hard limit for when to consider market data as invalid.
 
You can enable or disable automatic export searches here, and define what triggers them. The log file option is reliable and does an instant search as you approach a station.  
The EDCE option waits for the EDCE client to download the latest market data before searching. This is inconsistently slow. Enabling both is possible.

### FEATURES

The prominent features of this tool, in contrast to others are:
- Route profitability calculation as function of distance and time.  
  This means the tool takes your estimated travel time from system to system into account, as well as travel time from the target star to the station.
- Optional EDCE support to read station market data.  
  Upon entering a station, the EDCE client is triggered to gather the	data into the local database. Optional uploading to EDDN is also supported. Note that EDCE is in conflict with Frontier Developments wishes on the use of their mobile API. Thus this feature is entirely optional
	and on everyone's personal judgement to utilize, or not.
- Black market trades  
Smuggling routes can now be profitable and shown on a possible trade route.  
Smuggling trades are marked with black commodity background and a skull icon.  
NOTE! Black market prices are estimates derived from local legal commodity prices.  
The resulting price is inaccurate and is only indicative of your final price (probably +-500cr or so).  
Passive faction bonuses have already been applied to the shown black market price.  
- Multiple searches in tabs.
- Fast, high profit routes for all searches with unlimited trade hops.
- Automatic station exports search.

  Upon entering a station, search tabs with 'exports from current station' are automatically triggered with their current settings. This saves you from alt+tabbing to the tool on a second monitor to do this basic task. This also works on a secondary computer, if you share Elite's Log folder over the network.
- Long distance multi-hop optimal route profit search.

  Want to feel like a trucker and don't like dead ends or low profit routes?
- Multi-hop optimal loop search.

  Find profitable loops of arbitrary length
- From-To trade route search.

  Want to get from point A to B and do some trading on the way?
 
The tool utilizes the database provided by EDDB. ( http://eddb.io/api )

#####Version history:
v0.13.150726: Fixed a regression  
v0.13.150717: Fixes, Optimization
- Fixed export prices not updating from EDDB
- Optimized search - should be a lot faster.

v0.13.150701: Powers, Black market trades
- Powers and factions  
Power control and exploited systems are marked with a faction icon (faction name on mouse hover).  
Factions (Empire, Federation, Alliance) marked by system & station background color.  
- Black market trades  
Smuggling routes can now be profitable and shown on a possible trade route.  
Smuggling trades are marked with black commodity background and a skull icon.  
NOTE! Black market prices are estimates derived from local legal commodity prices.  
The resulting price is inaccurate and is only indicative of your final price (probably +-500cr or so).  
Passive faction bonuses have already been applied to the shown black market price.  
- Supply now shown better in UI as column and colored red when low.  
- Basic cache for generic trade search  
- Numerous bugfixes and small improvements

v0.12.150619: Moved away from windowed queries as they did more harm than good.  
v0.11.150619: 1.3 fixes and basic features  
- Added Direct system-to-system / station-to-station trade listing
- Added user guide  
Explaining all the things
- Multithreaded searches  
UI no longer freezes, can cancel searches in progress
- Update notifier  
A basic feature that should have been in at the start
- Fixed 1.3 automatic search triggers  
1.3 removed the station name from the ED log and this made things a bit more difficult for us.  
This means we've moved to higher reliance on EDCE to provide station name.  
FD, why u no API?? (yಠ,ಠ)y
- Search log in UI, separate window disabled in binary
- Can define specific export and import stations
- Target route attempts to find imports to final system/station more
- Fixed low exports results from low profit systems
- Optimized graph search - shouldn't get stuck anymore
- Fixed a bazillion bugs everywhere

v0.9.150605: hotfix - was trying to optimize an unoptimizable situation  
v0.9.150604: initial release
