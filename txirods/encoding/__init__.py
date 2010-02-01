
from txirods.encoding.binary import rodsObjStat, genQueryOut, miscSvrInfo
from txirods.encoding.binary import collOprStat
from txirods.encoding.binary import collInp, genQueryInp, dataObjInp
from txirods.encoding.rodsml import SimpleXMLParser

rods2_1_generic = {
    'RODS_VERSION': SimpleXMLParser
}

rods2_1_binary_inp = {
    608: dataObjInp,
    615: dataObjInp,
    633: dataObjInp,
    606: dataObjInp,
    681: collInp,
    679: collInp,
    702: genQueryInp,
}

rods2_1_binary_out = {
    633: rodsObjStat,
    679: collOprStat,
    700: miscSvrInfo,
    702: genQueryOut,
}
