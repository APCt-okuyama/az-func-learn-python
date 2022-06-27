from opencensus.extension.azure.functions import OpenCensusExtension
from opencensus.trace import config_integration

OpenCensusExtension.configure()

config_integration.trace_integrations(['requests'])

def mytest():
    print('test test')