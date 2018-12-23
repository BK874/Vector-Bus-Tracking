# Brian Knotten
# Bus Tracking Settings

# Port Authority TrueTime API key
API_KEY = ""
# Number of seconds to run
DURATION = 5
LOG_FILE = "bus-tracker.log"

STOPS = {
    # StopId: Location
    2555: 'East Carson and 22nd',
    4814: 'East Carson and 24th'
}

PREDICTIONS = [
    {
        # Stop id
        'stpid': 2555,
        # Bus route name
        'rt': '54',
        # Direction: 'INBOUND' or 'OUTBOUND'
        'dir': 'INBOUND'
    },
    {
        'stpid': 2555,
        'rt': '81',
        'dir': 'INBOUND'
    },
    {
        'stpid': 2555,
        'rt': '83',
        'dir': 'INBOUND'
    },
    {
        'stpid': 4814,
        'rt': '75',
        'dir': 'OUTBOUND'
    }
]
    
        
    
        
