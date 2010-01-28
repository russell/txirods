
from txirods.encoding.binary import rodsObjStat, genQueryOut
from txirods.encoding.rodsml import SimpleXMLParser

rods2_1_generic = {
    'RODS_VERSION': SimpleXMLParser
}

rods2_1_binary = {
    633: rodsObjStat,
    702: genQueryOut,
}
