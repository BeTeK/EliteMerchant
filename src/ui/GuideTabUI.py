# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\ui\GuideTab.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(983, 989)
        self.gridLayout_3 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_3.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">                    <img src=\"data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAYFBMVEVNVESjh1rbuXcaKS01QzyId1P//q7//7ObgVevr3t+cFCvkF7nwXsRICXw7KEIFyBrZkshMjMlNjWWmpNgYU2DgXDPyJjw8fBsdl5BS0BYWkc6Rz4gMTJzfWAsPDl3bE5oDgZOAAAG8UlEQVR4XsTOWRXAMAwDweUgH0lP/iz7/FMKGgSD0kbV3eQbLvcMyDgwiaWaANuFUFkDmyVnYOANnM/1Bz5izG7XbRAIwj5ZLFXEyAa5FzEr5/3fsuEfB3PKctx07qP5AjujNZp9UDoAKAgAelcSPyW562F4A2AKxOcErASQYv6/AGjAPiWpt20oAQDfBJmunYHHNpwBSJVLvuR/YKQuFDsHQLVnihS4P6z7fp3YcHoFuLOgjAHV/Yn+d1dJnwNIpp0Sg1JS3adFBnd9jR5NJ2AvAPE+TQsqdekJVAGckjkAfE23aQW0Q/ivZwCyALgQCuP/AhAAiNclYa+kAFzeYgMIIYz/bdpmWhfIv0jVeuDQP8L5OwAhKpXUh9IAEPw9AK2nMakHALLz7wOAZE8DkLb5HILzTwAE72BNrmJQtvskhvxlAKT7D+b0KjayIYz+Xw6AaB/daVWMO/MEgN6fjyEFpClAVMGdVMWhAgGC/2YBvjjnI03MHgGxikG6Ckz+6zraGNCl7XJBrWLfv8l/MQBdYra726tYp51QiOT/Apj6AHbhMlOv4hJgFoX/TwBibFqKSGsGDiD3N3qOVPH7dATAJoDdAeT+ZK1W2xuAlASAOH+j+fNEBYwIYMzbqlhrZgGSv3fnVkQKC8AA0LjXY1gAzPPBn9OUSAMAyvoeqSsA0d/ZU6fPKABoVMq5V6u4BMjPnw7ADwAM5DdlfA4Q8ufGj/focAVoEJpnQEGWv04En4U8BepUBmAoAH45gKcvgGeXQgxTD1SruEzB+GOCQw84glPJc4DZnsEUCD4P8GOC9yakAwhPwHtn4AhQ7+ISQLsqjgTRn3MqgY9hCEHbRmQBDHPIAqcHMSCkKq5vxroCICUGgjHYk4OQqtibN23FmlkAlRG4GPCOheR2BCh1BuA/zxGPt7D0L6XfNbGuARh/yLOw8H6AmIH2tdxJiNQHazfA+1ZcxLAEOCNYn7furfjYRE2f51AQbAZgWlDtRJWPFU0A+E6wLAZgmF8SJEFJ0ACA4XUsEWRfx0AXWjXPAPgnupCF8oECKYJFgcTo3fxAsRsI1wcRwI30H1bNRtlNEArCTTGiYzGBuc0k1fj+j9lw4Gbxh59D7r7AfiGHFRd5RaEWfU87Eeb5rpjkWxIQvIpKPFhKZYzo5YvAhC1vpqDQS9ATa6xBDYAhANnj9aSBEg1J+CfQHHgAHDAzGEHZq3rZyv59KkhEMYbQmWMQicB3xcUzoP1esgAvArU6mqSjWJPQFhMBDSFvDwjSxQI4gs2bsknmAClMJAJgSykLQATvmjN7aUWEe4LPAEKCPMAhQQ2AAkBIUHxtt5qE0/WjFcAc+ClIRDFyJAQxDS+CnRzAOLpJxFZATZe7tAKI9iT8XSDHwROEx3R6OX1Er+1IGxIb7VZK5Etj5XRxAB0I9DsSpxjAXt/+868nU/f7jQDOIYFDiAHM0XDVWj0lX60FAAFSuXnQCESGEAru8F4ALV8EAILv+tYsAIjfnq9j+XInAMnV2IEAqWymY4BdnYGZdgAjW7fuiEA3L4CJDyD7c8fWlgAAUy3A5wS6ses/JWYAshR7gBNPFgEEDoDSJrULkIQWQTkAeLMFghgAohjyENptQ9l7+4GrFYEQBgCHUQx5CKMDgKFOIYGOAezk/UOAoRoABPNi3Q/+gkPREACgDuFkhUkEQGYIfRQLDOGJVGVPeeBPKA0AEtvQZ8EmByo3Ael8I//2eQwQP12oVQ7U2ZO/JP8vMVUD1BFs/NUyPeoBSB/5X4QFmEpngBh+YgXgPy+lUewwEMVn2DMV+COKi3MAUVy9C97+tgky08MR5JMQUVz3ON76XxU1qBPOA2XPAiMI4PabrWHjrzUdSnEiKnsauhVoJVvt0Fnh97vbvLJTsXfHs6BGp9X8Z0/F0SORutcCnMP9b0X9QOGpWL+z6PKUbHkA+CshcCxnAojm+sXSqwQi4+7Af+auwOwaD656Atj7W4B/hTMADMGQIhHAGMwfOooYgIk3f1gNZkMC/1VBESkqE8KSZOUpHYD3X9eV0a44paVQeJUgAPJXszePf0uGKN6LD0EEBAB/9MWpD5sjWljCCmD9sfyEEO2KkzJFQnj2cjd/S6YrLjEonUIaQu+/6boTXXFCzKqQANb5gwskLgCfwQEgf+DPAeArIKAZiPjnu+J6BSSqv+9vCkjprvhzeRTzECvXkmu7n9XWF/6sKK7X0kS+YPjfrB3jMBDCQBQdybQUaxOMIeH+x4wQRYRCkWKF8y4wv3Ll7SVkIg7tRp+9nx6bW2cOdq+5tYP6FTDgmLm/BgD1nF2A4awlwMXfBMgr+QZkKXAN0CwJ1nyEi6CapVhnFxdF6CjAk3xEegPhifUZMhxnlQAAAABJRU5ErkJggg==\" /><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\">    Elite Merchant<br /></span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Release thread:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.reddit.com/r/EliteDangerous/comments/38k4ss/elite_merchant_trade_route_calculator/\n"
"\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">http://www.reddit.com/r/EliteDangerous/comments/38k4ss/elite_merchant_trade_route_calculator/</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Source:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/BeTeK/EliteMerchant\n"
"\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">https://github.com/BeTeK/EliteMerchant</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\'Elite Merchant\' is a trade route calculator for Elite: Dangerous.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Developed by <span style=\" font-size:8pt;\">Paavo Happonen and Pasi Luostarinen.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The prominent features of this tool, in contrast to others are: </span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Black market smuggling as a type of trade route</span></li>\n"
"<li style=\" font-size:8pt; font-weight:600;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Route profitability calculation as function of distance and time. <span style=\" font-weight:400;\"><br />This means the tool takes your estimated travel time from system to system<br />into account, as well as travel time from the target star to the station.<br />This replaces traditional needs to blacklist low value items or set station distance<br />requirements. Estimated travel time is displayed and search results sorted by<br />estimated profit per hour.</span></li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">PowerPlay filters and bonuses.</span></li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Multiple searches in tabs.</span></li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Fast, high profit routes for all searches with unlimited trade hops.</span></li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Automatic station exports search. </span><br />Upon entering a station, search tabs with \'exports from current station\' are<br />automatically triggered with their current settings. This saves you from<br />alt+tabbing to the tool on a second monitor to do this basic task. This also<br />works on a secondary computer, if you share Elite\'s Log folder over the network.</li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Long distance multi-hop optimal route profit search. </span><br />Want to feel like a trucker and don\'t like dead ends or low profit routes?</li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Multi-hop optimal loop search. </span><br />Find profitable loops of arbitrary length</li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">From-To trade route search. </span><br />Want to get from point A to B and do some trading on the way?</li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Optional EDCE support to read station market data. </span><br />Upon entering a station, the EDCE client is triggered to gather the data into the<br />local database. Optional uploading to EDDN is also supported.<br />Note that EDCE is in conflict with Frontier Developments wishes on the use of<br />their mobile API. Thus this feature is entirely optional and on everyone\'s personal<br />judgement to utilize, or not.<br />As the ED log no longer gives current station, EDCE use is recommended for full<br />functionality.</li></ul>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The tool utilizes the database provided by EDDB. ( <a href=\"http://eddb.io/api\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">http://eddb.io/api</span></a> )</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">    OVERLY DETAILED DESCRIPTION OF UI FUNCTIONS:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">    Options window:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can open the options screen from the top \'edit/options\' menu of the main window.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Market expire days</span><br />This sets a hard limit for when to consider market data as invalid.<br />Commodity prices on searches are colored according to this scale,<br />where <span style=\" background-color:#88ff88;\">0 days is green</span> and <span style=\" background-color:#ff8888;\">red is this many days old</span>.<br />No trades older than this are accepted for trade routes.<br />This value is ignored for current system export, target system imports and direct<br />system to system sales.<br />If values from these searches exceed the age set here, the price is colored<br /><span style=\" color:#ffff00; background-color:#ff0000;\">bright red with yellow text</span> to denote that it is heavily outdated.<br /><span style=\" font-weight:600;\">Always </span>check the age of data colored like this.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Elite product path</span><span style=\" font-size:8pt;\"><br />Find your ED installation product path.<br />This is used to find the Elite travel log and to detect current location.<br /></span>The tool does function without access to ED, but connecting to it is recommended.<br />Click &quot;...&quot; to browse for your ED installation path.<br />This refers to the PRODUCT path and not the LAUNCHER path.<br />This would look something like:<br />    <span style=\" font-weight:600;\">[elite install path]/Products/FORC-FDEV-D-10xx/</span> ( where <span style=\" font-weight:600;\">xx</span> varies )</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">EDCE path, Elite username, Elite password<br /></span>These fields are ONLY used to interface with EDCE and are not required for other use.<br />Once you enter your details, press \'Test EDCE connection\' and confirm your account.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">    Main Window:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The bottom of the window has the log which shows progress of search and other actions.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">At the top left you see your current location, as captured from your ED Log and EDCE.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Your global ship settings:</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Jump range</span><br />This is REQUIRED, and will directly influence profit per hour calculation and<br />thus route profitability</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Pad size</span><br />Optional, but frankly you should set this to match<br />Coming to a station with pads too small for your ship is embarrassing<br />Also speeds up searches quite a bit</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Cargo space</span><br />This setting is entirely optional and does not influence calculation in any way<br />It is purely for convenience of showing final profits of a trip (in tooltip on<br /> profit column)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">    The SEARCH tab:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This tool has 6 distinct types of trade route searches:</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Exports from current station</span><br />This attempts to find an outgoing trade route from the current station.<br />This is triggered by automatic searches as your location updates.<br />If you write a different system to the &quot;starting system&quot; field, exports from<br />this system are shown instead.<br />If you are getting 0 results, try reducing min/max hops to 1 and lowering <br />minimum profit. But it is also possible you are at a dead-end.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Exports from current system</span><br />Same as current station, but shows all stations in the system.<br />This is triggered by automatic searches as your location updates.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Loop route</span><br />This finds trade routes which end up in the starting station.<br />The loops are ordered by profit/h.<br />For more variety, add a few minimum hops.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Long route</span><br />This finds connecting trade routes and arranges them by profit/h.<br />Setting minimum hops to a bigger value gives you a grand tour of the galaxy<br />with no repeated stations.<br />The end of the route may be a deadend or a route the optimization algorithm<br />deems unprofitable. Using \'Exports from current system\' is a recommended<br />action after finishing a long route.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Single trades</span><br />This is the traditional min-max single one direction trade search available<br />everywhere. For the sake of nostalgia.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Long route on way to target</span><br />With this you can pick a target system and calculate a high profit series of<br />trade hops between the starting system and your target.<br />It is essentially \'long route\' search, with the additional criteria that<br />each hop must be closer to your target.<br />Note that a profitable route to target is not guaranteed and the route may<br />end somewhere near the target. Also the route is not direct and might wander<br />quite a bit on the way, spiraling down toward your target as dictated by<br />profit/h.<br />The result is sorted first by profit and then by lowest number of hops, so<br />scroll down a bit for variety.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Direct current to target trades</span><br />Find all trades between these two locations without trades in between</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">    The SEARCH input fields:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Starting system / station</span><br />This can be written manually or applied automagically from ED log, if<br />configured. The \'get current\' button on the right side of this area does this.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Target system / station</span><br />Only used for &quot;route on way to target&quot; and &quot;direct trade&quot; searches.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Min profit</span><br />This is a hard limit for basic single trade exchange. Its primary function<br />is to limit the number of possibilities and speed up searching. 1000 is a good<br />fast value for most trading, but might give low or no results if you\'re<br />desperate or in a short range vessel.<br />WARNING! DATA DROWNING HAZARD!<br />Lowering this will flood the tool with more trade data and the search may<br />take a long time.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Smuggling</span><br />Black market trades, or Smuggling is a fun and efficient way to make money<br />in 1.3, especially with the faction bonuses.Black market trades are marked<br />with a skull and a black background in search results.<br />NOTE! Black market prices are unreliable. Prices shown are copied from legal<br />stations in the same system, but actual price may be incorrect.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Max hops</span><br />How many trade stops do we want at most with our search.<br />This value is primarily for optimizing searches with too much data.<br />This may be necessary if you set min profit too low or max distance too high.<br />If you\'re worried about a setting, set this to 1 and give it a go. If it\'s still fast,<br />bump it to 2 and see how it goes. For most use you can confidently set this at<br />99 and no route will ever reach it, due to the route optimization algorithm<br />culling the tail as the average profit/h falls.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Min hops</span><br />Require at least this many trade stops before accepting a trade route.<br />This has some impact on search time, but not to a significant degree.<br />It\'s fun to pick \'long route\' search and set this to a high value for a grand<br />tour.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Max distance</span><br />This is the maximum distance in light years a trade route can be at.<br />This is primarily an optimization parameter, as higher than 50ly is rarely<br />more profitable due to the distance(=time) cost. For smaller vessels with<br />smaller tanks or jump ranges it\'s a good idea to lower this further for<br />performance.<br />    </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">    The SEARCH RESULTS table:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">In multi-hop searches, each profitable commodity trade is shown between the two</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">stations, to give the player options. Then an empty row, followed by the next</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">hop. At the end of each route is a grey row with a route summary.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Tooltips</span> show more details, such as supply and demand, or station distance to</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">star and estimated travel times.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">From current system column</span><br />Distance from your starting system to this system</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Commodity, Export Cr, Import Cr</span><br />Name and prices of market commodity.<br />Tooltip shows data age, buy and sell values, as well as profit and galactic<br />average.<br />Market data age is represented in the main results window with color coding.<br /><span style=\" background-color:#88ff88;\">Green</span> background is current, fading through <span style=\" background-color:#8888ff;\">blue</span> to <span style=\" background-color:#ff8888;\">red</span> as it gets older.<br />If values exceed the market expiration age set in the Options window, the<br />price is colored <span style=\" color:#ffff00; background-color:#ff0000;\">bright red with yellow text</span> to denote that it is heavily outdated.<br />Export commodities in short supply (&lt;100) are also colored like this to warn<br />of potential dead ends.<br /><span style=\" font-weight:600;\">Always </span>check the age and supply of data colored like this.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Distance</span><br />Ly from export to import system.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Minutes travel</span><br />Estimated total time on this trade hop. Includes star-to-star travel and<br />star-to-station travel time.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\"><span style=\" font-weight:600;\">Profit Cr/h</span><br />Profit value normalized by time taken by it.<br />This column is the primary evaluation for profit, and primary sort column.<br />The value is meant to be used as a route \'goodness\' measure rather than actual<br />expected profit estimate, as you never actually spend an hour on a trip.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">    The COMMODITY tab:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can search for stations that import or export certain commodities.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">These are sorted by the distance and value properties.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

