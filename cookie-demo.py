from automation import TaskManager, CommandSequence


def parse_cookie_selectors(file_name):
    """Parse the cookie selectors and return them in data structure.

    The data structure maps FQDNs to a list of CSS selectors.  The empty string
    "" maps to a list of general CSS selectors that apply to many sites.
    """

    unknown = 0

    # Maps a domain to a list of selectors.
    filterlist = dict()

    lines = []
    with open(file_name) as fd:
        for line in fd:
            line = line.strip()

            # AdBlock's filter rules are complex, but we only care about a
            # subset: element hiding rules.  These rules are denoted by the
            # symbol "##".
            if "##" not in line:
                unknown += 1
                continue
            domains, selectors = line.split("##")

            # Commas denote a list of domains and selectors.
            domains = [s.strip() for s in domains.split(",")]
            selectors = [s.strip() for s in selectors.split(",")]

            for domain in domains:
                for selector in selectors:
                    s = filterlist.get(domain, [])
                    filterlist[domain] = s + [selector]

    if unknown > 0:
        print "%d element weren't element hiding rules" % unknown

    return filterlist

file_name = "automation/Commands/cookie-selectors.dat"
selectors = parse_cookie_selectors(file_name)

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = ['http://www.derstandard.at']

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in xrange(NUM_BROWSERS):
    browser_params[i]['disable_flash'] = False #Enable flash for all three browsers
browser_params[0]['headless'] = True #Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site)

    # Start by visiting the page
    command_sequence.get(sleep=0, timeout=60)

    command_sequence.detect_cookie_banner(selectors, timeout=60)

    manager.execute_command_sequence(command_sequence, index='**') # ** = synchronized browsers

# Shuts down the browsers and waits for the data to finish logging
manager.close()
