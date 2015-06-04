'Elite Merchant' is a trade route calculator for Elite: Dangerous.

	GETTING STARTED / CONFIGURATION
 
On Windows, download the binary ( http://mahti.serv.fi/EliteMerchant/EliteMerchantInstaller.exe )

Install - Run - Profit!

Or on Linux, MacOS (or for the adventurous)...

Download the source ( https://github.com/BeTeK/EliteMerchant )

Install Python 3.4 ( https://www.python.org/ )

Install PyQt5 ( http://www.riverbankcomputing.com/software/pyqt/download5 )

Optional: Download EDCE for market data download ( https://github.com/BeTeK/edce-client/archive/feature/make_edce_more_library_friendly.zip )
(Or the equivalent in your Linux/MacOS distribution)

In /src run  python3 ./main.py
 
The database is downloaded on first launch and updated hourly, if an updated
database is detected.
The tool does function without access to ED, but connecting to it is recommended.
The first thing you should do after starting up is setting up your ED installation
path so the automatic player location detection feature is activated.
You can open the options screen from the top 'edit/options' menu.
Click "..." to browse for your ED installation path.
This refers to the PRODUCT path and not the LAUNCHER path.
This would look something like:

	[elite install path]/Products/FORC-FDEV-D-10xx/     ( where xx varies )
 
This screen also has entries for EDCE path, and your ED login credentials.
These fields are ONLY used to interface with EDCE and are not required for other use.
 
 
"Market expire days" sets a hard limit for when to consider market data as invalid.
 
 
You can enable or disable automatic export searches here, and define what triggers
them. The log file option is reliable and does an instant search as you approach
a station. The EDCE option waits for the EDCE client to download the latest market
data before searching. This is inconsistently slow. Enabling both is possible.


	FEATURES


The prominent features of this tool, in contrast to others are:
- Route profitability calculation as function of distance and time
	This means the tool takes your estimated travel time from system to system
	into account, as well as travel time from the target star to the station.
	The specifics of this calculation is described in our release thread,
	see link at top.
- Optional EDCE support to read station market data.
	Upon entering a station, the EDCE client is triggered to gather the
	data into the local database. Optional uploading to EDDN is also supported.
	Note that EDCE is in conflict with Frontier Developments wishes on
	the use of their mobile API. Thus this feature is entirely optional
	and on everyone's personal judgement to utilize, or not.
- Multiple searches in tabs
- Fast, high profit routes for all searches with unlimited trade hops
- Automatic station exports search
	Upon entering a station, search tabs with 'exports from current station'
	are automatically triggered with their current settings.
	This saves you from alt+tabbing to the tool on a second monitor to do this
	basic task. This also works on a secondary computer, if you share Elite's Log
	folder over the network.
- Long distance multi-hop optimal route profit search
	Want to feel like a trucker and don't like dead ends or low profit routes?
- Multi-hop optimal loop search
	Find profitable loops of arbitrary length
- From-To trade route search
	Want to get from point A to B and do some trading on the way?
 
The tool utilizes the database provided by EDDB. ( http://eddb.io/api )
